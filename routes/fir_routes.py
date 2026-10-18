from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import complaints_col, predictions_col, risks_col, firs_col, logs_col, transactions_col
from datetime import datetime

fir_bp = Blueprint("fir", __name__)

# Legal sections and investigation steps per category
FIR_TEMPLATES = {
    "financial_fraud": {
        "sections": ["Section 66C IT Act 2000", "Section 66D IT Act 2000",
                     "Section 420 IPC", "Section 406 IPC", "Section 120B IPC"],
        "steps": [
            "Collect and preserve all transaction records (UTR, TxnID, bank statements)",
            "Issue notice to concerned bank for account freeze under Section 102 CrPC",
            "Send LOC to beneficiary bank for fund hold",
            "Obtain CDR from telecom provider",
            "Trace IP address of fraudulent login from bank/payment gateway",
            "Coordinate with NCRP and 1930 helpline for inter-state tracking",
        ]
    },
    "digital_arrest": {
        "sections": ["Section 66D IT Act 2000", "Section 384 IPC",
                     "Section 419 IPC", "Section 420 IPC", "Section 506 IPC"],
        "steps": [
            "Record victim full statement under Section 161 CrPC",
            "Collect WhatsApp/Telegram/Skype call records and screenshots",
            "Obtain call records from telecom provider for threatening number",
            "Trace UPI/bank account used for extortion money",
            "Issue notice to WhatsApp/Telegram for user account details",
            "Coordinate with Cyber Cell for IP tracing of video call",
        ]
    },
    "fake_news": {
        "sections": ["Section 505(1)(b) IPC", "Section 505(2) IPC",
                     "Section 153A IPC", "Section 54 NDMA Act"],
        "steps": [
            "Preserve original message/post with metadata and timestamp",
            "Identify original sender through forwarding chain analysis",
            "Issue notice to WhatsApp/Facebook/Twitter for account details",
            "Collect witness statements from affected community members",
            "Coordinate with PIB fact-checking unit",
            "Document proof of actual harm caused",
        ]
    },
    "identity_theft": {
        "sections": ["Section 66C IT Act 2000", "Section 419 IPC",
                     "Section 468 IPC", "Section 471 IPC", "Section 43 IT Act 2000"],
        "steps": [
            "Collect all fake profiles/accounts created in victim name",
            "Issue notice to social media platform for profile takedown",
            "Obtain login IP and device details from platform",
            "Check if Aadhaar/PAN misused via UIDAI portal",
            "Verify SIM cloning through telecom provider records",
            "Document all instances of misuse with timestamps",
        ]
    },
    "darknet": {
        "sections": ["Section 66 IT Act 2000", "Section 67 IT Act 2000",
                     "Section 67A IT Act 2000", "Section 292 IPC",
                     "NDPS Act Section 8 (if drugs involved)"],
        "steps": [
            "Preserve all dark web URLs, screenshots and Bitcoin wallet addresses",
            "Coordinate with CERT-In for dark web monitoring",
            "Trace cryptocurrency transactions through blockchain analysis",
            "Issue notice to cryptocurrency exchange for KYC details",
            "Coordinate with Interpol/CBI for cross-border investigation",
            "Preserve digital evidence under Section 65B Indian Evidence Act",
        ]
    },
    "social_media_crime": {
        "sections": ["Section 67 IT Act 2000", "Section 67A IT Act 2000",
                     "Section 354D IPC", "Section 509 IPC",
                     "Section 499 IPC", "Section 500 IPC"],
        "steps": [
            "Preserve all screenshots of fake profile/morphed content with timestamps",
            "Issue legal notice to Instagram/Facebook/Twitter for account takedown",
            "Obtain IP address and device details of accused from platform",
            "Collect statements of victims who received obscene/threatening content",
            "Check if accused is known to victim — collect chat history",
            "File for emergency takedown if content is obscene or defamatory",
        ]
    },
    "online_job_fraud": {
        "sections": ["Section 420 IPC", "Section 406 IPC",
                     "Section 66D IT Act 2000", "Section 120B IPC"],
        "steps": [
            "Collect fake job offer letter, emails and WhatsApp messages as evidence",
            "Trace UPI/bank account where registration fee was transferred",
            "Issue notice to job portal (Naukri/LinkedIn) for fake employer details",
            "Obtain CDR of phone number used by fraudster",
            "Check if multiple victims targeted by same number/account",
            "Coordinate with bank for account freeze if money recently transferred",
        ]
    },
    "sextortion": {
        "sections": ["Section 67A IT Act 2000", "Section 384 IPC",
                     "Section 354C IPC", "Section 354D IPC",
                     "Section 506 IPC", "Section 66E IT Act 2000"],
        "steps": [
            "Record victim statement sensitively — ensure privacy and dignity",
            "Preserve all threatening messages, call recordings and screenshots",
            "Issue notice to WhatsApp/Telegram for account details of accused",
            "Trace payment account if victim has already paid money",
            "Obtain IP address and device details of accused",
            "Coordinate with cyber cell for emergency content takedown",
        ]
    },
    "loan_app_fraud": {
        "sections": ["Section 66C IT Act 2000", "Section 420 IPC",
                     "Section 385 IPC", "Section 386 IPC",
                     "RBI Digital Lending Guidelines 2022"],
        "steps": [
            "Collect loan app name, APK download link and all communications",
            "Check if app is RBI registered — verify on RBI website",
            "Preserve all threatening messages sent to victim and contacts",
            "Issue notice to Google Play Store/Apple Store for app takedown",
            "Trace bank account where loan repayments were collected",
            "Collect statements of contacts who received morphed/obscene content",
        ]
    },
    "cyber_bullying": {
        "sections": ["Section 507 IPC", "Section 504 IPC",
                     "Section 354D IPC", "Section 66A IT Act 2000 (advisory)",
                     "Section 67 IT Act 2000"],
        "steps": [
            "Preserve all threatening/abusive messages with date and timestamps",
            "Collect screenshots of all platforms where harassment occurred",
            "Issue notice to platform for account details of accused",
            "Obtain IP address of accused from platform",
            "Check if victim is minor — if yes invoke POCSO Act additionally",
            "Advise victim to preserve all evidence and not delete conversations",
        ]
    },
}

