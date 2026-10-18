# Transaction Blocking / Freeze Request Feature

## Overview

The AI-Assisted Transaction Blocking feature enables police officers to automatically generate and manage urgent freeze requests for financial fraud complaints. This system integrates with RBI guidelines and banking regulations to ensure rapid response to cybercrime incidents involving financial fraud.

## Key Features

### 1. **Automatic Eligibility Detection**

- Automatically identifies financial fraud complaints (various fraud categories)
- Validates minimum amount threshold (₹10,000)
- Checks for transaction details availability
- Provides clear eligibility messages if case doesn't qualify

### 2. **Smart Priority Scoring**

Calculates priority scores (0-100) based on:

- **Amount Factor (40 points)**: Higher amounts = higher priority
- **Time Decay Factor (30 points)**: Recent transactions get higher priority
- **Risk Level Factor (30 points)**: HIGH risk > MEDIUM > LOW
- **Result**: URGENT (>75), HIGH (>50), or NORMAL (<50)

### 3. **Comprehensive Freeze Request Generation**

Automatically collects and organizes:

- **Complainant Details**: Name, mobile, district
- **Transaction Details**: Transaction ID/UTR, Bank, Amount, Beneficiary, Timestamp
- **Crime Classification**: Category, Risk Level, Legal Sections
- **RBI Compliance**: Guidelines, legal references, temporal requirements

### 4. **Multiple Export Formats**

- **PDF Download**: Professional freeze request letter ready for bank submission
- **JSON Export**: Machine-readable format for API integration with banking systems

### 5. **Status Tracking**

- Track freeze request lifecycle (Pending → Approved/Rejected → Completed)
- Record bank responses and actions
- Maintain audit trail of all updates
- Full status history for accountability

### 6. **Advanced Filtering & Search**

- Filter by Status, Priority, District, Bank, Date Range
- Comprehensive list view with pagination
- Dashboard statistics and trends

## How to Use

### Step 1: Generate a Freeze Request

1. **Navigate to Complaint Details**
    - Go to Complaints → Select a complaint
    - If it's a financial fraud case, you'll see the "❄️ Request Freeze" button

2. **Click "Request Freeze" Button**
    - Button only appears for:
        - Financial fraud complaints (AI-classified)
        - Authorized users (Admin, Supervisor, SP, CCI, IO)

3. **Fill Transaction Details**
    - **Transaction ID/UTR** (Required): Unique identifier from the bank
    - **Bank Name** (Required): Name of the bank involved
    - **Amount** (Auto-filled from complaint, editable): Transaction amount
    - **Beneficiary Account** (Optional): Account number in masked format
    - **Beneficiary Name** (Optional): Account holder's name
    - **Additional Notes** (Optional): Any extra information for the bank

4. **Review Priority Assessment**
    - System shows:
        - Priority Score (0-100)
        - Priority Level (URGENT/HIGH/NORMAL)
        - Amount involved
        - Risk indicators

### Step 2: Download & Share with Bank

1. **View Freeze Request**
    - After generation, you'll see the freeze request details page
    - Download options are prominently displayed

2. **Choose Download Format**
    - **📄 Download PDF**:
        - Professional letter format
        - Includes legal sections and RBI guidelines
        - Print-ready for bank submission
        - Contains bank nodal officer instructions
    - **📋 Copy JSON**:
        - Machine-readable structured data
        - For API integration with banking systems
        - Contains complete transaction details

3. **Forward to Bank**
    - Email PDF to bank's nodal officer
    - Reference: Email template available in system
    - RBI expects action within 24-48 hours

### Step 3: Track Status & Bank Response

1. **Monitor Freeze Request Status**
    - Navigate to ❄️ Freeze Requests in main menu
    - View all freeze requests with current status
    - Filter by Status, Priority, District, or Bank

2. **Update Status**
    - Change status from Pending to Approved/Completed
    - Add notes for each status update
    - Full history maintained automatically

3. **Record Bank Response**
    - Enter bank reference number
    - Record bank's response (Approved/Processing/Rejected)
    - Add response notes for documentation

## Legal & Compliance Framework

### Applicable Legal Sections

- **66C IT Act**: Identity theft
- **66D IT Act**: Cheating through electronic means
- **420 IPC**: Cheating and dishonestly inducing delivery of property
- **406 IPC**: Criminal breach of trust
- **468/471 IPC**: Forgery for cheating

### RBI Guidelines

- **Section 8, RBI Cyber Security Framework**: Fraud detection and transaction blocking
- **RBI Guidelines on Regulation of Payment Systems (2023)**: Transaction reversal procedures
- **RBI Cyber Fraud Alert**: Urgent blocking procedures

### Time Requirements

- **24-48 Hours**: Bank must freeze the transaction
- **48-72 Hours**: Bank may release pending investigation
- **7+ Days**: FIR registration becomes mandatory for sustained freeze

## Audit Logging

All freeze request activities are permanently logged:

- Request generation with details
- Status updates and changes
- Bank response recordings
- Download activities (PDF/JSON)
- Officer/user information

### Example Audit Log Entries

