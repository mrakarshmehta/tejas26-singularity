"""
Inspect places table columns and records.
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
    cursor.execute("DESCRIBE places")
    cols = [r['Field'] for r in cursor.fetchall()]
    print("Actual columns in places:", cols)

    cursor.execute("SELECT * FROM places LIMIT 1")
    sample = cursor.fetchone()
    print("\nSample place keys:", list(sample.keys()))
