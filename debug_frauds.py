from database import complaints_col, transactions_col

def check_frauds():
    frauds = complaints_col.find({'crime_type': {'$in': ['financial_fraud', 'cyber_financial_fraud']}})
    print(f"{'Complaint ID':<20} | {'Crime Type':<25} | {'Txn Record?':<12} | {'Txn ID':<15} | {'Amount':<10}")
    print("-" * 90)
    for f in frauds:
        cid = f.get('complaint_id')
        ctype = f.get('crime_type')
        t = transactions_col.find_one({'complaint_id': cid})
        
        has_txn = t is not None
        txn_id = t.get('txn_id') if t else "MISSING"
        amount = t.get('amount', 0) if t else 0
        
        print(f"{cid:<20} | {ctype:<25} | {str(has_txn):<12} | {str(txn_id):<15} | {amount:<10}")

if __name__ == '__main__':
    print("Checking Financial Fraud Eligibility:")
    check_frauds()
