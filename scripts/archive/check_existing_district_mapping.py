import pymysql, os, dotenv
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
    SELECT p.id, p.name, p.district_id, d.name as district_name 
    FROM places p 
    JOIN districts d ON p.district_id = d.id 
    WHERE d.name IN ('West Champaran', 'Siwan', 'Begusarai', 'Buxar', 'Arwal', 'Jhanjharpur (Madhubani)', 'Samastipur', 'Madhepura', 'Kishanganj', 'Saran') 
    AND p.deleted_at IS NULL
    ORDER BY d.id, p.id
""")
for r in cur.fetchall():
    print(f"District {r['district_id']:2d} ({r['district_name']:<24}): Place {r['id']:3d} '{r['name']}'")
