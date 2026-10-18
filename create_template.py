#!/usr/bin/env python3
"""Create a clean, properly formatted complaint view template"""

template_content = """{% extends "base.html" %}
{% block content %}
<div style="max-width: 1200px; margin: 0 auto; padding: 20px">
  <!-- Header Section -->
  <div style="margin-bottom: 30px">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
      <div>
        <h1 style="color: #0f172a; font-size: 28px; font-weight: 800; margin: 0 0 12px 0;">📋 {{ complaint.complaint_id }}</h1>
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <span class="badge badge-{{ complaint.status }}">{{ complaint.status | replace('_',' ') | upper }}</span>
          {% if complaint.risk_level %}<span class="badge badge-{{ complaint.risk_level | lower }}">⚠️ RISK: {{ complaint.risk_level }}</span>{% endif %}
          {% if complaint.crime_type and complaint.crime_type != 'pending_ai' %}<span style="background: #e0e7ff; color: #1e40af; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;">🏷️ {{ complaint.crime_type | replace('_',' ') | title }}</span>{% endif %}
        </div>
      </div>
      <a href="{{ url_for('complaint.list_complaints') }}" style="color: #3b82f6; text-decoration: none; font-weight: 600; padding: 10px 20px; border: 2px solid #3b82f6; border-radius: 10px; transition: all 0.2s;">← Back to Complaints</a>
    </div>
  </div>

  <!-- AI CLASSIFICATION CARD -->
  {% if prediction %}
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 24px; margin-bottom: 24px; overflow: hidden; box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
      <div>
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px">
          <span style="background: rgba(255, 255, 255, 0.25); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">🤖 AI CLASSIFIED</span>
        </div>
        <div style="font-size: 24px; font-weight: 800; color: white; margin-bottom: 4px;">{{ prediction.category_label }}</div>
        <div style="opacity: 0.95; color: white; font-size: 13px;">Confidence: {{ (prediction.confidence * 100) | round(1) }}%</div>
      </div>
      <a href="{{ urls.ai_result }}" style="color: white; font-weight: 700; text-decoration: underline; padding: 12px 24px; background: rgba(255,255,255,0.15); border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.2s;">View Full Report →</a>
    </div>
  </div>
  {% endif %}

  <!-- COMPLAINANT INFO CARD -->
  <div class="detail-card" style="margin-bottom: 24px;">
    <div style="background: #0f172a; padding: 16px 20px; border-bottom: 2px solid #334155;"><h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">👤 COMPLAINANT INFORMATION</h3></div>
    <div style="padding: 20px">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;">
        {% if complaint.complainant_name %}<div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #3b82f6;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Name</div><div style="font-size: 15px; font-weight: 600;">{{ complaint.complainant_name }}</div></div>{% endif %}
        {% if complaint.email %}<div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #8b5cf6;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Email</div><div style="font-size: 14px; word-break: break-all;">{{ complaint.email }}</div></div>{% endif %}
        {% if complaint.phone %}<div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #06b6d4;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Phone</div><div style="font-size: 15px; font-weight: 600;">{{ complaint.phone }}</div></div>{% endif %}
        {% if complaint.district %}<div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #f59e0b;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">District</div><div style="font-size: 15px; font-weight: 600;">{{ complaint.district }}</div></div>{% endif %}
      </div>
    </div>
  </div>

  <!-- COMPLAINT DETAILS CARD -->
  <div class="detail-card" style="margin-bottom: 24px;">
    <div style="background: #0f172a; padding: 16px 20px; border-bottom: 2px solid #334155;"><h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">📝 COMPLAINT DETAILS</h3></div>
    <div style="padding: 20px">
      {% if complaint.description %}<div style="margin-bottom: 20px; background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #3b82f6;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Description</div><div style="line-height: 1.8; color: #e2e8f0; font-size: 14px;">{{ complaint.description }}</div></div>{% endif %}
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
        <div style="background: #0f172a; padding: 16px; border-radius: 8px;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Date Reported</div><div style="font-size: 15px; font-weight: 600;">{% if complaint.complaint_date %}{{ complaint.complaint_date.strftime('%d %b %Y') }}{% else %}Not provided{% endif %}</div></div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Current Status</div><div style="font-size: 15px; font-weight: 600;">{{ complaint.status | replace('_',' ') | title }}</div></div>
        {% if complaint.crime_type %}<div style="background: #0f172a; padding: 16px; border-radius: 8px;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Crime Type</div><div style="font-size: 15px; font-weight: 600;">{{ complaint.crime_type | replace('_',' ') | title }}</div></div>{% endif %}
      </div>
    </div>
  </div>

  <!-- RISK ASSESSMENT CARD -->
  {% if risk %}
  <div class="detail-card" style="margin-bottom: 24px;">
    <div style="background: #0f172a; padding: 16px 20px; border-bottom: 2px solid #334155;"><h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">⚠️ RISK ASSESSMENT</h3></div>
    <div style="padding: 20px">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid {% if risk.risk_level == 'HIGH' %}#dc2626{% elif risk.risk_level == 'MEDIUM' %}#f59e0b{% else %}#10b981{% endif %};"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Risk Level</div><div style="font-size: 18px; font-weight: 800;">{{ risk.risk_level }}</div></div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #3b82f6;"><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; font-weight: 600; margin-bottom: 8px;">Risk Score</div><div style="font-size: 24px; font-weight: 800;">{{ risk.risk_score | default(0) }}<span style="font-size: 12px; opacity: 0.6;">/100</span></div></div>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- TRANSACTION INFO CARD -->
  {% if transaction %}
  <div class="detail-card" style="margin-bottom: 24px;">
    <div style="background: #0f172a; padding: 16px 20px; border-bottom: 2px solid #334155;"><h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">💰 TRANSACTION DETAILS</h3></div>
    <div style="padding: 20px">
      <div style="background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #dc2626;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; color: #92400e;">
          {% if transaction.amount %}<div><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9; font-weight: 700; margin-bottom: 6px;">Amount</div><div style="font-size: 20px; font-weight: 800;">₹{{ transaction.amount }}</div></div>{% endif %}
          {% if transaction.utr %}<div><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9; font-weight: 700; margin-bottom: 6px;">UTR/Reference</div><div style="font-size: 13px; font-weight: 700; word-break: break-all;">{{ transaction.utr }}</div></div>{% endif %}
          {% if transaction.bank %}<div><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9; font-weight: 700; margin-bottom: 6px;">Bank</div><div style="font-size: 13px; font-weight: 700;">{{ transaction.bank }}</div></div>{% endif %}
          {% if transaction.beneficiary_account %}<div><div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9; font-weight: 700; margin-bottom: 6px;">Beneficiary Account</div><div style="font-size: 13px; font-weight: 700; word-break: break-all;">{{ transaction.beneficiary_account }}</div></div>{% endif %}
        </div>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- STATUS UPDATE CARD -->
  {% if current_user.role in ['admin', 'supervisor'] %}
  <div class="detail-card" style="margin-bottom: 24px;">
    <div style="background: #0f172a; padding: 16px 20px; border-bottom: 2px solid #334155;"><h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">⚙️ UPDATE STATUS</h3></div>
    <div style="padding: 20px">
      <form method="POST" action="{{ urls.update_status }}" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center;">
        <select name="status" style="flex: 1; min-width: 280px; padding: 12px 16px; border-radius: 8px; border: 1px solid #475569; background: #1e293b; color: #f1f5f9; font-weight: 500;">
          <option value="submitted" {% if complaint.status == 'submitted' %}selected{% endif %}>📋 SUBMITTED</option>
          <option value="classified" {% if complaint.status == 'classified' %}selected{% endif %}>🤖 CLASSIFIED</option>
          <option value="under_review" {% if complaint.status == 'under_review' %}selected{% endif %}>🔍 UNDER REVIEW</option>
          <option value="assigned" {% if complaint.status == 'assigned' %}selected{% endif %}>👮 ASSIGNED TO OFFICER</option>
          <option value="in_progress" {% if complaint.status == 'in_progress' %}selected{% endif %}>⚙️ IN PROGRESS</option>
          <option value="freeze_requested" {% if complaint.status == 'freeze_requested' %}selected{% endif %}>❄️ FREEZE REQUESTED</option>
          <option value="fir_drafted" {% if complaint.status == 'fir_drafted' %}selected{% endif %}>📄 FIR DRAFTED</option>
          <option value="fir_registered" {% if complaint.status == 'fir_registered' %}selected{% endif %}>✅ FIR REGISTERED</option>
          <option value="resolved" {% if complaint.status == 'resolved' %}selected{% endif %}>🎯 RESOLVED</option>
        </select>
        <button type="submit" class="btn-primary" style="padding: 12px 28px; font-weight: 700; border-radius: 8px;">✓ Update</button>
      </form>
    </div>
  </div>
  {% endif %}

  <!-- ACTION BUTTONS CARD -->
  <div class="detail-card" style="margin-bottom: 24px;">
    <div style="background: #0f172a; padding: 16px 20px; border-bottom: 2px solid #334155;"><h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">⚡ AVAILABLE ACTIONS</h3></div>
    <div style="padding: 20px">
      <div style="display: flex; gap: 12px; flex-wrap: wrap">
        <a href="{{ urls.ai_classify }}" style="padding: 11px 22px; border: 2px solid #38bdf8; border-radius: 8px; color: #38bdf8; text-decoration: none; font-weight: 600; transition: all 0.2s; background: rgba(56, 189, 248, 0.05);">🔄 Re-run AI</a>
        <a href="{{ urls.fir_view }}" style="padding: 11px 22px; background: #3b82f6; color: white; border-radius: 8px; text-decoration: none; font-weight: 600; transition: all 0.2s;">📄 Generate FIR</a>
        {% if current_user.role in ['admin', 'supervisor', 'sp', 'cci', 'io'] and prediction and ('fraud' in prediction.category.lower() or 'financial' in prediction.category.lower()) %}<a href="{{ urls.freeze_generate }}" style="padding: 11px 22px; background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; border-radius: 8px; text-decoration: none; font-weight: 600; transition: all 0.2s;">❄️ Request Freeze</a>{% endif %}
        {% if current_user.role in ['admin', 'supervisor'] %}<a href="{{ urls.assignment_assign }}" style="padding: 11px 22px; border: 2px solid #f59e0b; border-radius: 8px; color: #f59e0b; text-decoration: none; font-weight: 600; transition: all 0.2s; background: rgba(245, 158, 11, 0.05);">👮 Assign Officer</a>{% endif %}
        {% if current_user.role == 'admin' %}<a href="{{ urls.complaint_edit }}" style="padding: 11px 22px; border: 2px solid #a78bfa; border-radius: 8px; color: #a78bfa; text-decoration: none; font-weight: 600; transition: all 0.2s; background: rgba(167, 139, 250, 0.05);">✏️ Edit</a>{% endif %}
      </div>
    </div>
  </div>

</div>
{% endblock %}
"""

with open("templates/complaints/view.html", "w", encoding="utf-8") as f:
    f.write(template_content)

print("✅ Template created successfully!")

