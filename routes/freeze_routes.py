from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from datetime import datetime
from database import complaints_col, predictions_col, risks_col, logs_col
from freeze_requests import (
    check_freeze_eligibility,
    generate_freeze_request,
    save_freeze_request,
    get_freeze_request,
    get_freeze_requests_by_complaint,
    get_all_freeze_requests,
    update_freeze_request_status,
    record_bank_response,
    export_freeze_request_to_json,
    calculate_priority_score
)
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

freeze_bp = Blueprint("freeze", __name__)


def authorize_freeze_request(user_role):
    """Check if user is authorized to generate freeze requests"""
    authorized_roles = ["admin", "supervisor", "sp", "cci", "io"]
    return user_role in authorized_roles


def generate_freeze_request_pdf(freeze_request):
    """Generate a professional PDF document for freeze request"""
    
    # Create PDF in memory
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#c62828'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=10,
        fontName='Helvetica-Bold',
        borderPadding=5,
        borderColor=colors.HexColor('#e0e7ff'),
        borderWidth=1
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    # Header
    elements.append(Paragraph("🔴 URGENT TRANSACTION FREEZE REQUEST", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Request Details Table
    request_data = [
        ["Freeze Request ID:", freeze_request.get('freeze_request_id', 'N/A')],
        ["Complaint ID:", freeze_request.get('complaint_id', 'N/A')],
        ["Request Date & Time:", freeze_request.get('request_timestamp', datetime.utcnow()).strftime('%d-%b-%Y %H:%M:%S')],
        ["Priority Level:", f"🔴 {freeze_request.get('priority_level', 'NORMAL')}"],
        ["Status:", freeze_request.get('status', 'pending').upper()],
    ]
    
    request_table = Table(request_data, colWidths=[2.5*inch, 4*inch])
    request_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(request_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Complainant Details
    elements.append(Paragraph("COMPLAINANT DETAILS", heading_style))
    complainant_data = [
        ["Name:", freeze_request.get('complainant_name', '—')],
        ["Mobile:", freeze_request.get('complainant_mobile', '—')],
        ["District:", freeze_request.get('complainant_district', '—')],
    ]
    complainant_table = Table(complainant_data, colWidths=[2.5*inch, 4*inch])
    complainant_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(complainant_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Crime Classification
    elements.append(Paragraph("CRIME CLASSIFICATION", heading_style))
    crime_data = [
        ["Crime Category:", freeze_request.get('crime_category', '—')],
        ["Risk Level:", freeze_request.get('risk_level', '—')],
        ["Risk Score:", f"{freeze_request.get('risk_score', 0)}/100"],
        ["Priority Score:", f"{freeze_request.get('priority_score', 0)}/100"],
    ]
    crime_table = Table(crime_data, colWidths=[2.5*inch, 4*inch])
    crime_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef2f2')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(crime_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Transaction Details (CRITICAL)
    elements.append(Paragraph("⚠️ TRANSACTION DETAILS (FOR IMMEDIATE FREEZE)", heading_style))
    txn_data = [
        ["Transaction ID / UTR:", freeze_request.get('transaction_id', 'NOT PROVIDED')],
        ["Bank Name:", freeze_request.get('bank_name', 'NOT PROVIDED')],
        ["Beneficiary Account:", freeze_request.get('beneficiary_account', '—')],
        ["Beneficiary Name:", freeze_request.get('beneficiary_name', '—')],
        ["Amount:", f"₹ {freeze_request.get('amount_involved', 0):,.2f}"],
        ["Transaction Date/Time:", freeze_request.get('transaction_timestamp', 'N/A')],
    ]
    txn_table = Table(txn_data, colWidths=[2.5*inch, 4*inch])
    txn_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef3c7')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.red),
    ]))
    elements.append(txn_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Applicable Legal Sections
    elements.append(Paragraph("APPLICABLE LEGAL SECTIONS", heading_style))
    legal_sections = freeze_request.get('applicable_sections', [])
    legal_text = ", ".join(legal_sections) if legal_sections else "—"
    elements.append(Paragraph(f"<b>Sections:</b> {legal_text}", body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # RBI Guidelines
    elements.append(Paragraph("RBI COMPLIANCE & GUIDELINES", heading_style))
    rbi_guideline = freeze_request.get('rbi_guideline', 'RBI Guidelines on Regulation of Payment Systems')
    elements.append(Paragraph(f"<b>Reference:</b> {rbi_guideline}", body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Complaint Summary
    elements.append(Paragraph("COMPLAINT SUMMARY", heading_style))
    summary = freeze_request.get('complaint_summary', 'No summary provided')
    elements.append(Paragraph(summary, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer / Legal Notice
    elements.append(Paragraph(
        "<b>⚖️ LEGAL NOTICE:</b> This is an official freeze request document generated under the authority of Indian Cybercrime Complaint Portal (AICM-DSS) in compliance with RBI guidelines and applicable sections of the Indian Penal Code and Information Technology Act. This document should be forwarded immediately to the concerned bank's nodal officer for urgent transaction blocking within 24-48 hours.",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#7f1d1d'), alignment=TA_JUSTIFY, spaceAfter=10)
    ))
    
    elements.append(Spacer(1, 0.1*inch))
    
    # Officer Details
    officer_data = [
        ["Generated By:", freeze_request.get('requested_by_officer_name', 'System')],
        ["Officer ID:", freeze_request.get('requested_by_officer_id', '—')],
        ["Generated On:", freeze_request.get('request_timestamp', datetime.utcnow()).strftime('%d-%b-%Y %H:%M:%S')],
    ]
    officer_table = Table(officer_data, colWidths=[2.5*inch, 4*inch])
    officer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(officer_table)
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer


@freeze_bp.route("/freeze/check/<cmp_id>", methods=["GET"])
@login_required
def check_eligibility(cmp_id):
    """Check if complaint is eligible for freeze request"""
    if not authorize_freeze_request(current_user.role):
        flash("You do not have permission to manage freeze requests.", "danger")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))
    
    eligibility = check_freeze_eligibility(cmp_id)
    return jsonify(eligibility)


@freeze_bp.route("/freeze/generate/<cmp_id>", methods=["GET", "POST"])
@login_required
def generate_freeze(cmp_id):
    """Generate a new freeze request"""
    if not authorize_freeze_request(current_user.role):
        flash("You do not have permission to generate freeze requests.", "danger")
        return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))
    
    complaint = complaints_col.find_one({"complaint_id": cmp_id})
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("complaint.list_complaints"))
    
    if request.method == "POST":
        # Get manual transaction data from form
        manual_txn_data = None
        try:
            # Extract form data
            txn_id = request.form.get("transaction_id", "")
            bank_name = request.form.get("bank_name", "")
            account_number = request.form.get("beneficiary_account", "")
            amount = float(request.form.get("amount", 0)) if request.form.get("amount") else 0
            beneficiary = request.form.get("beneficiary_name", "")
            
            # If any transaction detail is provided, create manual_txn_data
            if txn_id or bank_name or amount or account_number or beneficiary:
                manual_txn_data = {
                    "txn_id": txn_id,
                    "bank_name": bank_name,
                    "account_number": account_number,
                    "amount": amount,
                    "beneficiary": beneficiary,
                    "timestamp": datetime.utcnow()
                }
        except (ValueError, TypeError) as e:
            flash(f"Invalid form data: {str(e)}", "danger")
            return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))
        
        # Generate freeze request
        freeze_request = generate_freeze_request(
            cmp_id,
            current_user.id,
            current_user.full_name,
            manual_txn_data
        )
        
        if "error" in freeze_request:
            flash(f"Cannot generate freeze request: {freeze_request['error']}", "danger")
            return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))
        
        # Save to database
        result = save_freeze_request(freeze_request, current_user.id)
        
        if result.get("success"):
            flash(f"Freeze request {result.get('freeze_request_id')} generated successfully!", "success")
            return redirect(url_for("freeze.view_freeze_request", freeze_id=result.get("freeze_request_id")))
        else:
            flash(f"Error saving freeze request: {result.get('error')}", "danger")
            return redirect(url_for("complaint.view_complaint", cmp_id=cmp_id))
    
    # GET - Show generation form
    eligibility = check_freeze_eligibility(cmp_id)
    priority_score = calculate_priority_score(cmp_id)
    
    return render_template("freeze/generate.html",
        complaint=complaint,
        complaint_id=complaint.get("complaint_id"),
        complainant_name=complaint.get("complainant_name", "N/A"),
        district=complaint.get("district", "N/A"),
        mobile=complaint.get("mobile", "N/A"),
        transaction_amount=complaint.get("amount_involved", 0),
        eligibility=eligibility,
        priority_score=priority_score
    )


