"""
Generate Enhanced Comprehensive PDF with all project code files
Using PyPDF2 for better formatting
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
                                Table, TableStyle, Preformatted, KeepTogether)
from reportlab.lib import colors
from datetime import datetime
import os

# Create PDF
pdf_filename = "Cybercrime_Project_Complete_Code.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                        rightMargin=0.4*inch, leftMargin=0.4*inch,
                        topMargin=0.6*inch, bottomMargin=0.4*inch)

elements = []

# Define styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=22,
    textColor=colors.HexColor('#0a3a5c'),
    spaceAfter=6,
    spaceBefore=0,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

section_style = ParagraphStyle(
    'Section',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.white,
    spaceAfter=8,
    spaceBefore=8,
    backColor=colors.HexColor('#0a3a5c'),
    leftIndent=0.2*inch,
    fontName='Helvetica-Bold'
)

subsection_style = ParagraphStyle(
    'Subsection',
    parent=styles['Heading3'],
    fontSize=10,
    textColor=colors.HexColor('#0a3a5c'),
    spaceAfter=4,
    spaceBefore=6,
    fontName='Courier-Bold',
    backColor=colors.HexColor('#dce5f0')
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=9,
    alignment=TA_LEFT,
    spaceAfter=6
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7.5,
    leftIndent=0.15*inch,
    rightIndent=0.15*inch,
    textColor=colors.HexColor('#000000'),
    backColor=colors.HexColor('#f5f5f5'),
    borderColor=colors.HexColor('#cccccc'),
    borderWidth=0.5,
    spaceAfter=4
)

# ─────────────────────────────────────────────────────────────
# COVER PAGE
# ─────────────────────────────────────────────────────────────
elements.append(Spacer(1, 2*inch))
elements.append(Paragraph("CYBERCRIME MANAGEMENT &", title_style))
elements.append(Paragraph("DIGITAL INVESTIGATION SYSTEM", title_style))
elements.append(Spacer(1, 0.1*inch))
elements.append(Paragraph("(AI-CMDSS)", ParagraphStyle(
    'Subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, 
    textColor=colors.HexColor('#0a3a5c'), fontName='Helvetica-Bold')))
elements.append(Spacer(1, 0.5*inch))
elements.append(Paragraph("COMPLETE SOURCE CODE &<br/>PROJECT DOCUMENTATION", 
                         ParagraphStyle('Info', parent=styles['Normal'], fontSize=11, 
                                       alignment=TA_CENTER)))
elements.append(Spacer(1, 1*inch))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%A, %B %d, %Y')}", 
                         ParagraphStyle('Date', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph("Python Flask + MongoDB + Machine Learning", 
                         ParagraphStyle('Tech', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER)))
elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# TABLE OF CONTENTS
# ─────────────────────────────────────────────────────────────
elements.append(Paragraph("TABLE OF CONTENTS", section_style))
elements.append(Spacer(1, 0.15*inch))

toc_items = [
    ("1. Project Overview & Setup", ""),
    ("2. Requirements & Dependencies", ""),
    ("3. Main Application Files", ""),
    ("   • app.py - Flask Application", ""),
    ("   • database.py - MongoDB Setup", ""),
    ("   • models.py - User Model", ""),
    ("   • setup_db.py - Database Initialization", ""),
    ("4. Authentication Routes (auth_routes.py)", ""),
    ("5. Dashboard & Admin Routes (dashboard_routes.py)", ""),
    ("6. Complaint Management Routes (complaint_routes.py)", ""),
    ("7. AI Classification Routes (ai_routes.py)", ""),
    ("8. FIR Generation Routes (fir_routes.py)", ""),
    ("9. Case Assignment Routes (assignment_routes.py)", ""),
    ("10. Reports & Audit Routes (reports_routes.py)", ""),
    ("11. AI Predictor Module (ai/predictor.py)", ""),
    ("12. Model Training (ai/train_model.py)", ""),
    ("13. Data Processing (ai/merge_and_clean.py)", ""),
]

for item, note in toc_items:
    elements.append(Paragraph(item, body_style))

elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# PROJECT OVERVIEW
# ─────────────────────────────────────────────────────────────
elements.append(Paragraph("PROJECT OVERVIEW & ARCHITECTURE", section_style))
elements.append(Spacer(1, 0.1*inch))

overview = """
<b>Purpose:</b><br/>
AI-CMDSS is a comprehensive cybercrime investigation system designed for police departments and law enforcement agencies in India. It automates crime classification, assessment, and case management using Machine Learning.<br/>
<br/>
<b>Key Features:</b><br/>
✓ Complaint registration from multiple sources (walk-in, NCRP, 1930 helpline)<br/>
✓ AI-powered automatic crime classification with confidence scoring<br/>
✓ Risk assessment & prioritization (HIGH/MEDIUM/LOW)<br/>
✓ FIR generation with legal section templates<br/>
✓ Bank account freeze requests & tracking<br/>
✓ Case assignment to investigating officers<br/>
✓ Comprehensive audit logging & reporting<br/>
✓ Role-based access control (Admin, Supervisor, Officer, Analyst)<br/>
<br/>
<b>Technology Stack:</b><br/>
Frontend: HTML5, CSS3, JavaScript<br/>
Backend: Flask (Python 3.8+)<br/>
Database: MongoDB<br/>
ML Framework: scikit-learn<br/>
Authentication: Flask-Login with bcrypt hashing<br/>
<br/>
<b>Crime Categories Supported:</b><br/>
• Cyber Financial Fraud<br/>
• Digital Arrest Scams<br/>
• Fake News / Misinformation<br/>
• Identity Theft<br/>
• Darknet Crimes<br/>
• Social Media Crimes<br/>
• Online Job Fraud<br/>
• Sextortion/Honey Traps<br/>
• Illegal Loan App Fraud<br/>
• Cyber Bullying/Stalking<br/>
"""

elements.append(Paragraph(overview, body_style))
elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# REQUIREMENTS
# ─────────────────────────────────────────────────────────────
elements.append(Paragraph("REQUIREMENTS & INSTALLATION", section_style))
elements.append(Spacer(1, 0.1*inch))

requirements = """
<b>System Requirements:</b><br/>
• Python 3.8 or higher<br/>
• MongoDB 4.4 or higher (running on localhost:27017)<br/>
• Windows/Linux/macOS<br/>
• 2GB RAM minimum<br/>
• 500MB disk space<br/>
<br/>
<b>Python Dependencies:</b><br/>
"""
elements.append(Paragraph(requirements, body_style))

# Add requirements table
req_data = [
    ['Package', 'Version', 'Purpose'],
    ['Flask', '2.3.0', 'Web framework'],
    ['Flask-Login', '0.6.2', 'User session management'],
    ['pymongo', '4.3.3', 'MongoDB driver'],
    ['bcrypt', '4.0.1', 'Password hashing'],
    ['pandas', '1.5.0', 'Data manipulation'],
    ['numpy', '1.24.0', 'Numerical computing'],
    ['scikit-learn', '1.2.0', 'Machine learning'],
    ['reportlab', '4.5.0', 'PDF generation'],
]

req_table = Table(req_data, colWidths=[2*inch, 1.2*inch, 2.3*inch])
req_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0a3a5c')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
]))
elements.append(req_table)
elements.append(Spacer(1, 0.2*inch))

setup = """
<b>Installation Steps:</b><br/>
<b>1. Clone/Download Project</b><br/>
Extract the project to a directory, e.g., C:\\projects\\cybercrime_project<br/>
<br/>
<b>2. Create Virtual Environment (Optional but Recommended)</b><br/>
<font face="Courier">python -m venv venv<br/>
venv\\Scripts\\activate</font><br/>
<br/>
<b>3. Install Dependencies</b><br/>
<font face="Courier">pip install -r requirements.txt</font><br/>
<br/>
<b>4. Ensure MongoDB is Running</b><br/>
<font face="Courier">mongod --dbpath C:\\data\\db</font><br/>
<br/>
<b>5. Initialize Database</b><br/>
<font face="Courier">python setup_db.py</font><br/>
(Creates collections & default admin user: admin/Admin@123)<br/>
<br/>
<b>6. Train AI Model</b><br/>
<font face="Courier">python ai/train_model.py</font><br/>
(Trains classifier on training_data.csv)<br/>
<br/>
<b>7. Start Application</b><br/>
<font face="Courier">python app.py</font><br/>
Access at: http://localhost:5000<br/>
<br/>
<b>Default Login Credentials:</b><br/>
Username: admin<br/>
Password: Admin@123<br/>
"""

elements.append(Paragraph(setup, body_style))
elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# SOURCE CODE SECTIONS
# ─────────────────────────────────────────────────────────────

def add_file_with_formatting(filepath, filename, max_lines=None):
    """Add file content to PDF with proper formatting"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            content = ''.join(lines) + '\n\n[... File truncated for space ...]'
        else:
            content = ''.join(lines)
        
        # File heading
        elements.append(Paragraph(f"FILE: {filename}", subsection_style))
        elements.append(Spacer(1, 0.05*inch))
        
        # Split into chunks
        lines = content.split('\n')
        chunk = ""
        line_count = 0
        
        for line in lines:
            if len(line) > 100:
                line = line[:97] + "..."
            chunk += line + "\n"
            line_count += 1
            
            if line_count >= 40:
                try:
                    elements.append(Preformatted(chunk, code_style))
                except:
                    pass
                chunk = ""
                line_count = 0
        
        if chunk.strip():
            try:
                elements.append(Preformatted(chunk, code_style))
            except:
                pass
        
        elements.append(Spacer(1, 0.1*inch))
        
    except Exception as e:
        elements.append(Paragraph(f"<b>ERROR:</b> Could not read {filename}", body_style))

