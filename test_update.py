from database import complaints_col
from datetime import datetime

def test_update():
    result = complaints_col.update_one(
        {'complaint_id': 'CMP-2026-00033'},
        {'$set': {'reversal_status': 'frozen', 'reversal_updated_at': datetime.utcnow()}}
    )
    print(f"Modified count: {result.modified_count}")

if __name__ == '__main__':
    test_update()