@freeze_bp.route("/freeze/<freeze_id>")
@login_required
def view_freeze_request(freeze_id):
    """View freeze request details"""
    freeze_request = get_freeze_request(freeze_id)
    if not freeze_request:
        flash("Freeze request not found.", "danger")
        return redirect(url_for("freeze.list_freeze_requests"))
    
    complaint = complaints_col.find_one({"complaint_id": freeze_request.get("complaint_id")})
    
    return render_template("freeze/view.html",
        freeze=freeze_request,
        complaint=complaint
    )


@freeze_bp.route("/freeze/list")
@login_required
def list_freeze_requests():
    """List all freeze requests with filters"""
    if not authorize_freeze_request(current_user.role):
        flash("You do not have permission to view freeze requests.", "danger")
        return redirect(url_for("dashboard.dashboard"))
    
    # Get filters from query params
    filters = {}
    status_filter = request.args.get("status", "")
    district_filter = request.args.get("district", "")
    bank_filter = request.args.get("bank", "")
    priority_filter = request.args.get("priority", "")
    
    if status_filter:
        filters["status"] = status_filter
    if district_filter:
        filters["district"] = district_filter
    if bank_filter:
        filters["bank_name"] = bank_filter
    if priority_filter:
        filters["priority"] = priority_filter
    
    # Pagination
    page = max(1, int(request.args.get("page", 1)))
    items_per_page = 15
    
    # Get freeze requests
    all_freezes = get_all_freeze_requests(filters)
    total_count = len(all_freezes)
    total_pages = (total_count + items_per_page - 1) // items_per_page
    
    skip = (page - 1) * items_per_page
    freeze_requests = all_freezes[skip:skip + items_per_page]
    
    # Calculate status counts
    all_freezes_unfiltered = get_all_freeze_requests()
    pending_count = len([f for f in all_freezes_unfiltered if f.get("status") == "pending"])
    approved_count = len([f for f in all_freezes_unfiltered if f.get("status") == "approved"])
    completed_count = len([f for f in all_freezes_unfiltered if f.get("status") == "completed"])
    
    # Get available filters for dropdowns
    available_districts = list(set([f.get("complainant_district") for f in all_freezes_unfiltered if f.get("complainant_district")]))
    available_banks = list(set([f.get("bank_name") for f in all_freezes_unfiltered if f.get("bank_name")]))
    
    return render_template("freeze/list.html",
        freezes=freeze_requests,
        status_filter=status_filter,
        district_filter=district_filter,
        bank_filter=bank_filter,
        priority_filter=priority_filter,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        pending_count=pending_count,
        approved_count=approved_count,
        completed_count=completed_count,
        has_prev=page > 1,
        has_next=page < total_pages,
        available_districts=sorted(available_districts),
        available_banks=sorted(available_banks),
    )


