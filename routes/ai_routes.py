from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from database import complaints_col, predictions_col, risks_col, logs_col
from ai.predictor import predict
from datetime import datetime

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/complaints/<cmp_id>/classify")
@login_required
def classify(cmp_id):
    complaint = complaints_col.find_one({"complaint_id": cmp_id})
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("complaint.list_complaints"))

    result = predict(
        complaint["complaint_text"],
        complaint.get("amount_involved", 0)
    )

    predictions_col.delete_one({"complaint_id": cmp_id})
    predictions_col.insert_one({
        "complaint_id"   : cmp_id,
        "category"       : result["category"],
        "category_label" : result["category_label"],
        "confidence"     : result["confidence"],
        "all_scores"     : result["all_scores"],
        "legal_sections" : result["legal_sections"],
        "model_version"  : "v2.0",
        "predicted_at"   : datetime.utcnow()
    })

    risks_col.delete_one({"complaint_id": cmp_id})
    risks_col.insert_one({
        "complaint_id" : cmp_id,
        "risk_score"   : result["risk_score"],
        "risk_level"   : result["risk_level"],
        "reason"       : f"Confidence {result['confidence_pct']}% · Category severity · Amount band",
        "assessed_at"  : datetime.utcnow()
    })

    complaints_col.update_one(
        {"complaint_id": cmp_id},
        {"$set": {"status": "classified", "crime_type" : result["category"],"updated_at": datetime.utcnow()}}
    )

    logs_col.insert_one({
        "user_id"      : current_user.id,
        "complaint_id" : cmp_id,
        "action"       : "ai_classified",
        "details"      : f"Classified as {result['category_label']} with {result['confidence_pct']}% confidence",
        "action_at"    : datetime.utcnow()
    })

    flash(f"AI classified as: {result['category_label']} ({result['confidence_pct']}% confidence)", "success")
    return redirect(url_for("ai.result", cmp_id=cmp_id))


@ai_bp.route("/complaints/<cmp_id>/result")
@login_required
def result(cmp_id):
    from database import transactions_col
    complaint   = complaints_col.find_one({"complaint_id": cmp_id})
    prediction  = predictions_col.find_one({"complaint_id": cmp_id})
    risk        = risks_col.find_one({"complaint_id": cmp_id})
    transaction = transactions_col.find_one({"complaint_id": cmp_id})

    return render_template("ai/result.html",
        complaint=complaint,
        prediction=prediction,
        risk=risk,
        transaction=transaction
    )