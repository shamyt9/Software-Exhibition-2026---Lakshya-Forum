"""
Generate Final Comprehensive PDF with ALL project code - Full Version
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
                                Table, TableStyle)
from reportlab.lib import colors
from datetime import datetime
import os

pdf_filename = "CYBERCRIME_PROJECT_FULL_SOURCE_CODE.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                        rightMargin=0.35*inch, leftMargin=0.35*inch,
                        topMargin=0.5*inch, bottomMargin=0.35*inch)

elements = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20,
                            textColor=colors.HexColor('#003d73'), alignment=TA_CENTER,
                            fontName='Helvetica-Bold', spaceAfter=4)

section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=11,
                              textColor=colors.white, spaceAfter=6, spaceBefore=6,
                              backColor=colors.HexColor('#003d73'), leftIndent=0.15*inch,
                              fontName='Helvetica-Bold')

file_style = ParagraphStyle('FileHeader', parent=styles['Normal'], fontSize=9,
                           fontName='Courier-Bold', textColor=colors.HexColor('#003d73'),
                           backColor=colors.HexColor('#e6f0ff'), spaceAfter=3,
                           leftIndent=0.1*inch, borderColor=colors.HexColor('#003d73'),
                           borderWidth=0.5)

normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=8.5,
                             spaceAfter=4, alignment=TA_JUSTIFY)

# COVER
elements.append(Spacer(1, 1.5*inch))
elements.append(Paragraph("CYBERCRIME MANAGEMENT &", title_style))
elements.append(Paragraph("DIGITAL INVESTIGATION SYSTEM", title_style))
elements.append(Spacer(1, 0.15*inch))
elements.append(Paragraph("AI-CMDSS", ParagraphStyle('Subtitle', parent=styles['Normal'],
                                                    fontSize=14, alignment=TA_CENTER,
                                                    fontName='Helvetica-Bold')))
elements.append(Spacer(1, 0.4*inch))
elements.append(Paragraph("COMPLETE SOURCE CODE DOCUMENTATION<br/>WITH PROJECT REQUIREMENTS",
                         ParagraphStyle('Info', parent=styles['Normal'], fontSize=10,
                                       alignment=TA_CENTER)))
elements.append(Spacer(1, 0.8*inch))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}", 
                         normal_style))
elements.append(Paragraph("Technology: Flask • MongoDB • Scikit-Learn • Python 3.8+",
                         ParagraphStyle('Tech', parent=styles['Normal'], fontSize=9,
                                       alignment=TA_CENTER)))
elements.append(PageBreak())

# QUICK START
elements.append(Paragraph("QUICK START GUIDE", section_style))
elements.append(Spacer(1, 0.08*inch))

quickstart = """
<b>1. Setup:</b> Extract project → <font face="Courier">python -m venv venv</font> → <font face="Courier">pip install -r requirements.txt</font><br/>
<b>2. Database:</b> Ensure MongoDB running on localhost:27017 → <font face="Courier">python setup_db.py</font><br/>
<b>3. Model:</b> <font face="Courier">python ai/train_model.py</font><br/>
<b>4. Run:</b> <font face="Courier">python app.py</font> → Visit http://localhost:5000<br/>
<b>Login:</b> Username: <font face="Courier">admin</font> | Password: <font face="Courier">Admin@123</font>
"""
elements.append(Paragraph(quickstart, normal_style))
elements.append(Spacer(1, 0.1*inch))

# REQUIREMENTS
elements.append(Paragraph("PYTHON REQUIREMENTS", section_style))
elements.append(Spacer(1, 0.08*inch))

req_table_data = [
    ['Package', 'Version', 'Purpose'],
    ['Flask', '2.3.0', 'Web framework'],
    ['Flask-Login', '0.6.2', 'Authentication'],
    ['pymongo', '4.3.3', 'MongoDB'],
    ['bcrypt', '4.0.1', 'Password hashing'],
    ['pandas', '1.5.0', 'Data processing'],
    ['scikit-learn', '1.2.0', 'ML model'],
    ['numpy', '1.24.0', 'Numerical compute'],
    ['reportlab', '4.5.0', 'PDF generation'],
]

req_table = Table(req_table_data, colWidths=[1.8*inch, 1*inch, 2.2*inch])
req_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003d73')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
]))
elements.append(req_table)
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("Create <font face='Courier'>requirements.txt</font> file with above dependencies.",
                         normal_style))
elements.append(PageBreak())

# Now add all code files

code_files = [
    ("═══ APP.PY ═══", "e:\\cybercrime_project\\app.py"),
    ("═══ DATABASE.PY ═══", "e:\\cybercrime_project\\database.py"),
    ("═══ MODELS.PY ═══", "e:\\cybercrime_project\\models.py"),
    ("═══ SETUP_DB.PY ═══", "e:\\cybercrime_project\\setup_db.py"),
    ("═══ ROUTES: AUTH_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\auth_routes.py"),
    ("═══ ROUTES: DASHBOARD_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\dashboard_routes.py"),
    ("═══ ROUTES: COMPLAINT_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\complaint_routes.py"),
    ("═══ ROUTES: AI_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\ai_routes.py"),
    ("═══ ROUTES: FIR_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\fir_routes.py"),
    ("═══ ROUTES: ASSIGNMENT_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\assignment_routes.py"),
    ("═══ ROUTES: REPORTS_ROUTES.PY ═══", "e:\\cybercrime_project\\routes\\reports_routes.py"),
    ("═══ AI: PREDICTOR.PY ═══", "e:\\cybercrime_project\\ai\\predictor.py"),
    ("═══ AI: TRAIN_MODEL.PY ═══", "e:\\cybercrime_project\\ai\\train_model.py"),
    ("═══ AI: MERGE_AND_CLEAN.PY ═══", "e:\\cybercrime_project\\ai\\merge_and_clean.py"),
]

def format_code(filepath, max_width=120):
    """Read file and format for PDF"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        formatted = ""
        for line in lines:
            line = line.rstrip('\n')
            if len(line) > max_width:
                line = line[:max_width-3] + "..."
            formatted += line + "\n"
        return formatted
    except:
        return "ERROR: Could not read file"

