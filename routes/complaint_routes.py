from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import complaints_col, transactions_col, logs_col, predictions_col, risks_col
from datetime import datetime
from freeze_requests import get_freeze_requests_by_complaint
from ai.predictor import generate_summary

complaint_bp = Blueprint("complaint", __name__)

def generate_complaint_id():
    year = datetime.utcnow().year
    prefix = f"CMP-{year}-"
    count = complaints_col.count_documents({"complaint_id": {"$regex": f"^{prefix}"}})
    return f"{prefix}{str(count + 1).zfill(5)}"

def run_auto_classify(cmp_id, complaint_text, amount):
    """Auto-classify complaint immediately after registration"""
    try:
        from ai.predictor import predict
        result = predict(complaint_text, amount)

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
            "reason"       : f"Auto-classified: {result['confidence_pct']}% confidence · Category severity · Amount band",
            "assessed_at"  : datetime.utcnow()
        })

        complaints_col.update_one(
            {"complaint_id": cmp_id},
            {"$set": {
                "crime_type"  : result["category"],
                "risk_level"  : result["risk_level"],
                "risk_score"  : result["risk_score"],
                "status"      : "classified",
                "updated_at"  : datetime.utcnow()
            }}
        )

        logs_col.insert_one({
            "user_id"      : "system",
            "complaint_id" : cmp_id,
            "action"       : "auto_ai_classified",
            "details"      : f"Auto-classified as {result['category_label']} ({result['confidence_pct']}% confidence) | Risk: {result['risk_level']}",
            "action_at"    : datetime.utcnow(),
            "permanent"    : True
        })

        return result

    except Exception as e:
        logs_col.insert_one({
            "user_id"      : "system",
            "complaint_id" : cmp_id,
            "action"       : "auto_classify_failed",
            "details"      : f"Auto-classification failed: {str(e)}",
            "action_at"    : datetime.utcnow(),
            "permanent"    : True
        })
        return None


@complaint_bp.route("/complaints")
@login_required
def list_complaints():
    if current_user.role == "officer":
        query = {"assigned_to": current_user.id}
    elif current_user.role in ["admin", "supervisor", "analyst"]:
        query = {}
    else:
        query = {"assigned_to": current_user.id}

    # Filter support
    status_filter   = request.args.get("status", "")
    category_filter = request.args.get("category", "")
    district_filter = request.args.get("district", "")

    if status_filter:
        query["status"] = status_filter
    if category_filter:
        query["crime_type"] = category_filter
    if district_filter:
        query["district"] = district_filter

    # Pagination
    page = max(1, int(request.args.get("page", 1)))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_count = complaints_col.count_documents(query)
    total_pages = (total_count + items_per_page - 1) // items_per_page
    page = min(page, total_pages) if total_pages > 0 else 1
    
    complaints = list(complaints_col.find(query).sort("submitted_at", -1).skip(skip).limit(items_per_page))

    return render_template("complaints/list.html",
        complaints      = complaints,
        status_filter   = status_filter,
        category_filter = category_filter,
        district_filter = district_filter,
        page            = page,
        total_pages     = total_pages,
        total_count     = total_count,
        has_prev        = page > 1,
        has_next        = page < total_pages,
        max             = max,
        min             = min,
    )


@complaint_bp.route("/complaints/queue")
@login_required
def priority_queue():
    """Priority queue — sorted by risk score HIGH on top"""
    from database import risks_col
    import math

    # Get all risk assessments sorted by score
    risk_records = list(risks_col.find().sort("risk_score", -1))

    queue = []
    for r in risk_records:
        c = complaints_col.find_one({"complaint_id": r["complaint_id"]})
        p = predictions_col.find_one({"complaint_id": r["complaint_id"]})
        if c:
            queue.append({
                "complaint_id"   : r["complaint_id"],
                "complainant"    : c.get("complainant_name", "—"),
                "district"       : c.get("district", "—"),
                "risk_level"     : r.get("risk_level", "LOW"),
                "risk_score"     : r.get("risk_score", 0),
                "category_label" : p["category_label"] if p else c.get("crime_type", "—"),
                "amount"         : c.get("amount_involved", 0),
                "status"         : c.get("status", "—"),
                "submitted_at"   : c.get("submitted_at"),
                "assigned_to"    : c.get("assigned_to_name", "Unassigned"),
            })

    # Separate by risk level
    high   = [q for q in queue if q["risk_level"] == "HIGH"]
    medium = [q for q in queue if q["risk_level"] == "MEDIUM"]
    low    = [q for q in queue if q["risk_level"] == "LOW"]

    # Pagination
    page = max(1, int(request.args.get("page", 1)))
    items_per_page = 10

    # Paginate high risk
    high_pages = math.ceil(len(high) / items_per_page) if high else 1
    high_skip = (page - 1) * items_per_page
    high_paginated = high[high_skip:high_skip + items_per_page]

    # Paginate medium risk
    medium_pages = math.ceil(len(medium) / items_per_page) if medium else 1
    medium_skip = (page - 1) * items_per_page
    medium_paginated = medium[medium_skip:medium_skip + items_per_page]

    # Paginate low risk
    low_pages = math.ceil(len(low) / items_per_page) if low else 1
    low_skip = (page - 1) * items_per_page
    low_paginated = low[low_skip:low_skip + items_per_page]

    # Get max pages from all three lists
    max_pages = max(high_pages, medium_pages, low_pages)
    page = min(page, max_pages) if max_pages > 0 else 1

    return render_template("complaints/queue.html",
        high=high_paginated, medium=medium_paginated, low=low_paginated,
        total_high=len(high), total_medium=len(medium), total_low=len(low),
        page=page,
        total_pages=max_pages,
        has_prev=page > 1,
        has_next=page < max_pages,
        max=max,
        min=min,
    )


