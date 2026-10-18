from database import complaints_col, transactions_col

def inspect_complaint(cid):
    c = complaints_col.find_one({'complaint_id': cid})
    t = transactions_col.find_one({'complaint_id': cid})
    print(f"--- {cid} ---")
    print(f"Crime Type: '{c.get('crime_type')}'")
    print(f"Transaction Found: {t is not None}")
    if t:
        print(f"Txn ID: '{t.get('txn_id')}'")
        print(f"Amount: {t.get('amount')}")
        print(f"Amount Type: {type(t.get('amount'))}")

if __name__ == '__main__':
    inspect_complaint('CMP-2026-00005')
    inspect_complaint('CMP-2026-00007')
