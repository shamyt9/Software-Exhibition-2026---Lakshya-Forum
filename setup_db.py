from database import *
from datetime import datetime
import bcrypt

# ── 1. USERS ──────────────────────────────────────────────
# Create indexes so username/email must be unique
users_col.create_index("username", unique=True)
users_col.create_index("email", unique=True)

# Insert a default admin user
password = bcrypt.hashpw("Admin@123".encode(), bcrypt.gensalt())
users_col.insert_one({
    "username"   : "admin",
    "full_name"  : "System Admin",
    "email"      : "admin@upcyber.gov.in",
    "password"   : password,
    "role"       : "admin",          # admin / officer / supervisor / analyst
    "district"   : "Lucknow",
    "is_active"  : True,
    "created_at" : datetime.utcnow()
})

# ── 2. COMPLAINTS ─────────────────────────────────────────
# Create indexes for fast search
complaints_col.create_index("complaint_id", unique=True)
complaints_col.create_index("status")
complaints_col.create_index("district")
complaints_col.create_index("submitted_at")

# Sample complaint document shape (for reference):
sample_complaint = {
    "complaint_id"     : "CMP-2026-00001",
    "complainant_name" : "Ramesh Kumar",
    "mobile"           : "9876543210",
    "district"         : "Lucknow",
    "complaint_text"   : "I received a call from someone claiming to be SBI officer...",
    "amount_involved"  : 45000,
    "txn_id"           : "TXN123456789",
    "source"           : "NCRP",       # NCRP / walk-in / 1930
    "status"           : "submitted",  # submitted/classified/assigned/closed
    "assigned_to"      : None,         # officer user_id
    "submitted_at"     : datetime.utcnow(),
    "updated_at"       : datetime.utcnow()
}

# ── 3. TRANSACTIONS ───────────────────────────────────────
transactions_col.create_index("complaint_id")
transactions_col.create_index("txn_id")

# Sample shape:
sample_transaction = {
    "complaint_id"  : "CMP-2026-00001",
    "txn_id"        : "TXN123456789",
    "bank_name"     : "SBI",
    "account_masked": "XXXX1234",
    "utr_ref"       : "UTR987654",
    "amount"        : 45000,
    "txn_datetime"  : datetime.utcnow(),
    "channel"       : "UPI",          # UPI / NEFT / IMPS / card
    "beneficiary"   : "Unknown Acc"
}

# ── 4. AI_PREDICTIONS ─────────────────────────────────────
predictions_col.create_index("complaint_id")

sample_prediction = {
    "complaint_id"   : "CMP-2026-00001",
    "category"       : "cyber_financial_fraud",
    "confidence"     : 0.91,
    "model_version"  : "v1.0",
    "all_scores"     : {
        "cyber_financial_fraud" : 0.91,
        "digital_arrest_scam"   : 0.05,
        "phishing"              : 0.03,
        "fake_news"             : 0.01
    },
    "predicted_at"   : datetime.utcnow()
}

# ── 5. RISK_ASSESSMENTS ───────────────────────────────────
risks_col.create_index("complaint_id")

sample_risk = {
    "complaint_id"  : "CMP-2026-00001",
    "risk_score"    : 87.5,
    "risk_level"    : "HIGH",          # HIGH / MEDIUM / LOW
    "reason"        : "High amount + high confidence + severe category",
    "amount_band"   : "high",          # low <10k / medium 10k-1L / high >1L
    "assessed_at"   : datetime.utcnow()
}

# ── 6. FIRS ───────────────────────────────────────────────
firs_col.create_index("complaint_id")
firs_col.create_index("fir_number", unique=True, sparse=True)

sample_fir = {
    "complaint_id"     : "CMP-2026-00001",
    "fir_number"       : None,            # filled when FIR is registered
    "police_station"   : "Cyber Cell Lucknow",
    "sections"         : ["66C IT Act", "420 IPC", "66D IT Act"],
    "fir_text_draft"   : "On the complaint of Ramesh Kumar...",
    "status"           : "draft",         # draft / registered
    "created_by"       : "officer_id",
    "created_at"       : datetime.utcnow()
}

# ── 7. BANK_FREEZES ───────────────────────────────────────
freezes_col.create_index("complaint_id")

sample_freeze = {
    "complaint_id"    : "CMP-2026-00001",
    "bank_name"       : "SBI",
    "account_masked"  : "XXXX1234",
    "amount"          : 45000,
    "request_status"  : "pending",   # pending / sent / frozen / rejected / reversed
    "requested_by"    : "officer_id",
    "requested_at"    : datetime.utcnow(),
    "bank_response"   : None,
    "resolved_at"     : None
}

# ── 8. AUDIT_LOGS ─────────────────────────────────────────
logs_col.create_index("user_id")
logs_col.create_index("complaint_id")
logs_col.create_index("action_at")

sample_log = {
    "user_id"      : "officer_id",
    "complaint_id" : "CMP-2026-00001",
    "action"       : "complaint_assigned",
    "details"      : "Assigned to Officer Rahul Sharma",
    "ip_address"   : "192.168.1.10",
    "action_at"    : datetime.utcnow()
}

print("All collections and indexes created!")
print("Default admin user created — username: admin, password: Admin@123")