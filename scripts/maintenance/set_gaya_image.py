import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()
cur.execute("UPDATE districts SET cover_image = 'district_2_8350b443.jpg' WHERE id = 2 AND (cover_image IS NULL OR cover_image = '')")
conn.commit()
print("Gaya cover image set to district_2_8350b443.jpg")
cur.close()
conn.close()
