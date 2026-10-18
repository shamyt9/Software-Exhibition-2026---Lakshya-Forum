from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import complaints_col, users_col, logs_col
from datetime import datetime
from bson import ObjectId

assignment_bp = Blueprint("assignment", __name__)

@assignment_bp.route("/complaints/<cmp_id>/assign", methods=["GET", "POST"])
@login_required
def assign(cmp_id):
    # Only admin and supervisor can assign
    if current_user.role not in ["admin", "supervisor"]:
        flash("You do not have permission to assign complaints.", "danger")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    complaint = complaints_col.find_one({"complaint_id": cmp_id})
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("complaint.list_complaints"))

    # Get all active officers and analysts
    officers = list(users_col.find(
        {"role": {"$in": ["officer", "analyst"]}, "is_active": True},
        {"password": 0}
    ))

    if request.method == "POST":
        officer_id   = request.form.get("officer_id", "").strip()
        priority     = request.form.get("priority", "normal")
        notes        = request.form.get("notes", "").strip()

        if not officer_id:
            flash("Please select an officer.", "danger")
            return redirect(url_for("assignment.assign", cmp_id=cmp_id))

        # Get officer details
        officer = users_col.find_one({"_id": ObjectId(officer_id)})
        if not officer:
            flash("Officer not found.", "danger")
            return redirect(url_for("assignment.assign", cmp_id=cmp_id))

        # Update complaint
        complaints_col.update_one(
            {"complaint_id": cmp_id},
            {"$set": {
                "assigned_to"      : officer_id,
                "assigned_to_name" : officer["full_name"],
                "priority"         : priority,
                "assignment_notes" : notes,
                "status"           : "assigned",
                "assigned_at"      : datetime.utcnow(),
                "updated_at"       : datetime.utcnow()
            }}
        )

        logs_col.insert_one({
            "user_id"      : current_user.id,
            "complaint_id" : cmp_id,
            "action"       : "complaint_assigned",
            "details"      : f"Assigned to {officer['full_name']} with {priority} priority",
            "action_at"    : datetime.utcnow()
        })

        flash(f"Complaint assigned to {officer['full_name']} successfully!", "success")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    # Current assigned officer
    current_officer = None
    if complaint.get("assigned_to"):
        try:
            current_officer = users_col.find_one(
                {"_id": ObjectId(complaint["assigned_to"])},
                {"password": 0}
            )
        except:
            pass

    return render_template("assignment/assign.html",
        complaint       = complaint,
        officers        = officers,
        current_officer = current_officer,
    )


@assignment_bp.route("/my-cases")
@login_required
def my_cases():
    # Officers see their assigned cases
    if current_user.role in ["officer", "analyst"]:
        query = {"assigned_to": current_user.id}
        sort_field = "assigned_at"
    else:
        # Admin/supervisor sees all
        query = {}
        sort_field = "submitted_at"

    # Pagination
    page = max(1, int(request.args.get("page", 1)))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_count = complaints_col.count_documents(query)
    total_pages = (total_count + items_per_page - 1) // items_per_page
    page = min(page, total_pages) if total_pages > 0 else 1
    
    complaints = list(complaints_col.find(query).sort(sort_field, -1).skip(skip).limit(items_per_page))

    return render_template("assignment/my_cases.html",
        complaints=complaints,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        has_prev=page > 1,
        has_next=page < total_pages,
    )