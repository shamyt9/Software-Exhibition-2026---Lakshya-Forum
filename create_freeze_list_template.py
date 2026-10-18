#!/usr/bin/env python3
"""Create clean freeze request list template"""

template = """{% extends "base.html" %}
{% block content %}
<div style="max-width: 1400px; margin: 0 auto; padding: 20px">
  <div style="margin-bottom: 30px">
    <h1 style="color: #0f172a; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;">❄️ TRANSACTION FREEZE REQUESTS</h1>
    <p style="color: #666; margin: 0; font-size: 14px;">Manage and track all financial fraud transaction blocking requests</p>
  </div>

  <!-- Stats Cards -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px; color: white;">
      <div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Total Requests</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 8px;">{{ total_count | default(0) }}</div>
    </div>
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; padding: 20px; color: white;">
      <div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Pending Approval</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 8px;">{{ pending_count | default(0) }}</div>
    </div>
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 12px; padding: 20px; color: white;">
      <div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Approved</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 8px;">{{ approved_count | default(0) }}</div>
    </div>
    <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 12px; padding: 20px; color: white;">
      <div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Completed</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 8px;">{{ completed_count | default(0) }}</div>
    </div>
  </div>

  <!-- Freeze Requests Table -->
  {% if freezes %}
  <div style="background: #1e293b; border-radius: 12px; overflow: hidden; margin-bottom: 24px;">
    <div style="padding: 20px; border-bottom: 1px solid #334155;">
      <h3 style="margin: 0; color: #f1f5f9; font-size: 16px; font-weight: 700;">📋 RECENT FREEZE REQUESTS</h3>
    </div>
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="border-bottom: 2px solid #334155; background: #0f172a;">
          <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Request ID</th>
          <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Complaint</th>
          <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Amount</th>
          <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Priority</th>
          <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Status</th>
          <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Date</th>
          <th style="padding: 12px 16px; text-align: center; font-weight: 600; color: #cbd5e1; font-size: 12px; text-transform: uppercase;">Action</th>
        </tr>
      </thead>
      <tbody>
        {% for freeze in freezes %}
        <tr style="border-bottom: 1px solid #334155; background: #1e293b; transition: background 0.2s;">
          <td style="padding: 14px 16px; color: #e2e8f0; font-weight: 600;">{{ freeze.freeze_request_id[:8] }}...</td>
          <td style="padding: 14px 16px; color: #e2e8f0;">{{ freeze.complaint_id }}</td>
          <td style="padding: 14px 16px; color: #fbbf24; font-weight: 600;">₹{{ freeze.amount_involved | default('—') }}</td>
          <td style="padding: 14px 16px;"><span style="background: {% if freeze.priority_score > 75 %}#dc2626{% elif freeze.priority_score > 50 %}#f59e0b{% else %}#10b981{% endif %}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">{% if freeze.priority_score > 75 %}URGENT{% elif freeze.priority_score > 50 %}HIGH{% else %}NORMAL{% endif %}</span></td>
          <td style="padding: 14px 16px;"><span style="background: {% if freeze.status == 'pending' %}#f59e0b{% elif freeze.status == 'approved' %}#3b82f6{% elif freeze.status == 'completed' %}#10b981{% else %}#6b7280{% endif %}; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;">{{ freeze.status | replace('_',' ') | title }}</span></td>
          <td style="padding: 14px 16px; color: #94a3b8; font-size: 13px;">{{ freeze.created_at.strftime('%d %b %Y') if freeze.created_at else '—' }}</td>
          <td style="padding: 14px 16px; text-align: center;"><a href="{{ url_for('freeze.view_freeze_request', freeze_id=freeze.freeze_request_id) }}" style="color: #3b82f6; text-decoration: none; font-weight: 600; padding: 6px 12px; border: 1px solid #3b82f6; border-radius: 6px; transition: all 0.2s;">View</a></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <div style="background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 40px; text-align: center;">
    <div style="font-size: 48px; margin-bottom: 16px;">❄️</div>
    <h3 style="color: #f1f5f9; font-size: 18px; font-weight: 700; margin: 0 0 8px 0;">No Freeze Requests Yet</h3>
    <p style="color: #94a3b8; margin: 0;">No transaction freeze requests have been created. Create a new one from a financial fraud complaint.</p>
  </div>
  {% endif %}

</div>
{% endblock %}
"""

with open("templates/freeze/list.html", "w", encoding="utf-8") as f:
    f.write(template)

print("✅ Freeze list template created!")
