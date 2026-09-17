import sys, os, pymysql, dotenv
dotenv.load_dotenv()

conn = pymysql.connect(
    host=os.getenv('DB_HOST','127.0.0.1'),
    port=int(os.getenv('DB_PORT',3307)),
    user=os.getenv('DB_USER','root'),
    password=os.getenv('DB_PASSWORD',''),
    database=os.getenv('DB_NAME','hiddenyatra'),
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()
cur.execute("""
    SELECT p.id, p.name, p.category, d.name as district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON p.district_id = d.id
    WHERE p.deleted_at IS NULL AND d.name IN (
        'Arwal', 'Khagaria', 'Kishanganj', 'Madhepura', 'Samastipur', 'Sheohar', 'Siwan', 'Supaul',
        'Begusarai', 'Buxar', 'West Champaran', 'Madhubani', 'Saran', 'Nawada', 'Jamui', 'Lakhisarai', 'Jehanabad'
    )
    ORDER BY d.name, p.id
""")
rows = cur.fetchall()
for r in rows:
    print(f"{r['district_name']:<18} | ID: {r['id']:3d} | {r['name']:<42} | Cat: {r['category']} | {r['latitude']}, {r['longitude']}")