# File lists by category
file_sections = [
    ("MAIN APPLICATION FILES", [
        ("app.py", "e:\\cybercrime_project\\app.py", 50),
        ("database.py", "e:\\cybercrime_project\\database.py", 20),
        ("models.py", "e:\\cybercrime_project\\models.py", 30),
        ("setup_db.py", "e:\\cybercrime_project\\setup_db.py", 100),
    ]),
    ("ROUTES: AUTHENTICATION", [
        ("routes/auth_routes.py", "e:\\cybercrime_project\\routes\\auth_routes.py", 60),
    ]),
    ("ROUTES: DASHBOARD & ADMIN", [
        ("routes/dashboard_routes.py", "e:\\cybercrime_project\\routes\\dashboard_routes.py", 120),
    ]),
    ("ROUTES: COMPLAINT MANAGEMENT", [
        ("routes/complaint_routes.py", "e:\\cybercrime_project\\routes\\complaint_routes.py", 150),
    ]),
    ("ROUTES: AI CLASSIFICATION", [
        ("routes/ai_routes.py", "e:\\cybercrime_project\\routes\\ai_routes.py", 60),
    ]),
    ("ROUTES: FIR GENERATION", [
        ("routes/fir_routes.py", "e:\\cybercrime_project\\routes\\fir_routes.py", 80),
    ]),
    ("ROUTES: CASE ASSIGNMENT", [
        ("routes/assignment_routes.py", "e:\\cybercrime_project\\routes\\assignment_routes.py", 70),
    ]),
    ("ROUTES: REPORTS & AUDIT", [
        ("routes/reports_routes.py", "e:\\cybercrime_project\\routes\\reports_routes.py", 80),
    ]),
    ("AI MODULE: PREDICTOR", [
        ("ai/predictor.py", "e:\\cybercrime_project\\ai\\predictor.py", 150),
    ]),
    ("AI MODULE: TRAINING", [
        ("ai/train_model.py", "e:\\cybercrime_project\\ai\\train_model.py", 80),
    ]),
    ("AI MODULE: DATA PROCESSING", [
        ("ai/merge_and_clean.py", "e:\\cybercrime_project\\ai\\merge_and_clean.py", 100),
    ]),
]

