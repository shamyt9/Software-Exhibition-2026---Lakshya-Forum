from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from functools import wraps

dashboard_bp = Blueprint("dashboard", __name__)

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator

@dashboard_bp.route("/dashboard")
@login_required
def home():
    from database import complaints_col, predictions_col, risks_col
    from datetime import datetime, timedelta

    total        = complaints_col.count_documents({})
    submitted    = complaints_col.count_documents({"status": "submitted"})
    classified   = complaints_col.count_documents({"status": "classified"})
    high_risk    = risks_col.count_documents({"risk_level": "HIGH"})

    cat_pipeline = [
        {"$group": {"_id": "$crime_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    cat_data = list(complaints_col.aggregate(cat_pipeline))

    dist_pipeline = [
        {"$group": {"_id": "$district", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 8}
    ]
    dist_data = list(complaints_col.aggregate(dist_pipeline))

    high_risk_complaints = []
    high_risk_records = list(risks_col.find(
        {"risk_level": "HIGH"}
    ).sort("assessed_at", -1).limit(5))

    for r in high_risk_records:
        c = complaints_col.find_one({"complaint_id": r["complaint_id"]})
        p = predictions_col.find_one({"complaint_id": r["complaint_id"]})
        if c:
            high_risk_complaints.append({
                "complaint_id"   : r["complaint_id"],
                "complainant"    : c.get("complainant_name", "—"),
                "district"       : c.get("district", "—"),
                "risk_score"     : r["risk_score"],
                "category_label" : p["category_label"] if p else "—",
                "amount"         : c.get("amount_involved", 0),
            })

    recent = list(complaints_col.find().sort("submitted_at", -1).limit(5))

    return render_template("dashboard.html",
        user=current_user,
        total=total,
        submitted=submitted,
        classified=classified,
        high_risk=high_risk,
        cat_data=cat_data,
        dist_data=dist_data,
        high_risk_complaints=high_risk_complaints,
        recent=recent,
    )


@dashboard_bp.route("/admin")
@login_required
@role_required("admin")
def admin_panel():
    from database import users_col
    
    # Pagination
    page = max(1, int(request.args.get("page", 1)))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_count = users_col.count_documents({})
    total_pages = (total_count + items_per_page - 1) // items_per_page
    page = min(page, total_pages) if total_pages > 0 else 1
    
    all_users = list(users_col.find({}, {"password": 0}).skip(skip).limit(items_per_page))
    
    return render_template("admin.html",
        users=all_users,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        has_prev=page > 1,
        has_next=page < total_pages,
    )


@dashboard_bp.route("/admin/add-user", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_user():
    from database import users_col
    import bcrypt
    from datetime import datetime

    if request.method == "POST":
        username  = request.form.get("username", "").strip()
        full_name = request.form.get("full_name", "").strip()
        email     = request.form.get("email", "").strip()
        password  = request.form.get("password", "").strip()
        role      = request.form.get("role", "officer")
        district  = request.form.get("district", "").strip()

        if users_col.find_one({"username": username}):
            flash("Username already exists. Choose a different one.", "danger")
            return redirect(url_for("dashboard.add_user"))

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        users_col.insert_one({
            "username"   : username,
            "full_name"  : full_name,
            "email"      : email,
            "password"   : hashed,
            "role"       : role,
            "district"   : district,
            "is_active"  : True,
            "created_at" : datetime.utcnow()
        })
        flash(f"User '{full_name}' created successfully!", "success")
        return redirect(url_for("dashboard.admin_panel"))

    return render_template("admin_add_user.html")


@dashboard_bp.route("/admin/toggle-user/<user_id>")
@login_required
@role_required("admin")
def toggle_user(user_id):
    from database import users_col
    from bson import ObjectId

    user = users_col.find_one({"_id": ObjectId(user_id)})
    if user:
        new_status = not user.get("is_active", True)
        users_col.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": new_status}}
        )
        status_text = "activated" if new_status else "deactivated"
        flash(f"User {status_text} successfully.", "success")
    return redirect(url_for("dashboard.admin_panel"))


@dashboard_bp.route("/admin/reset-password/<user_id>", methods=["POST"])
@login_required
@role_required("admin")
def reset_password(user_id):
    from database import users_col
    from bson import ObjectId
    import bcrypt

    new_pass = request.form.get("new_password", "").strip()
    if len(new_pass) < 6:
        flash("Password must be at least 6 characters.", "danger")
        return redirect(url_for("dashboard.admin_panel"))

    hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
    users_col.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hashed}}
    )
    flash("Password reset successfully.", "success")
    return redirect(url_for("dashboard.admin_panel"))


@dashboard_bp.app_errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403