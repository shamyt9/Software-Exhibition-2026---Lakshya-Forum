#!/usr/bin/env python3
"""Create clean freeze request generate and view templates"""

generate_template = """{% extends "base.html" %}
{% block content %}
<div style="max-width: 900px; margin: 0 auto; padding: 20px">
  <div style="margin-bottom: 30px">
    <h1 style="color: #0f172a; font-size: 28px; font-weight: 700; margin: 0 0 12px 0;">❄️ GENERATE TRANSACTION FREEZE REQUEST</h1>
    <p style="color: #666; font-size: 14px; margin: 0;">Create an urgent freeze request for this financial fraud complaint to be forwarded to the concerned bank and RBI.</p>
  </div>

  {% if not eligibility.eligible %}
  <div style="background: #fee2e2; border-left: 4px solid #dc2626; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
    <div style="display: flex; gap: 12px; align-items: flex-start;">
      <div style="font-size: 20px; margin-top: 2px;">⚠️</div>
      <div>
        <div style="color: #7f1d1d; font-weight: 600; margin-bottom: 4px;">Not Eligible for Freeze Request</div>
        <div style="color: #991b1b; font-size: 14px;">{{ eligibility.reason }}</div>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- Priority Metrics -->
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 24px; color: white; text-align: center;">
      <div style="font-size: 28px; font-weight: 800;">{{ priority_score }}</div>
      <div style="font-size: 12px; text-transform: uppercase; opacity: 0.9; margin-top: 4px;">Priority Score</div>
      <div style="font-size: 11px; opacity: 0.8; margin-top: 2px;">(out of 100)</div>
    </div>
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; padding: 24px; color: white; text-align: center;">
      <div style="font-size: 24px; font-weight: 800; color: #fbbf24;">₹ {% if transaction_amount %}{{ transaction_amount }}{% else %}—{% endif %}</div>
      <div style="font-size: 12px; text-transform: uppercase; opacity: 0.9; margin-top: 4px;">Amount Involved</div>
    </div>
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 12px; padding: 24px; color: white; text-align: center;">
      <div style="font-size: 24px; font-weight: 800;">{% if priority_score > 75 %}URGENT{% elif priority_score > 50 %}HIGH{% else %}NORMAL{% endif %}</div>
      <div style="font-size: 12px; text-transform: uppercase; opacity: 0.9; margin-top: 4px;">Priority Level</div>
    </div>
  </div>

  <!-- Complaint and Form Section -->
  <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 24px; margin-bottom: 24px;">
    <!-- Complaint Summary -->
    <div>
      <div style="background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
        <h3 style="margin: 0 0 16px 0; color: #f1f5f9; font-size: 14px; font-weight: 700; text-transform: uppercase;">📋 COMPLAINT SUMMARY</h3>
        <div style="space-y: 12px;">
          <div style="margin-bottom: 14px;">
            <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">Complaint ID</div>
            <p style="margin: 0; color: #e2e8f0; font-weight: 600;">{{ complaint_id }}</p>
          </div>
          <div style="margin-bottom: 14px;">
            <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">Complainant Name</div>
            <p style="margin: 0; color: #e2e8f0;">{{ complainant_name }}</p>
          </div>
          <div style="margin-bottom: 14px;">
            <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">District</div>
            <p style="margin: 0; color: #e2e8f0;">{{ district }}</p>
          </div>
          <div style="margin-bottom: 14px;">
            <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">Mobile Number</div>
            <p style="margin: 0; color: #e2e8f0;">{{ mobile }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Transaction Form -->
    <div>
      <div style="background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
        <h3 style="margin: 0 0 16px 0; color: #f1f5f9; font-size: 14px; font-weight: 700; text-transform: uppercase;">💳 TRANSACTION DETAILS</h3>
        <p style="margin: 0 0 16px 0; color: #94a3b8; font-size: 13px;">Enter transaction details (required for freeze request)</p>
        <form method="POST" style="space-y: 12px;">
          <div style="margin-bottom: 14px;">
            <label style="display: block; color: #cbd5e1; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase;">Transaction ID / UTR <span style="color: #f87171;">*</span></label>
            <input type="text" name="transaction_id" placeholder="Enter transaction ID or UTR" required style="width: 100%; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;" />
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
            <div>
              <label style="display: block; color: #cbd5e1; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase;">Bank Name <span style="color: #f87171;">*</span></label>
              <input type="text" name="bank_name" placeholder="e.g., ICICI Bank, HDFC Bank" required style="width: 100%; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;" />
            </div>
            <div>
              <label style="display: block; color: #cbd5e1; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase;">Amount <span style="color: #f87171;">*</span></label>
              <input type="number" name="amount" placeholder="Amount in INR" required style="width: 100%; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;" />
            </div>
          </div>
          <div style="margin-bottom: 14px;">
            <label style="display: block; color: #cbd5e1; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase;">Beneficiary Account Number</label>
            <input type="text" name="beneficiary_account" placeholder="Account number (masked format)" style="width: 100%; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;" />
          </div>
          <div style="margin-bottom: 16px;">
            <label style="display: block; color: #cbd5e1; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase;">Beneficiary Name</label>
            <input type="text" name="beneficiary_name" placeholder="Account holder name" style="width: 100%; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;" />
          </div>
          <div style="margin-bottom: 16px;">
            <label style="display: block; color: #cbd5e1; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase;">Additional Notes (Optional)</label>
            <textarea name="notes" placeholder="Any additional information for the bank" style="width: 100%; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit; min-height: 80px; resize: vertical;"></textarea>
          </div>
          <div style="display: flex; gap: 12px;">
            <button type="submit" style="flex: 1; padding: 12px; background: #3b82f6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px; text-transform: uppercase;">✓ Generate Freeze Request</button>
            <a href="{{ url_for('complaint.view_complaint', cmp_id=complaint_id) }}" style="flex: 1; padding: 12px; background: #374151; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px; text-transform: uppercase; text-align: center; text-decoration: none;">← Cancel</a>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Info Boxes -->
  <div style="display: grid; gap: 16px;">
    <!-- Important Notice -->
    <div style="background: #fef3c7; border-left: 4px solid #d97706; border-radius: 8px; padding: 16px;">
      <h4 style="margin: 0 0 8px 0; color: #92400e; display: flex; gap: 8px; align-items: center; font-size: 14px; font-weight: 700;">⚠️ Important Notice</h4>
      <p style="margin: 0; color: #b45309; font-size: 13px; line-height: 1.5;">This freeze request will be forwarded to the concerned bank's nodal officer for immediate action. Banks are expected to freeze the transaction within 24-48 hours as per RBI guidelines. Ensure all transaction details are accurate before submitting.</p>
    </div>

    <!-- RBI Guidelines -->
    <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px;">
      <h4 style="margin: 0 0 8px 0; color: #f1f5f9; font-size: 14px; font-weight: 700;">📋 RBI GUIDELINES &amp; LEGAL BASIS</h4>
      <ul style="margin: 0; padding-left: 20px; color: #cbd5e1; font-size: 13px;">
        <li style="margin-bottom: 4px;">Section 8 of RBI Cyber Security Framework</li>
        <li style="margin-bottom: 4px;">RBI Guidelines on Regulation of Payment Systems (2023)</li>
        <li style="margin-bottom: 4px;">Sections 66C, 66D of IT Act, 2000</li>
        <li style="margin-bottom: 4px;">Section 420, 406 of Indian Penal Code</li>
        <li>Urgent Action Protocols for Financial Fraud</li>
      </ul>
    </div>

    <!-- Time Sensitivity -->
    <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px;">
      <h4 style="margin: 0 0 8px 0; color: #f1f5f9; font-size: 14px; font-weight: 700;">⏰ TIME SENSITIVITY</h4>
      <div style="space-y: 8px; color: #cbd5e1; font-size: 13px;">
        <p style="margin: 0 0 6px 0;"><strong>24-48 Hours:</strong> Bank freezes the account/transaction</p>
        <p style="margin: 0 0 6px 0;"><strong>48-72 Hours:</strong> Bank may release held funds pending investigation</p>
        <p style="margin: 0;"><strong>After 7 Days:</strong> FIR registration becomes mandatory for sustained freeze</p>
      </div>
    </div>
  </div>
</div>
{% endblock %}
"""

