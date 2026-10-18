"""
Freeze Request Management Module
Handles transaction blocking/freezing requests for financial fraud cases
"""

from datetime import datetime, timedelta
from bson import ObjectId
from database import complaints_col, predictions_col, risks_col, freezes_col, transactions_col, logs_col
import json

# RBI Guidelines and Legal References
RBI_GUIDELINES = {
    "section_8": "Section 8 of RBI Cyber Security Framework - Fraud Detection & Transaction Blocking",
    "guidelines_2023": "RBI Guidelines on Regulation of Payment Systems - 2023 (Transaction Reversal)",
    "cyber_alert": "RBI Cyber Fraud Alert - Urgent Transaction Blocking Procedures"
}

LEGAL_SECTIONS_MAP = {
    "financial_fraud": ["66C IT Act", "66D IT Act", "420 IPC", "406 IPC"],
    "online_fraud": ["66C IT Act", "66D IT Act", "420 IPC"],
    "cyber_financial_fraud": ["66C IT Act", "66D IT Act", "120B IPC"],
    "credit_card_fraud": ["66C IT Act", "420 IPC", "406 IPC"],
    "loan_fraud": ["420 IPC", "468 IPC", "471 IPC"],
}

# Priority thresholds
FREEZE_ELIGIBILITY_THRESHOLD = 10000  # ₹10,000
HIGH_PRIORITY_THRESHOLD = 500000  # ₹5 lakhs


def is_financial_fraud_complaint(complaint_id):
    """Check if complaint is classified as financial fraud"""
    prediction = predictions_col.find_one({"complaint_id": complaint_id})
    if not prediction:
        return False
    
    fraud_categories = [
        "financial_fraud",
        "online_fraud",
        "cyber_financial_fraud",
        "credit_card_fraud",
        "loan_fraud",
        "online_job_fraud",
        "fake_sms_fraud",
        "email_spoofing_fraud"
    ]
    
    return prediction.get("category") in fraud_categories


def check_freeze_eligibility(complaint_id):
    """
    Check if complaint is eligible for transaction freezing.
    Returns dict with eligibility status and reason
    """
    complaint = complaints_col.find_one({"complaint_id": complaint_id})
    if not complaint:
        return {"eligible": False, "reason": "Complaint not found"}
    
    # Check if financial fraud
    if not is_financial_fraud_complaint(complaint_id):
        return {"eligible": False, "reason": "Not classified as financial fraud"}
    
    # Check amount threshold
    amount = complaint.get("amount_involved", 0)
    if amount < FREEZE_ELIGIBILITY_THRESHOLD:
        return {
            "eligible": False,
            "reason": f"Amount (₹{amount:,.0f}) below minimum threshold (₹{FREEZE_ELIGIBILITY_THRESHOLD:,.0f})"
        }
    
    # Check if transaction details exist
    transaction = transactions_col.find_one({"complaint_id": complaint_id})
    if not transaction:
        return {
            "eligible": True,
            "reason": "Eligible but transaction details not in system - can be added manually",
            "requires_manual_entry": True
        }
    
    return {"eligible": True, "requires_manual_entry": False}


def calculate_priority_score(complaint_id):
    """
    Calculate priority score based on:
    - Amount (higher = higher priority)
    - Time since transaction (recent = higher priority)
    - Risk level (HIGH > MEDIUM > LOW)
    
    Returns score out of 100
    """
    complaint = complaints_col.find_one({"complaint_id": complaint_id})
    transaction = transactions_col.find_one({"complaint_id": complaint_id})
    risk = risks_col.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        return 0
    
    score = 0
    
    # Amount factor (0-40 points)
    amount = complaint.get("amount_involved", 0)
    amount_score = min(40, (amount / HIGH_PRIORITY_THRESHOLD) * 40)
    score += amount_score
    
    # Time decay factor (0-30 points)
    if transaction and transaction.get("txn_timestamp"):
        txn_time = transaction["txn_timestamp"]
        if isinstance(txn_time, str):
            txn_time = datetime.fromisoformat(txn_time)
        
        hours_since_txn = (datetime.utcnow() - txn_time).total_seconds() / 3600
        
        # Recent transactions get higher score
        if hours_since_txn < 24:
            score += 30  # Full 30 points for very recent
        elif hours_since_txn < 48:
            score += 25
        elif hours_since_txn < 72:
            score += 15
        else:
            score += 5
    else:
        score += 10  # Default score if timestamp not available
    
    # Risk level factor (0-30 points)
    if risk:
        risk_level = risk.get("risk_level", "LOW")
        if risk_level == "HIGH":
            score += 30
        elif risk_level == "MEDIUM":
            score += 15
        else:
            score += 5
    
    return min(100, score)


def get_applicable_legal_sections(complaint_id):
    """Get applicable legal sections for the complaint"""
    prediction = predictions_col.find_one({"complaint_id": complaint_id})
    
    if prediction and prediction.get("legal_sections"):
        return prediction["legal_sections"]
    
    # Fallback: determine from category
    if prediction:
        category = prediction.get("category", "financial_fraud")
        return LEGAL_SECTIONS_MAP.get(category, ["420 IPC", "66C IT Act"])
    
    return ["420 IPC", "66C IT Act"]


