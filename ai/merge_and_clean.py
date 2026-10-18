import pandas as pd
import re
import os

# ── Step 1: Read all CSV files ─────────────────────────────
csv_files = [
    "ai/c1.csv",
    "ai/c2.csv",
    "ai/c3.csv",
    "ai/c4.csv",
    "ai/c5.csv",
    "ai/c6.csv",
    "ai/c7.csv",
]

dfs = []
for file in csv_files:
    if os.path.exists(file):
        try:
            df = pd.read_csv(file, dtype=str)
            print(f"✅ {file}: {len(df)} rows loaded")
            dfs.append(df)
        except Exception as e:
            print(f"❌ {file}: Error - {e}")
    else:
        print(f"⚠️  {file}: Not found, skipping")

if not dfs:
    print("❌ No files loaded. Check file paths.")
    exit()

# ── Step 2: Merge all ──────────────────────────────────────
combined = pd.concat(dfs, ignore_index=True)
print(f"\nTotal rows after merge : {len(combined)}")

# ── Step 3: Standardize columns ───────────────────────────
# Rename columns if slightly different names exist
combined.columns = combined.columns.str.strip().str.lower()

# Make sure all required columns exist
required = ["complaint_text", "category", "amount", "district",
            "transaction_id", "bank_name", "phone_number",
            "timestamp", "status", "language"]

for col in required:
    if col not in combined.columns:
        combined[col] = "N/A"

# Keep only required columns (drop complaint_id — we will regenerate)
combined = combined[required].copy()

# ── Step 4: Clean category column ─────────────────────────
combined["category"] = combined["category"].astype(str).str.strip().str.lower()

combined["category"] = combined["category"].replace({
    "finanzial_fraud"    : "financial_fraud",
    "financial fraud"    : "financial_fraud",
    "digital arrest"     : "digital_arrest",
    "fake news"          : "fake_news",
    "identity theft"     : "identity_theft",
    "social media crime" : "social_media_crime",
    "online job fraud"   : "online_job_fraud",
    "loan app fraud"     : "loan_app_fraud",
    "cyber bullying"     : "cyber_bullying",
    "nan"                : "unknown",
})

# Keep only valid categories
VALID_CATS = [
    "financial_fraud",
    "identity_theft",
    "digital_arrest",
    "fake_news",
    "darknet",
    "social_media_crime",
    "online_job_fraud",
    "sextortion",
    "loan_app_fraud",
    "cyber_bullying",
]

before = len(combined)
combined = combined[combined["category"].isin(VALID_CATS)]
print(f"Rows removed (invalid category) : {before - len(combined)}")

# ── Step 5: Clean complaint_text ───────────────────────────
# Remove Python code patterns
bad_patterns = [
    r'random\.randint',
    r'random\.choice',
    r'random\.uniform',
    r'random\.sample',
    r'\{random',
    r'randint\(',
    r'choice\(',
    r'f"',
    r"f'",
    r'\.format\(',
    r'import random',
    r'def ',
    r'print\(',
    r'\[\'HDFC\'',
    r'\[\'SBI\'',
    r'\[\'WhatsApp\'',
    r'\[\'Instagram\'',
    r'\[\'Telegram\'',
    r'\[\'Paytm\'',
    r'\[\'GPay\'',
    r'random\.',
]

def is_bad_row(text):
    text = str(text)
    for pattern in bad_patterns:
        if re.search(pattern, text):
            return True
    return False

before = len(combined)
mask = combined["complaint_text"].apply(is_bad_row)
combined = combined[~mask]
print(f"Rows removed (Python code)      : {before - len(combined)}")

# ── Step 6: Remove empty/short texts ──────────────────────
before = len(combined)
combined = combined.dropna(subset=["complaint_text"])
combined = combined[combined["complaint_text"].astype(str).str.strip() != ""]
combined = combined[combined["complaint_text"].astype(str).str.strip() != "nan"]
combined = combined[combined["complaint_text"].astype(str).str.len() > 50]
print(f"Rows removed (empty/short)      : {before - len(combined)}")

# ── Step 7: Remove duplicates ──────────────────────────────
before = len(combined)
combined = combined.drop_duplicates(subset=["complaint_text"])
print(f"Rows removed (duplicates)       : {before - len(combined)}")

# ── Step 8: Renumber complaint IDs cleanly ─────────────────
# Format: CPL-1, CPL-2, CPL-3 ... CPL-N
combined = combined.reset_index(drop=True)
combined.insert(0, "complaint_id", 
    combined.index.map(lambda i: f"CPL-{i+1}")
)

# ── Step 9: Final summary ──────────────────────────────────
print(f"\n{'='*55}")
print(f"  FINAL CLEAN DATASET SUMMARY")
print(f"{'='*55}")
print(f"  Total clean rows     : {len(combined)}")
print(f"  Complaint ID range   : CPL-1 to CPL-{len(combined)}")
print(f"\n  Category distribution:")
cat_counts = combined["category"].value_counts()
for cat, count in cat_counts.items():
    pct = round((count / len(combined)) * 100, 1)
    print(f"    {cat:<25} : {count} rows ({pct}%)")

print(f"\n  Language distribution:")
lang_counts = combined["language"].value_counts()
for lang, count in lang_counts.items():
    print(f"    {lang:<25} : {count} rows")
print(f"{'='*55}")

# ── Step 10: Save final file ───────────────────────────────
output = "ai/training_data.csv"
combined.to_csv(output, index=False)
print(f"\n✅ Saved to     : {output}")
print(f"✅ Ready to run : python ai/train_model.py")