@freeze_bp.route("/freeze/<freeze_id>/download/<format>")
@login_required
def download_freeze_request(freeze_id, format):
    """Download freeze request as PDF or JSON"""
    freeze_request = get_freeze_request(freeze_id)
    if not freeze_request:
        flash("Freeze request not found.", "danger")
        return redirect(url_for("freeze.list_freeze_requests"))
    
    if format == "pdf":
        pdf_buffer = generate_freeze_request_pdf(freeze_request)
        
        # Log download
        logs_col.insert_one({
            "user_id": current_user.id,
            "complaint_id": freeze_request.get("complaint_id"),
            "action": "freeze_request_downloaded",
            "details": f"Freeze request {freeze_id} downloaded as PDF by {current_user.full_name}",
            "action_at": datetime.utcnow(),
            "permanent": True
        })
        
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{freeze_id}_freeze_request.pdf"
        )
    
    elif format == "json":
        json_data = export_freeze_request_to_json(freeze_id)
        
        # Log download
        logs_col.insert_one({
            "user_id": current_user.id,
            "complaint_id": freeze_request.get("complaint_id"),
            "action": "freeze_request_downloaded",
            "details": f"Freeze request {freeze_id} downloaded as JSON by {current_user.full_name}",
            "action_at": datetime.utcnow(),
            "permanent": True
        })
        
        return send_file(
            BytesIO(json.dumps(json_data, indent=2, default=str).encode()),
            mimetype="application/json",
            as_attachment=True,
            download_name=f"{freeze_id}_freeze_request.json"
        )
    
    flash("Invalid format.", "danger")
    return redirect(url_for("freeze.view_freeze_request", freeze_id=freeze_id))


@freeze_bp.route("/freeze/<freeze_id>/status", methods=["POST"])
@login_required
def update_status(freeze_id):
    """Update freeze request status"""
    if not authorize_freeze_request(current_user.role):
        flash("You do not have permission to update freeze requests.", "danger")
        return redirect(url_for("freeze.view_freeze_request", freeze_id=freeze_id))
    
    new_status = request.form.get("status")
    notes = request.form.get("notes", "")
    
    result = update_freeze_request_status(freeze_id, new_status, notes, current_user.id, current_user.full_name)
    
    if result.get("success"):
        flash(f"Freeze request status updated to '{new_status}'.", "success")
    else:
        flash(f"Error updating status: {result.get('error')}", "danger")
    
    return redirect(url_for("freeze.view_freeze_request", freeze_id=freeze_id))


@freeze_bp.route("/freeze/<freeze_id>/bank-response", methods=["POST"])
@login_required
def record_bank_resp(freeze_id):
    """Record bank's response to freeze request"""
    if not authorize_freeze_request(current_user.role):
        flash("You do not have permission to record bank responses.", "danger")
        return redirect(url_for("freeze.view_freeze_request", freeze_id=freeze_id))
    
    bank_ref_id = request.form.get("bank_reference_id", "")
    response_status = request.form.get("response_status", "unknown")
    notes = request.form.get("notes", "")
    
    record_bank_response(freeze_id, bank_ref_id, response_status, notes, current_user.id)
    
    flash("Bank response recorded successfully.", "success")
    return redirect(url_for("freeze.view_freeze_request", freeze_id=freeze_id))