def extract_transaction_details(complaint_id, manual_data=None):
    """
    Extract transaction details from system or accept manual entry.
    manual_data: dict with manually entered transaction details
    """
    transaction = transactions_col.find_one({"complaint_id": complaint_id})
    complaint = complaints_col.find_one({"complaint_id": complaint_id})
    
    if manual_data:
        # Use manually provided data
        return {
            "txn_id": manual_data.get("txn_id", ""),
            "bank_name": manual_data.get("bank_name", ""),
            "account_number": manual_data.get("account_number", ""),
            "amount": manual_data.get("amount", complaint.get("amount_involved", 0)),
            "beneficiary": manual_data.get("beneficiary", ""),
            "timestamp": manual_data.get("timestamp", datetime.utcnow()),
            "source": "manual_entry"
        }
    elif transaction:
        # Use system data
        return {
            "txn_id": transaction.get("txn_id", ""),
            "bank_name": transaction.get("bank_name", ""),
            "account_number": transaction.get("account_masked", ""),
            "amount": transaction.get("amount", complaint.get("amount_involved", 0)),
            "beneficiary": transaction.get("beneficiary", ""),
            "timestamp": transaction.get("txn_timestamp", datetime.utcnow()),
            "source": "system_record"
        }
    else:
        # Minimal data from complaint
        return {
            "txn_id": "",
            "bank_name": "",
            "account_number": "",
            "amount": complaint.get("amount_involved", 0),
            "beneficiary": "",
            "timestamp": complaint.get("submitted_at", datetime.utcnow()),
            "source": "complaint_only"
        }


def generate_freeze_request(complaint_id, user_id, user_name, manual_txn_data=None):
    """
    Generate a freeze request object for a financial fraud complaint.
    
    Args:
        complaint_id: Complaint ID
        user_id: ID of officer generating the request
        user_name: Name of officer
        manual_txn_data: Optional dict with manually entered transaction details
    
    Returns:
        dict with freeze request details
    """
    
    # Verify eligibility
    eligibility = check_freeze_eligibility(complaint_id)
    if not eligibility.get("eligible"):
        return {"error": eligibility.get("reason")}
    
    complaint = complaints_col.find_one({"complaint_id": complaint_id})
    prediction = predictions_col.find_one({"complaint_id": complaint_id})
    risk = risks_col.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        return {"error": "Complaint not found"}
    
    # Generate unique freeze request ID
    freeze_req_id = f"FRZ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{complaint_id[-5:]}"
    
    # Extract transaction details
    txn_details = extract_transaction_details(complaint_id, manual_txn_data)
    
    # Calculate priority
    priority_score = calculate_priority_score(complaint_id)
    if priority_score > 75:
        priority = "URGENT"
    elif priority_score > 50:
        priority = "HIGH"
    else:
        priority = "NORMAL"
    
    # Get legal sections
    legal_sections = get_applicable_legal_sections(complaint_id)
    
    # Create freeze request object
    freeze_request = {
        "_id": freeze_req_id,
        "freeze_request_id": freeze_req_id,
        "complaint_id": complaint_id,
        "status": "pending",
        
        # Complainant Details
        "complainant_name": complaint.get("complainant_name", ""),
        "complainant_mobile": complaint.get("mobile", ""),
        "complainant_district": complaint.get("district", ""),
        
        # Complaint Classification
        "crime_category": prediction.get("category_label") if prediction else complaint.get("crime_type", ""),
        "risk_level": risk.get("risk_level") if risk else "MEDIUM",
        "risk_score": risk.get("risk_score") if risk else 0,
        
        # Transaction Details
        "transaction_id": txn_details.get("txn_id", ""),
        "bank_name": txn_details.get("bank_name", ""),
        "beneficiary_account": txn_details.get("account_number", ""),
        "beneficiary_name": txn_details.get("beneficiary", ""),
        "amount_involved": txn_details.get("amount", 0),
        "transaction_timestamp": txn_details.get("timestamp"),
        
        # Priority & Scores
        "priority_score": priority_score,
        "priority_level": priority,
        
        # Legal & Compliance
        "applicable_sections": legal_sections,
        "rbi_guideline": RBI_GUIDELINES.get("guidelines_2023"),
        "complaint_summary": complaint.get("complaint_text", "")[:500],  # First 500 chars
        
        # Officer Details
        "requested_by_officer_id": user_id,
        "requested_by_officer_name": user_name,
        "request_timestamp": datetime.utcnow(),
        
        # Bank/RBI Status
        "bank_response": None,
        "bank_response_timestamp": None,
        "bank_reference_id": None,
        
        # Status Updates
        "status_history": [
            {
                "status": "pending",
                "timestamp": datetime.utcnow(),
                "notes": "Freeze request generated"
            }
        ],
        
        # Additional fields
        "is_high_priority_alert": priority_score > 75 or txn_details["amount"] > HIGH_PRIORITY_THRESHOLD,
        "download_formats": ["pdf", "json"]
    }
    
    return freeze_request