@complaint_bp.route("/complaints/new", methods=["GET", "POST"])
@login_required
def new_complaint():
    if request.method == "POST":
        cmp_id = generate_complaint_id()
        amount = request.form.get("amount_involved", 0)
        try:
            amount = float(amount)
        except:
            amount = 0.0

        complaint_text = request.form.get("complaint_text", "").strip()
        txn_id = request.form.get("txn_id", "").strip()

        complaint = {
            "complaint_id"     : cmp_id,
            "complainant_name" : request.form.get("complainant_name", "").strip(),
            "mobile"           : request.form.get("mobile", "").strip(),
            "district"         : request.form.get("district", "").strip(),
            "complaint_text"   : complaint_text,
            "amount_involved"  : amount,
            "txn_id"           : txn_id,
            "source"           : request.form.get("source", "walk-in"),
            "crime_type"       : "pending_ai",
            "risk_level"       : "PENDING",
            "risk_score"       : 0,
            "status"           : "submitted",
            "assigned_to"      : None,
            "submitted_by"     : current_user.id,
            "submitted_at"     : datetime.utcnow(),
            "updated_at"       : datetime.utcnow()
        }

        complaints_col.insert_one(complaint)

        # Create transaction record if details provided
        if txn_id or amount > 0:
            transactions_col.insert_one({
                "complaint_id"        : cmp_id,
                "txn_id"              : txn_id,
                "utr"                 : txn_id,
                "amount"              : amount,
                "bank"                : request.form.get("bank_name", "").strip(),
                "account_masked"      : request.form.get("account_masked", "").strip(),
                "channel"             : request.form.get("channel", "UPI"),
                "beneficiary_account" : request.form.get("beneficiary", "").strip(),
                "created_at"          : datetime.utcnow()
            })

        # Permanent registration log
        logs_col.insert_one({
            "user_id"      : current_user.id,
            "complaint_id" : cmp_id,
            "action"       : "complaint_registered",
            "details"      : f"Complaint {cmp_id} registered by {current_user.full_name}",
            "action_at"    : datetime.utcnow(),
            "permanent"    : True
        })

        # Auto-classify immediately
        result = run_auto_classify(cmp_id, complaint_text, amount)

        if result:
            flash(f"Complaint {cmp_id} registered and auto-classified as {result['category_label']} (Risk: {result['risk_level']})", "success")
        else:
            flash(f"Complaint {cmp_id} registered. AI classification pending.", "warning")

        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    return render_template("complaints/new.html")


