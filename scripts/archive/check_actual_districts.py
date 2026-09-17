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
cur.execute("SELECT id, name FROM districts ORDER BY id")
dists = cur.fetchall()
print("ACTUAL DISTRICTS TABLE IN MYSQL:")
for d in dists:
    print(f"{d['id']:2d}: {d['name']}")

target_dists = [
    'West Champaran', 'Siwan', 'Begusarai', 'Buxar', 'Arwal', 
    'Madhubani', 'Samastipur', 'Madhepura', 'Kishanganj', 'Saran'
]

print("\nMAPPING FOR 10 BATCH 7 DISTRICTS:")
for td in target_dists:
    match = [d for d in dists if td.lower() in d['name'].lower()]
    print(f"  {td:<16} -> {match}")