view_template = """{% extends "base.html" %}
{% block content %}
<div style="max-width: 1000px; margin: 0 auto; padding: 20px">
  <!-- Header with Back Button -->
  <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-start;">
    <div>
      <h1 style="color: #0f172a; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;">❄️ TRANSACTION FREEZE REQUEST</h1>
      <p style="color: #666; font-size: 14px; margin: 0;">Request ID: {{ freeze.freeze_request_id[:12] }}...</p>
    </div>
    <a href="{{ url_for('freeze.list_freeze_requests') }}" style="color: #3b82f6; text-decoration: none; font-weight: 600;">← Back to Freeze Requests</a>
  </div>

  <!-- Status Badges -->
  <div style="display: flex; gap: 12px; margin-bottom: 24px;">
    <span style="background: {% if freeze.status == 'pending' %}#f59e0b{% elif freeze.status == 'approved' %}#10b981{% else %}#6b7280{% endif %}; color: white; padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 13px;">{{ freeze.status | replace('_', ' ') | title }}</span>
    <span style="background: {% if freeze.priority_score > 75 %}#dc2626{% elif freeze.priority_score > 50 %}#f59e0b{% else %}#10b981{% endif %}; color: white; padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 13px;">{% if freeze.priority_score > 75 %}🔴 URGENT{% elif freeze.priority_score > 50 %}🟠 HIGH{% else %}🟢 NORMAL{% endif %}</span>
    <span style="background: #667eea; color: white; padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 13px;">Score: {{ freeze.priority_score }}/100</span>
  </div>

  <!-- Download Buttons -->
  <div style="display: flex; gap: 12px; margin-bottom: 24px;">
    <a href="{{ url_for('freeze.download_freeze', freeze_id=freeze.freeze_request_id, format='pdf') }}" style="padding: 10px 16px; background: #dc2626; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-flex; gap: 6px; align-items: center;">📄 Download PDF</a>
    <a href="{{ url_for('freeze.download_freeze', freeze_id=freeze.freeze_request_id, format='json') }}" style="padding: 10px 16px; background: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-flex; gap: 6px; align-items: center;">📋 Export JSON</a>
  </div>

  <!-- Main Content Grid -->
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
    <!-- Transaction Details -->
    <div style="background: #fffbeb; border: 1px solid #fed7aa; border-radius: 12px; padding: 20px;">
      <h3 style="margin: 0 0 16px 0; color: #92400e; font-size: 14px; font-weight: 700; text-transform: uppercase;">💳 TRANSACTION DETAILS</h3>
      <div style="space-y: 12px;">
        <div style="margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Transaction ID / UTR</div>
          <p style="margin: 0; color: #92400e; font-weight: 600;">{{ freeze.transaction_id }}</p>
        </div>
        <div style="margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Bank Name</div>
          <p style="margin: 0; color: #92400e;">{{ freeze.bank_name }}</p>
        </div>
        <div style="margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Amount Involved</div>
          <p style="margin: 0; color: #d97706; font-size: 18px; font-weight: 800;">₹{{ freeze.amount_involved }}</p>
        </div>
        <div style="margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Beneficiary Account</div>
          <p style="margin: 0; color: #92400e;">{{ freeze.beneficiary_account | default('Not provided') }}</p>
        </div>
        <div>
          <div style="color: #b45309; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Beneficiary Name</div>
          <p style="margin: 0; color: #92400e;">{{ freeze.beneficiary_name | default('Not provided') }}</p>
        </div>
      </div>
    </div>

    <!-- Complainant Info -->
    <div style="background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
      <h3 style="margin: 0 0 16px 0; color: #f1f5f9; font-size: 14px; font-weight: 700; text-transform: uppercase;">👤 COMPLAINANT INFORMATION</h3>
      <div style="space-y: 12px;">
        <div style="margin-bottom: 12px;">
          <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Name</div>
          <p style="margin: 0; color: #e2e8f0;">{{ complaint.complainant_name | default('Not provided') }}</p>
        </div>
        <div style="margin-bottom: 12px;">
          <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">District</div>
          <p style="margin: 0; color: #e2e8f0;">{{ complaint.district | default('Not provided') }}</p>
        </div>
        <div style="margin-bottom: 12px;">
          <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Mobile</div>
          <p style="margin: 0; color: #e2e8f0;">{{ complaint.mobile | default('Not provided') }}</p>
        </div>
        <div style="margin-bottom: 12px;">
          <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Email</div>
          <p style="margin: 0; color: #e2e8f0;">{{ complaint.email | default('Not provided') }}</p>
        </div>
        <div>
          <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Complaint ID</div>
          <p style="margin: 0; color: #3b82f6; font-weight: 600;">{{ freeze.complaint_id }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Status Update Form -->
  {% if current_user.role in ['admin', 'supervisor', 'sp'] %}
  <div style="background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
    <h3 style="margin: 0 0 16px 0; color: #f1f5f9; font-size: 14px; font-weight: 700; text-transform: uppercase;">⚙️ UPDATE STATUS</h3>
    <form method="POST" action="{{ url_for('freeze.update_freeze_status', freeze_id=freeze.freeze_request_id) }}" style="display: flex; gap: 12px;">
      <select name="status" style="flex: 1; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;">
        <option value="pending" {% if freeze.status == 'pending' %}selected{% endif %}>📋 Pending Approval</option>
        <option value="approved" {% if freeze.status == 'approved' %}selected{% endif %}>✅ Approved</option>
        <option value="sent_to_bank" {% if freeze.status == 'sent_to_bank' %}selected{% endif %}>📤 Sent to Bank</option>
        <option value="bank_confirmed" {% if freeze.status == 'bank_confirmed' %}selected{% endif %}>🏦 Bank Confirmed</option>
        <option value="completed" {% if freeze.status == 'completed' %}selected{% endif %}>✓ Completed</option>
        <option value="rejected" {% if freeze.status == 'rejected' %}selected{% endif %}>❌ Rejected</option>
      </select>
      <input type="text" name="notes" placeholder="Optional status notes..." style="flex: 1; padding: 10px 12px; background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #e2e8f0; font-family: inherit;" />
      <button type="submit" style="padding: 10px 24px; background: #3b82f6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer;">✓ Update</button>
    </form>
  </div>
  {% endif %}

  <!-- Legal References -->
  <div style="background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
    <h4 style="margin: 0 0 12px 0; color: #f1f5f9; font-size: 13px; font-weight: 700; text-transform: uppercase;">📜 LEGAL BASIS &amp; RBI GUIDELINES</h4>
    <ul style="margin: 0; padding-left: 20px; color: #cbd5e1; font-size: 12px; line-height: 1.6;">
      <li>Section 8 of RBI Cyber Security Framework</li>
      <li>RBI Guidelines on Regulation of Payment Systems (2023)</li>
      <li>Sections 66C, 66D of IT Act, 2000 (Identity Theft)</li>
      <li>Section 420, 406 of Indian Penal Code (Cheating, Criminal Breach of Trust)</li>
      <li>Urgent Action Protocols for Financial Fraud Prevention</li>
    </ul>
  </div>
</div>
{% endblock %}
"""

with open("templates/freeze/generate.html", "w", encoding="utf-8") as f:
    f.write(generate_template)
with open("templates/freeze/view.html", "w", encoding="utf-8") as f:
    f.write(view_template)

print("✅ Freeze generate and view templates created!")
