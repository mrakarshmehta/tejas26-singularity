import sys, os
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
import pymysql

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', '3307')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hiddenyatra'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

BACKUP_PATH = os.path.join(r'd:\HiddenYatra\scratch', 'backup_feature_homestay_booking.sql')

def escape_val(val):
    if val is None:
        return 'NULL'
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, bytes):
        return "X'" + val.hex() + "'"
    s = str(val).replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
    return "'" + s + "'"

def main():
    conn = pymysql.connect(**DB_CONFIG)
    with conn.cursor() as cur, open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        f.write("-- HiddenYatra Full Database Backup before Homestay Booking Feature Phase\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        cur.execute("SHOW TABLES")
        tables = [list(row.values())[0] for row in cur.fetchall()]
        print(f"Backing up {len(tables)} tables to {BACKUP_PATH}...")
        for table in tables:
            cur.execute(f"SHOW CREATE TABLE `{table}`")
            create_stmt = list(cur.fetchone().values())[1]
            f.write(f"-- Table: {table}\n{create_stmt};\n\n")
            cur.execute(f"SELECT * FROM `{table}`")
            rows = cur.fetchall()
            if rows:
                cols = ', '.join(f"`{k}`" for k in rows[0].keys())
                for r in rows:
                    vals = ', '.join(escape_val(v) for v in r.values())
                    f.write(f"INSERT INTO `{table}` ({cols}) VALUES ({vals});\n")
                f.write("\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
    print(f"Backup complete! File size: {os.path.getsize(BACKUP_PATH)} bytes")

if __name__ == '__main__':
    main()