@complaint_bp.route("/complaints/<cmp_id>")
@login_required
def view_complaint(cmp_id):
    from database import predictions_col, risks_col
    import json
    import os

    complaint  = complaints_col.find_one({"complaint_id": cmp_id})
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("complaint.list_complaints"))
    
    transaction = transactions_col.find_one({"complaint_id": cmp_id})
    prediction  = predictions_col.find_one({"complaint_id": cmp_id})
    risk        = risks_col.find_one({"complaint_id": cmp_id})
    freezes     = get_freeze_requests_by_complaint(cmp_id)
    
    ai_summary = None
    if prediction and prediction.get("category") in ["financial_fraud", "cyber_financial_fraud"]:
        amount = transaction.get("amount", 0) if transaction else complaint.get("amount_involved", 0)
        bank = transaction.get("bank", "N/A") if transaction else "N/A"
        txn = transaction.get("txn_id", "N/A") if transaction else "N/A"
        ai_summary = generate_summary(complaint.get("complaint_text", ""), amount, bank, txn)

    # Load SOP data
    sop_data = None
    try:
        sop_path = os.path.join("static", "sops.json")
        with open(sop_path, "r", encoding="utf-8") as f:
            sops_json = json.load(f)
            
        # Mapping logic
        category_key = "default_sop"
        if prediction and "category" in prediction:
            cat = prediction["category"]
            if cat in sops_json["sops"]:
                category_key = cat
            elif cat == "cyber_bullying":
                category_key = "cyber_stalking"
            elif cat == "social_media_crime":
                category_key = "cyber_stalking" # or another suitable mapping
        
        if category_key == "default_sop":
            sop_data = sops_json["default_sop"]
        else:
            sop_data = sops_json["sops"].get(category_key, sops_json["default_sop"])
            
    except Exception as e:
        print(f"Error loading SOP: {e}")
        sop_data = None

    return render_template("complaints/view.html",
        complaint   = complaint,
        transaction = transaction,
        prediction  = prediction,
        risk        = risk,
        sop         = sop_data,
        freezes     = freezes,
        ai_summary  = ai_summary,
        now         = datetime.utcnow(),
        urls = {
            'ai_classify': url_for('ai.classify', cmp_id=cmp_id),
            'ai_result': url_for('ai.result', cmp_id=cmp_id),
            'fir_view': url_for('fir.fir_view', cmp_id=cmp_id),
            'freeze_generate': url_for('freeze.generate_freeze', cmp_id=cmp_id),
            'assignment_assign': url_for('assignment.assign', cmp_id=cmp_id),
            'complaint_edit': url_for('complaint.edit_complaint', cmp_id=cmp_id),
            'update_status': url_for('complaint.update_status', cmp_id=cmp_id),
            'update_sop_step': url_for('complaint.update_sop_step', cmp_id=cmp_id),
            'download_sop_pdf': url_for('complaint.download_sop_pdf', cmp_id=cmp_id),
            'update_reversal_status': url_for('complaint.update_reversal_status', cmp_id=cmp_id),
            'generate_bank_letter': url_for('complaint.generate_bank_letter', cmp_id=cmp_id),
        }
    )


@complaint_bp.route("/complaints/<cmp_id>/update_sop_step", methods=["POST"])
@login_required
def update_sop_step(cmp_id):
    import json
    data = request.get_json()
    step_number = data.get("step_number")
    completed = data.get("completed", False)
    
    # Store SOP progress in complaint document
    # Structure: "sop_progress": { "1": true, "2": false, ... }
    field = f"sop_progress.{step_number}"
    complaints_col.update_one(
        {"complaint_id": cmp_id},
        {"$set": {field: completed, "updated_at": datetime.utcnow()}}
    )
    
    return {"status": "success", "step": step_number, "completed": completed}


@complaint_bp.route("/complaints/<cmp_id>/sop_pdf")
@login_required
def download_sop_pdf(cmp_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
    from reportlab.lib import colors
    import io
    from flask import send_file

    complaint = complaints_col.find_one({"complaint_id": cmp_id})
    prediction = predictions_col.find_one({"complaint_id": cmp_id})
    
    # Load SOP data again for PDF
    import json
    import os
    sop_data = None
    try:
        sop_path = os.path.join("static", "sops.json")
        with open(sop_path, "r", encoding="utf-8") as f:
            sops_json = json.load(f)
        
        cat = prediction["category"] if prediction else "default_sop"
        if cat in sops_json["sops"]:
            sop_data = sops_json["sops"][cat]
        else:
            sop_data = sops_json["default_sop"]
    except:
        return "Error loading SOP data", 500

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1E40AF'), spaceAfter=12)
    elements.append(Paragraph(f"Investigation SOP: {sop_data['category_name']}", title_style))
    elements.append(Paragraph(f"Complaint ID: {cmp_id}", styles['Normal']))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %b %Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    # Complaint Summary Table
    elements.append(Paragraph("Case Summary", styles['Heading2']))
    summary_data = [
        ["Complainant", complaint.get("complainant_name", "N/A")],
        ["District", complaint.get("district", "N/A")],
        ["Crime Type", complaint.get("crime_type", "N/A").replace("_", " ").title()],
        ["Amount Involved", f"Rs. {complaint.get('amount_involved', 0)}"]
    ]
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EFF6FF')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))

    # Investigation Steps
    elements.append(Paragraph("Standard Operating Procedure Steps", styles['Heading2']))
    progress = complaint.get("sop_progress", {})
    
    steps_data = [["#", "Action", "Responsible", "Status"]]
    for step in sop_data['investigation_steps']:
        status = "COMPLETED" if progress.get(str(step['step_number'])) else "PENDING"
        steps_data.append([
            str(step['step_number']),
            Paragraph(f"<b>{step['action']}</b><br/><font size='8'>{step['description']}</font>", styles['Normal']),
            step['responsible'],
            status
        ])
    
    steps_table = Table(steps_data, colWidths=[0.4*inch, 3.5*inch, 1.2*inch, 0.9*inch])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(steps_table)
    
    # Required Authorities
    if sop_data.get('required_authorities'):
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Required Authorities & Coordination", styles['Heading2']))
        auth_list = [ListItem(Paragraph(auth, styles['Normal'])) for auth in sop_data['required_authorities']]
        elements.append(ListFlowable(auth_list, bulletType='bullet'))

    # Footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("This is an AI-generated investigation guideline. Please follow official police protocols.", 
                             ParagraphStyle('Footer', parent=styles['Italic'], fontSize=8, alignment=1)))

    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"SOP_{cmp_id}.pdf", mimetype='application/pdf')