```
[Freeze Request Generated]
Officer: Inspector Rajesh Kumar
Complaint: CMP-2026-00145
Action: Generated freeze request FRZ-20260516-00145
Details: Financial fraud ₹ 50,000 | Priority: HIGH
Timestamp: 16-May-2026 14:30:45

[Bank Response Recorded]
Officer: Supervisor Priya Singh
Freeze Request: FRZ-20260516-00145
Action: Bank response recorded
Details: Frozen | Reference: BNK-STB-2026001234
Timestamp: 17-May-2026 08:15:22
```

## User Roles & Permissions

### Authorized to Create Freeze Requests

- **Admin**: Full access
- **Supervisor**: Full access
- **SP (Superintendent of Police)**: Full access
- **CCI (Cyber Crime Inspector)**: Full access
- **IO (Investigating Officer)**: Full access

### Viewing Access

- Same roles can view all freeze requests
- Filter and search capabilities
- Access to download history

## Technical Details

### Database Collections

- **freeze_requests**: Stores all freeze request records
- **audit_logs**: Permanent record of all activities
- **complaints**: Updated with freeze_request_id reference
- **predictions**: AI classification data linked to freeze request

### Data Structure

```python
{
    "freeze_request_id": "FRZ-20260516-12345",
    "complaint_id": "CMP-2026-00145",

    # Complainant
    "complainant_name": "John Doe",
    "complainant_mobile": "+919876543210",
    "complainant_district": "Agra",

    # Transaction Details
    "transaction_id": "TXN123456789",
    "bank_name": "ICICI Bank",
    "amount_involved": 50000,
    "beneficiary_account": "XXXXX7890",
    "beneficiary_name": "Unknown Account",

    # Scoring
    "priority_score": 72,
    "priority_level": "HIGH",
    "risk_score": 85,
    "risk_level": "HIGH",

    # Status
    "status": "approved",
    "status_history": [...],
    "bank_response": "FROZEN",
    "bank_reference_id": "BNK-STB-2026001234",

    # Metadata
    "requested_by_officer_name": "Inspector Rajesh",
    "request_timestamp": "2026-05-16T14:30:45",
    "applicable_sections": ["66C IT Act", "420 IPC"]
}
```

## Best Practices

### 1. **Accuracy of Transaction Details**

- Verify transaction ID/UTR from official bank documents
- Ensure bank name is spelled correctly (affects routing)
- Double-check beneficiary account number
- Document transaction timestamp accurately

### 2. **Timely Action**

- Generate freeze requests within hours of complaint registration
- High-priority cases should be forwarded immediately
- Follow up with bank if no response within 24 hours

### 3. **Documentation**

- Keep PDF copies of all freeze requests
- Record bank responses with reference numbers
- Maintain correspondence logs
- Cross-reference with FIR registration

### 4. **Compliance**

- Ensure all legal sections are correctly referenced
- RBI guidelines must be mentioned in all communications
- Maintain audit trail integrity
- Document any rejections or delays

## Troubleshooting

### Issue: "Not Eligible for Freeze Request"

**Cause**: Case is not classified as financial fraud or amount is below ₹10,000
**Solution**:

- Verify AI classification (re-run if needed)
- Ensure amount_involved field is populated correctly
- Contact system admin if case should be eligible

### Issue: Transaction Details Missing

**Cause**: Transaction record not in system
**Solution**:

- Use "Manual Entry" option to enter transaction details
- Verify details from complainant or bank statement
- System will still generate freeze request

### Issue: PDF Download Fails

**Cause**: Server configuration or missing dependencies
**Solution**:

- Try JSON export instead
- Check server logs for errors
- Verify reportlab library is installed

### Issue: Freeze Request Not Saved

**Cause**: Database connection or validation error
**Solution**:

- Check all required fields (marked with \*)
- Verify internet connection
- Retry operation
- Contact system administrator

## FAQ

**Q: Can I modify a freeze request after generation?**
A: No, but you can update its status and record bank responses. For different transaction details, generate a new freeze request.

**Q: How long does the bank have to freeze?**
A: RBI guidelines require freezing within 24-48 hours of receiving the request.

**Q: What if the beneficiary account is unknown?**
A: Leave it blank or enter "Unknown". System will allow freezing on transaction ID/UTR basis.

**Q: Can I cancel a freeze request?**
A: Change status to "Rejected" with reason in notes. The original record remains for audit trail.

**Q: Who should I contact if bank doesn't respond?**
A: Escalate to bank's nodal officer or RBI's Cyber Security Centre with freeze request reference.

**Q: Is there a batch freeze request feature?**
A: Not in current version. Generate individual freeze requests per complaint.

**Q: How is audit trail protected?**
A: All logs are marked "permanent" and cannot be deleted, only viewed for compliance.

## Support & Resources

- **System Administrator**: Contact IT department for technical issues
- **Legal Advisor**: Verify applicable sections with legal team
- **RBI Reference**: Visit [rbi.org.in](https://rbi.org.in) for updated guidelines
- **Bank Nodal Officer**: Contact information usually in complaint details

---

**Last Updated**: May 2026  
**Feature Version**: 1.0  
**Status**: Production Ready
