import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

with get_cursor() as cursor:
    cursor.execute("""
        SELECT p.id, p.name, p.category, d.name as district_name 
        FROM places p 
        JOIN districts d ON p.district_id=d.id 
        WHERE d.name = 'Bhagalpur' AND p.deleted_at IS NULL
    """)
    for r in cursor.fetchall():
        print(r)