@complaint_bp.route("/complaints/<cmp_id>/status", methods=["POST"])
@login_required
def update_status(cmp_id):
    # Only admin and supervisor can update status
    if current_user.role not in ["admin", "supervisor"]:
        flash("You do not have permission to update status.", "danger")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    new_status  = request.form.get("status")
    old_complaint = complaints_col.find_one({"complaint_id": cmp_id})
    old_status  = old_complaint.get("status", "unknown") if old_complaint else "unknown"

    complaints_col.update_one(
        {"complaint_id": cmp_id},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
    )

    # Permanent log — cannot be deleted
    logs_col.insert_one({
        "user_id"      : current_user.id,
        "complaint_id" : cmp_id,
        "action"       : "status_updated",
        "details"      : f"Status changed from '{old_status}' to '{new_status}' by {current_user.full_name}",
        "action_at"    : datetime.utcnow(),
        "permanent"    : True
    })

    flash(f"Status updated to '{new_status}' successfully.", "success")
    return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))


@complaint_bp.route("/complaints/<cmp_id>/edit", methods=["GET", "POST"])
@login_required
def edit_complaint(cmp_id):
    # Only admin can edit
    if current_user.role != "admin":
        flash("Only Admin can edit complaints.", "danger")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    complaint = complaints_col.find_one({"complaint_id": cmp_id})
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("complaint.list_complaints"))

    if request.method == "POST":
        new_name   = request.form.get("complainant_name", "").strip()
        new_mobile = request.form.get("mobile", "").strip()
        new_text   = request.form.get("complaint_text", "").strip()
        new_amount = request.form.get("amount_involved", 0)
        try:
            new_amount = float(new_amount)
        except:
            new_amount = 0.0

        # Track what changed
        changes = []
        if new_name   != complaint.get("complainant_name"): changes.append(f"Name: {complaint.get('complainant_name')} → {new_name}")
        if new_mobile != complaint.get("mobile"):           changes.append(f"Mobile: {complaint.get('mobile')} → {new_mobile}")
        if new_text   != complaint.get("complaint_text"):   changes.append("Complaint text updated")
        if new_amount != complaint.get("amount_involved"):  changes.append(f"Amount: {complaint.get('amount_involved')} → {new_amount}")

        complaints_col.update_one(
            {"complaint_id": cmp_id},
            {"$set": {
                "complainant_name" : new_name,
                "mobile"           : new_mobile,
                "complaint_text"   : new_text,
                "amount_involved"  : new_amount,
                "updated_at"       : datetime.utcnow(),
                "last_edited_by"   : current_user.full_name,
            }}
        )

        # Permanent log of edit
        logs_col.insert_one({
            "user_id"      : current_user.id,
            "complaint_id" : cmp_id,
            "action"       : "complaint_edited",
            "details"      : f"Edited by Admin {current_user.full_name}. Changes: {' | '.join(changes) if changes else 'No changes'}",
            "action_at"    : datetime.utcnow(),
            "permanent"    : True
        })

        # Re-classify after edit if text changed
        if "Complaint text updated" in changes:
            run_auto_classify(cmp_id, new_text, new_amount)
            flash("Complaint updated and re-classified by AI.", "success")
        else:
            flash("Complaint updated successfully.", "success")

        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))

    return render_template("complaints/edit.html", complaint=complaint)