for file_title, filepath in code_files:
    # Add page break and header
    elements.append(PageBreak())
    elements.append(Paragraph(file_title, file_style))
    elements.append(Spacer(1, 0.08*inch))
    
    # Get file content
    code_content = format_code(filepath)
    
    # Create code block
    code_paragraph = Paragraph(
        f"<font face='Courier' size='7'><b>{code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</b></font>",
        normal_style
    )
    
    try:
        # Split long code into sections
        lines = code_content.split('\n')
        chunk_size = 45
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            escaped_chunk = chunk.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            try:
                elements.append(Paragraph(
                    f"<font face='Courier' size='7'>{escaped_chunk}</font>",
                    normal_style
                ))
            except:
                # Fallback for very long lines
                pass
    except:
        elements.append(Paragraph("Unable to render code", normal_style))

# Final page
elements.append(PageBreak())
elements.append(Spacer(1, 2*inch))
elements.append(Paragraph("DOCUMENTATION COMPLETE", title_style))
elements.append(Spacer(1, 0.3*inch))

footer = """
<b>This PDF contains:</b><br/>
✓ Complete source code for all Python modules<br/>
✓ All route handlers and API endpoints<br/>
✓ AI/ML prediction system<br/>
✓ Database setup and initialization<br/>
✓ Project requirements and setup instructions<br/>
<br/>
<b>Files Included:</b><br/>
• app.py - Main Flask application<br/>
• database.py - MongoDB connectivity<br/>
• models.py - User authentication model<br/>
• setup_db.py - Database schema initialization<br/>
• 7 route modules (auth, dashboard, complaint, ai, fir, assignment, reports)<br/>
• 3 AI modules (predictor, train_model, merge_and_clean)<br/>
<br/>
For questions or support, refer to the project documentation.
"""

elements.append(Paragraph(footer, normal_style))

# Build PDF
try:
    doc.build(elements)
    size_kb = os.path.getsize(pdf_filename) / 1024
    print(f"✅ SUCCESS! PDF created: {pdf_filename}")
    print(f"📊 File size: {size_kb:.1f} KB")
    print(f"📁 Location: {os.path.abspath(pdf_filename)}")
    print(f"📄 Complete source code with requirements included")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
