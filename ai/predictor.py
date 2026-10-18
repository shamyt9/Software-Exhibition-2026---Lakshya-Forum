import pickle
import re

MODEL_PATH      = "ai/model/classifier.pkl"
VECTORIZER_PATH = "ai/model/vectorizer.pkl"

# Load once when server starts
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# ── Human-readable labels ──────────────────────────────────
CATEGORY_LABELS = {
    "financial_fraud"   : "Cyber Financial Fraud",
    "digital_arrest"    : "Digital Arrest Scam",
    "fake_news"         : "Fake News / Misinformation",
    "identity_theft"    : "Identity Theft / Impersonation",
    "darknet"           : "Darknet Crime",
    "social_media_crime": "Social Media Crime",
    "online_job_fraud"  : "Online Job Fraud",
    "sextortion"        : "Sextortion / Honey Trap",
    "loan_app_fraud"    : "Illegal Loan App Fraud",
    "cyber_bullying"    : "Cyber Bullying / Stalking",
}

# ── Severity weights (0 to 1) ──────────────────────────────
SEVERITY = {
    "financial_fraud"   : 0.90,
    "digital_arrest"    : 0.95,
    "fake_news"         : 0.45,
    "identity_theft"    : 0.70,
    "darknet"           : 1.00,
    "social_media_crime": 0.65,
    "online_job_fraud"  : 0.72,
    "sextortion"        : 0.92,
    "loan_app_fraud"    : 0.78,
    "cyber_bullying"    : 0.68,
}

# ── Minimum risk level per category ───────────────────────
# Ensures correct risk even when confidence is low
MINIMUM_RISK = {
    "financial_fraud"   : "MEDIUM",
    "digital_arrest"    : "HIGH",
    "fake_news"         : "LOW",
    "identity_theft"    : "MEDIUM",
    "darknet"           : "HIGH",
    "social_media_crime": "MEDIUM",
    "online_job_fraud"  : "MEDIUM",
    "sextortion"        : "HIGH",
    "loan_app_fraud"    : "MEDIUM",
    "cyber_bullying"    : "MEDIUM",
}

# ── Legal sections per category ────────────────────────────
LEGAL_SECTIONS = {
    "financial_fraud"   : [
        "Section 66C IT Act 2000",
        "Section 66D IT Act 2000",
        "Section 420 IPC",
        "Section 406 IPC",
        "Section 120B IPC",
    ],
    "digital_arrest"    : [
        "Section 66D IT Act 2000",
        "Section 384 IPC",
        "Section 419 IPC",
        "Section 420 IPC",
        "Section 506 IPC",
    ],
    "fake_news"         : [
        "Section 505(1)(b) IPC",
        "Section 505(2) IPC",
        "Section 153A IPC",
        "Section 54 NDMA Act",
    ],
    "identity_theft"    : [
        "Section 66C IT Act 2000",
        "Section 419 IPC",
        "Section 468 IPC",
        "Section 471 IPC",
        "Section 43 IT Act 2000",
    ],
    "darknet"           : [
        "Section 66 IT Act 2000",
        "Section 67 IT Act 2000",
        "Section 67A IT Act 2000",
        "Section 292 IPC",
        "NDPS Act Section 8",
    ],
    "social_media_crime": [
        "Section 67 IT Act 2000",
        "Section 67A IT Act 2000",
        "Section 354D IPC",
        "Section 509 IPC",
        "Section 499 IPC",
        "Section 500 IPC",
    ],
    "online_job_fraud"  : [
        "Section 420 IPC",
        "Section 406 IPC",
        "Section 66D IT Act 2000",
        "Section 120B IPC",
    ],
    "sextortion"        : [
        "Section 67A IT Act 2000",
        "Section 384 IPC",
        "Section 354C IPC",
        "Section 354D IPC",
        "Section 506 IPC",
        "Section 66E IT Act 2000",
    ],
    "loan_app_fraud"    : [
        "Section 66C IT Act 2000",
        "Section 420 IPC",
        "Section 385 IPC",
        "Section 386 IPC",
        "RBI Digital Lending Guidelines 2022",
    ],
    "cyber_bullying"    : [
        "Section 507 IPC",
        "Section 504 IPC",
        "Section 354D IPC",
        "Section 67 IT Act 2000",
        "Section 66A IT Act 2000 (advisory)",
    ],
}

# ── Preprocessing ──────────────────────────────────────────
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ── Amount band scoring ────────────────────────────────────
def amount_band(amount):
    try:
        amount = float(amount)
    except:
        amount = 0
    if amount >= 500000:  return 1.00   # above 5 lakh = very high
    if amount >= 100000:  return 0.85   # 1L-5L = high
    if amount >= 50000:   return 0.70   # 50k-1L = medium high
    if amount >= 10000:   return 0.50   # 10k-50k = medium
    if amount > 0:        return 0.30   # below 10k = low
    return 0.10                          # no amount = very low

# ── Risk computation ───────────────────────────────────────
def compute_risk(category, confidence, amount):
    severity  = SEVERITY.get(category, 0.5)
    amt_score = amount_band(amount)

    # Confidence gets less weight because low training data
    # causes low confidence even for correct predictions
    score = (0.25 * confidence) + (0.45 * severity) + (0.30 * amt_score)
    score = round(score * 100, 1)

    # Determine level from score
    if score >= 65:   level = "HIGH"
    elif score >= 40: level = "MEDIUM"
    else:             level = "LOW"

    # Apply minimum risk floor per category
    # So digital_arrest is never LOW even with low confidence
    min_level  = MINIMUM_RISK.get(category, "LOW")
    level_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

    if level_rank[level] < level_rank[min_level]:
        level = min_level

    return score, level

# ── Main predict function ──────────────────────────────────
def predict(complaint_text, amount=0):
    clean   = preprocess(complaint_text)
    vec     = vectorizer.transform([clean])
    proba   = model.predict_proba(vec)[0]
    classes = model.classes_

    all_scores = {cls: round(float(p), 4) for cls, p in zip(classes, proba)}

    top_category   = classes[proba.argmax()]
    top_confidence = round(float(proba.max()), 4)

    risk_score, risk_level = compute_risk(top_category, top_confidence, amount)

    return {
        "category"        : top_category,
        "category_label"  : CATEGORY_LABELS.get(top_category, top_category),
        "confidence"      : top_confidence,
        "confidence_pct"  : round(top_confidence * 100, 1),
        "all_scores"      : all_scores,
        "risk_score"      : risk_score,
        "risk_level"      : risk_level,
        "legal_sections"  : LEGAL_SECTIONS.get(top_category, []),
    }

def generate_summary(text, amount=0, bank_name="N/A", txn_id="N/A"):
    """
    Generate a professional case summary based on complaint text, amount, bank and txn ID.
    Used for fund reversal support.
    """
    summary_template = (
        f"Case involves potential financial fraud amounting to ₹{amount:,.2f} "
        f"transferred to {bank_name} (Txn ID: {txn_id}). "
        f"Complainant reports: '{text[:200]}...'. "
        "The patterns suggest unauthorized fund transfer requiring immediate bank intervention and transaction blocking under RBI guidelines (24-48h window)."
    )
    return summary_template
