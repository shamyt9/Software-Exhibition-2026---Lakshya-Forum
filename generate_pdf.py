"""
Generate a comprehensive PDF with all project code files
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from datetime import datetime
import os

# Create PDF
pdf_filename = "Cybercrime_Project_Documentation.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.75*inch, bottomMargin=0.5*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=6,
    alignment=1  # center
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2e5c8a'),
    spaceAfter=6,
    spaceBefore=10
)

file_heading_style = ParagraphStyle(
    'FileHeading',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#1f4788'),
    fontName='Courier-Bold',
    spaceAfter=3,
    spaceBefore=6,
    backColor=colors.HexColor('#e8f0f8')
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leftIndent=0.2*inch,
    rightIndent=0.2*inch,
    textColor=colors.HexColor('#333333'),
)

# ─────────────────────────────────────────────────────────────
# TITLE PAGE
# ─────────────────────────────────────────────────────────────
elements.append(Spacer(1, 1.5*inch))
elements.append(Paragraph("CYBERCRIME MANAGEMENT & DIGITAL INVESTIGATION SYSTEM", title_style))
elements.append(Paragraph("AI-CMDSS", title_style))
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("Complete Source Code Documentation", styles['Normal']))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# PROJECT STRUCTURE
# ─────────────────────────────────────────────────────────────
elements.append(Paragraph("PROJECT STRUCTURE", heading_style))
elements.append(Spacer(1, 0.1*inch))

structure_text = """
<b>Main Application Files:</b><br/>
• app.py - Flask main application<br/>
• database.py - MongoDB connection & collections<br/>
• models.py - User model with Flask-Login integration<br/>
• setup_db.py - Database initialization & sample data<br/>
<br/>
<b>Routes (Blueprint Modules):</b><br/>
• routes/auth_routes.py - Authentication (login/logout)<br/>
• routes/dashboard_routes.py - Dashboard & admin panel<br/>
• routes/complaint_routes.py - Complaint registration & management<br/>
• routes/ai_routes.py - AI classification & prediction results<br/>
• routes/fir_routes.py - FIR generation & management<br/>
• routes/assignment_routes.py - Case assignment to officers<br/>
• routes/reports_routes.py - Reports & audit logs<br/>
<br/>
<b>AI Module:</b><br/>
• ai/predictor.py - Crime classification using ML model<br/>
• ai/train_model.py - Model training with scikit-learn<br/>
• ai/merge_and_clean.py - Data preprocessing from CSV files<br/>
• ai/model/ - Trained model (classifier.pkl, vectorizer.pkl)<br/>
• ai/*.csv - Training data files (c1.csv - c7.csv)<br/>
<br/>
<b>Static & Templates:</b><br/>
• static/css/style.css - Styling<br/>
• static/js/ - JavaScript files<br/>
• templates/ - HTML templates for all pages<br/>
"""

elements.append(Paragraph(structure_text, styles['Normal']))
elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# REQUIREMENTS
# ─────────────────────────────────────────────────────────────
elements.append(Paragraph("REQUIREMENTS & DEPENDENCIES", heading_style))
elements.append(Spacer(1, 0.1*inch))

requirements_text = """
<b>Python Version:</b> 3.8+<br/>
<br/>
<b>Core Dependencies:</b><br/>
flask==2.3.0<br/>
flask-login==0.6.2<br/>
pymongo==4.3.3<br/>
bcrypt==4.0.1<br/>
pandas==1.5.0<br/>
scikit-learn==1.2.0<br/>
numpy==1.24.0<br/>
<br/>
<b>MongoDB Setup:</b><br/>
• MongoDB server running on localhost:27017<br/>
• Database name: aicmdss<br/>
• Collections auto-created by setup_db.py<br/>
<br/>
<b>Installation & Setup:</b><br/>
1. Create virtual environment (venv) - already exists in project<br/>
2. Install dependencies: pip install -r requirements_full.txt<br/>
3. Run setup: python setup_db.py<br/>
4. Train AI model: python ai/train_model.py<br/>
5. Start app: python app.py<br/>
6. Access at: http://localhost:5000<br/>
<br/>
<b>Default Credentials:</b><br/>
Username: admin<br/>
Password: Admin@123<br/>
Role: Administrator<br/>
"""

elements.append(Paragraph(requirements_text, styles['Normal']))
elements.append(PageBreak())

# ─────────────────────────────────────────────────────────────
# FILE LISTING WITH CODE
# ─────────────────────────────────────────────────────────────

files_to_include = [
    ("MAIN APPLICATION FILES", [
        ("app.py", "e:\\cybercrime_project\\app.py"),
        ("database.py", "e:\\cybercrime_project\\database.py"),
        ("models.py", "e:\\cybercrime_project\\models.py"),
        ("setup_db.py", "e:\\cybercrime_project\\setup_db.py"),
    ]),
    ("ROUTE: Authentication", [
        ("routes/auth_routes.py", "e:\\cybercrime_project\\routes\\auth_routes.py"),
    ]),
    ("ROUTE: Dashboard & Admin", [
        ("routes/dashboard_routes.py", "e:\\cybercrime_project\\routes\\dashboard_routes.py"),
    ]),
    ("ROUTE: Complaint Management", [
        ("routes/complaint_routes.py", "e:\\cybercrime_project\\routes\\complaint_routes.py"),
    ]),
    ("ROUTE: AI Classification", [
        ("routes/ai_routes.py", "e:\\cybercrime_project\\routes\\ai_routes.py"),
    ]),
    ("ROUTE: FIR Generation", [
        ("routes/fir_routes.py", "e:\\cybercrime_project\\routes\\fir_routes.py"),
    ]),
    ("ROUTE: Case Assignment", [
        ("routes/assignment_routes.py", "e:\\cybercrime_project\\routes\\assignment_routes.py"),
    ]),
    ("ROUTE: Reports & Audit", [
        ("routes/reports_routes.py", "e:\\cybercrime_project\\routes\\reports_routes.py"),
    ]),
    ("AI MODULE: Prediction", [
        ("ai/predictor.py", "e:\\cybercrime_project\\ai\\predictor.py"),
    ]),
    ("AI MODULE: Training", [
        ("ai/train_model.py", "e:\\cybercrime_project\\ai\\train_model.py"),
    ]),
    ("AI MODULE: Data Processing", [
        ("ai/merge_and_clean.py", "e:\\cybercrime_project\\ai\\merge_and_clean.py"),
    ]),
]

# Helper function to add file content
def add_file_content(filepath, filename):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Add file heading
        elements.append(Paragraph(f"FILE: {filename}", file_heading_style))
        elements.append(Spacer(1, 0.08*inch))
        
        # Add code - split into chunks to avoid overwhelming the document
        lines = content.split('\n')
        code_chunks = []
        current_chunk = ""
        
        for line in lines:
            # Limit line length for display
            if len(line) > 95:
                line = line[:92] + "..."
            
            current_chunk += line + "\n"
            
            # Create chunks of reasonable size
            if len(current_chunk.split('\n')) > 35:
                code_chunks.append(current_chunk)
                current_chunk = ""
        
        if current_chunk:
            code_chunks.append(current_chunk)
        
        # Add code chunks
        for chunk in code_chunks:
            try:
                elements.append(Preformatted(chunk, code_style))
            except:
                # Fallback for very long chunks
                elements.append(Paragraph(f"<pre>{chunk[:2000]}</pre>", code_style))
        
        elements.append(Spacer(1, 0.15*inch))
        elements.append(PageBreak())
        
    except Exception as e:
        elements.append(Paragraph(f"ERROR reading {filename}: {str(e)}", styles['Normal']))
        elements.append(PageBreak())

# Add all files
for section_name, files in files_to_include:
    elements.append(Paragraph(section_name, heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    for display_name, filepath in files:
        add_file_content(filepath, display_name)

# ─────────────────────────────────────────────────────────────
# BUILD PDF
# ─────────────────────────────────────────────────────────────

try:
    doc.build(elements)
    print(f"✅ PDF generated successfully: {pdf_filename}")
    print(f"📄 Total pages: {len(elements)} elements")
except Exception as e:
    print(f"❌ Error generating PDF: {e}")
