from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from database import complaints_col, predictions_col, risks_col, logs_col, users_col
from datetime import datetime, timedelta

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/reports")
@login_required
def reports():
    # ── Category wise counts ───────────────────────────────
    cat_pipeline = [
        {"$group": {"_id": "$crime_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    cat_data = list(complaints_col.aggregate(cat_pipeline))

    # ── District wise counts ───────────────────────────────
    dist_pipeline = [
        {"$group": {"_id": "$district", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    dist_data = list(complaints_col.aggregate(dist_pipeline))

    # ── Status wise counts ─────────────────────────────────
    status_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    status_data = list(complaints_col.aggregate(status_pipeline))

    # ── Risk wise counts ───────────────────────────────────
    risk_pipeline = [
        {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    risk_data = list(risks_col.aggregate(risk_pipeline))

    # ── Total amounts by category ──────────────────────────
    amount_pipeline = [
        {"$group": {
            "_id"          : "$crime_type",
            "total_amount" : {"$sum": "$amount_involved"},
            "avg_amount"   : {"$avg": "$amount_involved"},
            "count"        : {"$sum": 1}
        }},
        {"$sort": {"total_amount": -1}}
    ]
    amount_data = list(complaints_col.aggregate(amount_pipeline))

    # ── Temporal Heatmap Data ───────────────────────────
    temporal_pipeline = [
        {
            "$project": {
                "day": {"$dayOfWeek": "$submitted_at"},
                "hour": {"$hour": "$submitted_at"}
            }
        },
        {
            "$group": {
                "_id": {"day": "$day", "hour": "$hour"},
                "count": {"$sum": 1}
            }
        }
    ]
    temporal_data = list(complaints_col.aggregate(temporal_pipeline))

    # ── Matrix Heatmap Data (District vs Category) ──────
    matrix_pipeline = [
        {
            "$group": {
                "_id": {"district": "$district", "category": "$crime_type"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]
    matrix_data = list(complaints_col.aggregate(matrix_pipeline))

    # ── Overall stats ──────────────────────────────────────
    total        = complaints_col.count_documents({})
    total_amount = list(complaints_col.aggregate([
        {"$group": {"_id": None, "total": {"$sum": "$amount_involved"}}}
    ]))
    total_amount = total_amount[0]["total"] if total_amount else 0

    high_risk  = risks_col.count_documents({"risk_level": "HIGH"})
    classified = complaints_col.count_documents({"status": {"$in": ["classified", "assigned", "fir_drafted", "fir_registered"]}})
    fir_count  = complaints_col.count_documents({"status": {"$in": ["fir_drafted", "fir_registered"]}})

    return render_template("reports.html",
        cat_data      = cat_data,
        dist_data     = dist_data,
        status_data   = status_data,
        risk_data     = risk_data,
        amount_data   = amount_data,
        temporal_data = temporal_data,
        matrix_data   = matrix_data,
        total         = total,
        total_amount  = total_amount,
        high_risk     = high_risk,
        classified    = classified,
        fir_count     = fir_count,
    )


@reports_bp.route("/audit-logs")
@login_required
def audit_logs():
    if current_user.role not in ["admin", "supervisor"]:
        from flask import flash, redirect, url_for
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard.home"))

    # Pagination
    page = max(1, int(request.args.get("page", 1)))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_count = logs_col.count_documents({})
    total_pages = (total_count + items_per_page - 1) // items_per_page
    page = min(page, total_pages) if total_pages > 0 else 1
    
    logs = list(logs_col.find().sort("action_at", -1).skip(skip).limit(items_per_page))

    # Attach usernames
    for log in logs:
        user = None
        if log.get("user_id"):
            try:
                # Only try to convert to ObjectId if it looks like a valid hex string
                user_id = log["user_id"]
                if isinstance(user_id, str) and len(user_id) == 24:
                    from bson import ObjectId
                    user = users_col.find_one({"_id": ObjectId(user_id)}, {"username": 1, "full_name": 1})
            except (ValueError, Exception):
                # If conversion fails, user_id might be a system value like "system"
                pass
        log["username"] = user["full_name"] if user else "Unknown"

    return render_template("audit_logs.html",
        logs=logs,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        has_prev=page > 1,
        has_next=page < total_pages,
    )