@complaint_bp.route("/complaints/<cmp_id>/update_reversal_status", methods=["POST"])
@login_required
def update_reversal_status(cmp_id):
    from flask import request, jsonify
    data = request.get_json()
    new_status = data.get("status")

    if not new_status:
        return jsonify({"success": False, "error": "No status provided"}), 400

    complaints_col.update_one(
        {"complaint_id": cmp_id},
        {"$set": {
            "reversal_status": new_status,
            "reversal_updated_at": datetime.utcnow()
        }}
    )

    logs_col.insert_one({
        "user_id": current_user.id,
        "complaint_id": cmp_id,
        "action": "reversal_status_updated",
        "details": f"Fund reversal status updated to: {new_status}",
        "action_at": datetime.utcnow(),
        "permanent": True
    })

    return jsonify({"success": True})

@complaint_bp.route("/complaints/<cmp_id>/generate_bank_letter")
@login_required
def generate_bank_letter(cmp_id):
    from io import BytesIO
    from flask import send_file
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

    complaint = complaints_col.find_one({"complaint_id": cmp_id})
    transaction = transactions_col.find_one({"complaint_id": cmp_id})

    if not complaint:
        return "Complaint not found", 404

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, alignment=TA_CENTER, spaceAfter=20)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=14, alignment=TA_JUSTIFY, spaceAfter=10)
    bold_style = ParagraphStyle('Bold', parent=body_style, fontName='Helvetica-Bold')

    # Header
    elements.append(Paragraph("<b>OFFICE OF THE SUPERINTENDENT OF POLICE, CYBER CELL</b>", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%d %b %Y')}", body_style))
    elements.append(Paragraph(f"Ref: {cmp_id}/BANK/FREEZE/2026", body_style))
    elements.append(Spacer(1, 20))

    # Subject
    elements.append(Paragraph("<b>SUBJECT: URGENT REQUEST FOR TRANSACTION FREEZE AND FUND REVERSAL</b>", bold_style))
    elements.append(Spacer(1, 15))

    # To
    elements.append(Paragraph(f"To,<br/>The Nodal Officer / Branch Manager,<br/>{transaction.get('bank', 'Concerned Bank') if transaction else 'Concerned Bank'}", body_style))
    elements.append(Spacer(1, 15))

    # Content
    content = f"""This is to inform you that a cyber financial fraud complaint has been registered with our office (ID: {cmp_id}) and classified as a financial fraud incident. 
    The investigation reveals that an unauthorized transaction of ₹{transaction.get('amount', 0) if transaction else 0} was initiated 
    from the victim's account to account number {transaction.get('beneficiary_account', 'N/A') if transaction else 'N/A'} 
    with Transaction ID {transaction.get('utr', 'N/A') if transaction else 'N/A'} at {transaction.get('bank', 'Concerned Bank') if transaction else 'Concerned Bank'}.
    """
    elements.append(Paragraph(content, body_style))

    elements.append(Paragraph("<b>LEGAL MANDATE & DIRECTIVES:</b>", bold_style))
    elements.append(Paragraph(f"Under the powers vested in the Police under <b>Section 102 CrPC</b> and in alignment with <b>Section 66C/66D of the Information Technology Act 2000</b> and <b>Section 420 IPC</b>, you are hereby directed to:", body_style))
    
    elements.append(Paragraph("1. <b>IMMEDIATE FREEZE:</b> Place an immediate debit freeze on the beneficiary account mentioned above to prevent further siphoning of funds.", body_style))
    elements.append(Paragraph("2. <b>FUND REVERSAL:</b> Initiate the process for reversal of funds to the complainant's source account as per <b>RBI Guidelines (Circular RBI/2017-18/15)</b> on Limiting Liability of Customers in Unauthorized Electronic Banking Transactions.", body_style))
    elements.append(Paragraph("3. <b>KYC DETAILS:</b> Furnish the complete KYC details, account statement, and IP logs of the beneficiary account within 24 hours.", body_style))
    elements.append(Paragraph("4. <b>LIEN MARK:</b> If funds are already moved, mark a lien on the subsequent accounts where the funds have been transferred.", body_style))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Failure to comply with these directives may attract legal action under Section 175/188 IPC for non-compliance with lawful orders of a public servant.", body_style))

    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<b>Authorized Signatory,</b><br/>Cyber Cell Department<br/>State Police Headquarters", body_style))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"Bank_Letter_{cmp_id}.pdf", mimetype='application/pdf')
