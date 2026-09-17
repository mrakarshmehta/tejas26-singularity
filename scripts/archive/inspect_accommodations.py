"""
Inspect accommodations and nearby_services tables for Hotels.
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
from models.connection import get_db

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with get_db() as db:
    cursor = db.cursor()

    print("=== Table: accommodations ===")
    cursor.execute("DESCRIBE accommodations")
    for r in cursor.fetchall():
        print(f"  {r['Field']} ({r['Type']}) Nullable={r['Null']} Key={r['Key']}")
    cursor.execute("SELECT * FROM accommodations LIMIT 10")
    acc_rows = cursor.fetchall()
    print(f"Total rows in accommodations: {len(acc_rows)}")
    for a in acc_rows:
        print("  ", a)

    print("\n=== Table: nearby_services ===")
    cursor.execute("DESCRIBE nearby_services")
    for r in cursor.fetchall():
        print(f"  {r['Field']} ({r['Type']}) Nullable={r['Null']} Key={r['Key']}")
    cursor.execute("SELECT service_type, COUNT(*) as cnt FROM nearby_services GROUP BY service_type")
    for r in cursor.fetchall():
        print(f"  Service Type: {r['service_type']} -> Count: {r['cnt']}")

    cursor.execute("""
        SELECT * FROM nearby_services
        WHERE LOWER(service_type) IN ('hotel', 'lodging', 'resort', 'stay', 'accommodation')
        LIMIT 10
    """)
    ns_hotels = cursor.fetchall()
    print(f"\nTotal hotel nearby services: {len(ns_hotels)}")
    for nh in ns_hotels:
        print("  ", nh)