def generate_fir_number():
    year  = datetime.utcnow().year
    count = firs_col.count_documents({})
    return f"FIR/CYB/{year}/{str(count + 1).zfill(4)}"


@fir_bp.route("/complaints/<cmp_id>/fir")
@login_required
def fir_view(cmp_id):
    complaint   = complaints_col.find_one({"complaint_id": cmp_id})
    prediction  = predictions_col.find_one({"complaint_id": cmp_id})
    risk        = risks_col.find_one({"complaint_id": cmp_id})
    transaction = transactions_col.find_one({"complaint_id": cmp_id})
    existing_fir = firs_col.find_one({"complaint_id": cmp_id})

    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("complaint.list_complaints"))

    if not prediction:
        flash("Please run AI Classification first before generating FIR.", "warning")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    category = prediction.get("category", "financial_fraud")
    template = FIR_TEMPLATES.get(category, FIR_TEMPLATES["financial_fraud"])

    return render_template("fir/fir_view.html",
        complaint    = complaint,
        prediction   = prediction,
        risk         = risk,
        transaction  = transaction,
        existing_fir = existing_fir,
        template     = template,
    )


@fir_bp.route("/complaints/<cmp_id>/fir/save", methods=["POST"])
@login_required
def fir_save(cmp_id):
    complaint  = complaints_col.find_one({"complaint_id": cmp_id})
    prediction = predictions_col.find_one({"complaint_id": cmp_id})

    if not complaint or not prediction:
        flash("Missing data. Cannot save FIR.", "danger")
        return redirect(url_for("complaint.list_complaints"))

    fir_text     = request.form.get("fir_text", "").strip()
    fir_number   = request.form.get("fir_number", "").strip()
    ps_name      = request.form.get("ps_name", "").strip()
    sections_raw = request.form.get("sections", "")
    sections     = [s.strip() for s in sections_raw.split(",") if s.strip()]
    action       = request.form.get("action", "draft")

    status = "registered" if action == "register" else "draft"
    if action == "register" and not fir_number:
        fir_number = generate_fir_number()

    # Remove old FIR if exists
    firs_col.delete_one({"complaint_id": cmp_id})
    firs_col.insert_one({
        "complaint_id"   : cmp_id,
        "fir_number"     : fir_number if status == "registered" else None,
        "police_station" : ps_name,
        "sections"       : sections,
        "fir_text_draft" : fir_text,
        "status"         : status,
        "created_by"     : current_user.id,
        "created_at"     : datetime.utcnow()
    })

    # Update complaint status
    new_status = "fir_registered" if status == "registered" else "fir_drafted"
    complaints_col.update_one(
        {"complaint_id": cmp_id},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
    )

    logs_col.insert_one({
        "user_id"      : current_user.id,
        "complaint_id" : cmp_id,
        "action"       : f"fir_{status}",
        "details"      : f"FIR {status} for {cmp_id}",
        "action_at"    : datetime.utcnow()
    })

    msg = f"FIR registered with number {fir_number}!" if status == "registered" else "FIR draft saved successfully!"
    flash(msg, "success")
    return redirect(url_for("fir.fir_view", cmp_id=cmp_id))