def save_freeze_request(freeze_request_dict, user_id):
    """Save freeze request to database"""
    try:
        freeze_request_dict["saved_at"] = datetime.utcnow()
        freezes_col.insert_one(freeze_request_dict)
        
        # Log the action
        logs_col.insert_one({
            "user_id": user_id,
            "complaint_id": freeze_request_dict.get("complaint_id"),
            "action": "freeze_request_generated",
            "details": f"Freeze request {freeze_request_dict.get('freeze_request_id')} generated for transaction blocking - Amount: ₹{freeze_request_dict.get('amount_involved'):,.0f} | Priority: {freeze_request_dict.get('priority_level')}",
            "action_at": datetime.utcnow(),
            "permanent": True
        })
        
        # Update complaint status if needed
        complaints_col.update_one(
            {"complaint_id": freeze_request_dict.get("complaint_id")},
            {"$set": {
                "freeze_request_id": freeze_request_dict.get("freeze_request_id"),
                "has_freeze_request": True,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return {"success": True, "freeze_request_id": freeze_request_dict.get("freeze_request_id")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_freeze_request(freeze_request_id):
    """Retrieve a freeze request by ID"""
    return freezes_col.find_one({"_id": freeze_request_id})


def get_freeze_requests_by_complaint(complaint_id):
    """Get all freeze requests for a complaint"""
    return list(freezes_col.find({"complaint_id": complaint_id}).sort("request_timestamp", -1))


def get_all_freeze_requests(filters=None):
    """
    Get all freeze requests with optional filters.
    filters: dict with filter criteria (status, district, bank_name, date_range, etc.)
    """
    query = {}
    
    if filters:
        if filters.get("status"):
            query["status"] = filters["status"]
        if filters.get("district"):
            query["complainant_district"] = filters["district"]
        if filters.get("bank_name"):
            query["bank_name"] = filters["bank_name"]
        if filters.get("priority"):
            query["priority_level"] = filters["priority"]
        if filters.get("date_from") or filters.get("date_to"):
            date_query = {}
            if filters.get("date_from"):
                date_query["$gte"] = datetime.fromisoformat(filters["date_from"])
            if filters.get("date_to"):
                date_query["$lte"] = datetime.fromisoformat(filters["date_to"])
            if date_query:
                query["request_timestamp"] = date_query
    
    return list(freezes_col.find(query).sort("request_timestamp", -1))


def update_freeze_request_status(freeze_request_id, new_status, notes, user_id, user_name):
    """Update status of freeze request"""
    freeze_request = freezes_col.find_one({"_id": freeze_request_id})
    if not freeze_request:
        return {"success": False, "error": "Freeze request not found"}
    
    old_status = freeze_request.get("status")
    
    # Update status
    freezes_col.update_one(
        {"_id": freeze_request_id},
        {
            "$set": {
                "status": new_status,
                "updated_at": datetime.utcnow()
            },
            "$push": {
                "status_history": {
                    "status": new_status,
                    "timestamp": datetime.utcnow(),
                    "notes": notes,
                    "updated_by": user_name
                }
            }
        }
    )
    
    # Log the status change
    logs_col.insert_one({
        "user_id": user_id,
        "complaint_id": freeze_request.get("complaint_id"),
        "action": "freeze_request_status_updated",
        "details": f"Freeze request {freeze_request_id} status: {old_status} → {new_status} | Notes: {notes}",
        "action_at": datetime.utcnow(),
        "permanent": True
    })
    
    return {"success": True}


def record_bank_response(freeze_request_id, bank_reference_id, response_status, notes, user_id):
    """Record bank's response to freeze request"""
    freezes_col.update_one(
        {"_id": freeze_request_id},
        {
            "$set": {
                "bank_response": response_status,
                "bank_response_timestamp": datetime.utcnow(),
                "bank_reference_id": bank_reference_id,
                "bank_notes": notes
            }
        }
    )
    
    freeze_req = freezes_col.find_one({"_id": freeze_request_id})
    
    logs_col.insert_one({
        "user_id": user_id,
        "complaint_id": freeze_req.get("complaint_id"),
        "action": "bank_response_recorded",
        "details": f"Bank response received for {freeze_request_id}: {response_status} | Reference: {bank_reference_id}",
        "action_at": datetime.utcnow(),
        "permanent": True
    })
    
    return {"success": True}


def export_freeze_request_to_json(freeze_request_id):
    """Export freeze request as JSON for API integration"""
    freeze_request = freezes_col.find_one({"_id": freeze_request_id})
    if not freeze_request:
        return None
    
    # Remove MongoDB ObjectId and convert datetime objects
    freeze_request.pop("_id", None)
    
    # Convert all datetime objects to ISO format strings
    for key, value in freeze_request.items():
        if isinstance(value, datetime):
            freeze_request[key] = value.isoformat()
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            for item in value:
                for k, v in item.items():
                    if isinstance(v, datetime):
                        item[k] = v.isoformat()
    
    return freeze_request