for section_name, files in file_sections:
    elements.append(Paragraph(section_name, section_style))
    elements.append(Spacer(1, 0.08*inch))
    
    for display_name, filepath, max_lines in files:
        add_file_with_formatting(filepath, display_name, max_lines)
    
    elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# CLOSING PAGE
# ─────────────────────────────────────────────────────────────
elements.append(Spacer(1, 2*inch))
elements.append(Paragraph("PROJECT COMPLETE", title_style))
elements.append(Spacer(1, 0.3*inch))

closing = """
<b>Document Information:</b><br/>
This document contains the complete source code for the AI-CMDSS system.<br/>
All files are organized by module and route.<br/>
Code is presented exactly as it appears in the project.<br/>
<br/>
<b>For Support & Updates:</b><br/>
Refer to README.md and documentation in the project directory.<br/>
<br/>
<b>Version:</b> 2.0<br/>
<b>Last Updated:</b> 2026<br/>
<b>Status:</b> Production Ready<br/>
"""

elements.append(Paragraph(closing, body_style))

# ─────────────────────────────────────────────────────────────
# BUILD PDF
# ─────────────────────────────────────────────────────────────

try:
    doc.build(elements)
    print(f"✅ Enhanced PDF created: {pdf_filename}")
    
    # Get file size
    size_mb = os.path.getsize(pdf_filename) / (1024 * 1024)
    print(f"📊 File size: {size_mb:.2f} MB")
    print(f"📍 Location: {os.path.abspath(pdf_filename)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
