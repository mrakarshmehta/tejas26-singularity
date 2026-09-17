"""
Complete MySQL database backup using Python/PyMySQL.
Creates a full SQL dump including schema + data for all tables.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

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

BACKUP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'backup_hiddenyatra_20260814_1934.sql')

def escape_value(val):
    if val is None:
        return 'NULL'
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, bytes):
        return "X'" + val.hex() + "'"
    s = str(val)
    s = s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r').replace('\0', '\\0')
    return "'" + s + "'"

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        f.write(f"-- HiddenYatra Full Database Backup\n")
        f.write(f"-- Generated: 2026-08-14 19:34 IST\n")
        f.write(f"-- Database: {DB_CONFIG['database']}\n")
        f.write(f"-- Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}\n\n")
        f.write(f"SET NAMES utf8mb4;\n")
        f.write(f"SET FOREIGN_KEY_CHECKS = 0;\n\n")

        # Get all tables
        cur.execute("SHOW TABLES")
        tables = [list(row.values())[0] for row in cur.fetchall()]
        print(f"Found {len(tables)} tables: {', '.join(tables)}")

        for table in tables:
            print(f"  Backing up: {table}...")

            # Schema
            cur.execute(f"SHOW CREATE TABLE `{table}`")
            create_stmt = list(cur.fetchone().values())[1]
            f.write(f"-- -------------------------------------------\n")
            f.write(f"-- Table: {table}\n")
            f.write(f"-- -------------------------------------------\n")
            f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
            f.write(f"{create_stmt};\n\n")

            # Data
            cur.execute(f"SELECT * FROM `{table}`")
            rows = cur.fetchall()
            if rows:
                columns = list(rows[0].keys())
                col_str = ', '.join(f'`{c}`' for c in columns)
                f.write(f"-- Data for {table} ({len(rows)} rows)\n")
                for row in rows:
                    vals = ', '.join(escape_value(row[c]) for c in columns)
                    f.write(f"INSERT INTO `{table}` ({col_str}) VALUES ({vals});\n")
                f.write('\n')
            else:
                f.write(f"-- {table}: 0 rows\n\n")

        f.write(f"\nSET FOREIGN_KEY_CHECKS = 1;\n")
        f.write(f"-- End of backup\n")

    cur.close()
    conn.close()

    size = os.path.getsize(BACKUP_PATH)
    print(f"\n✅ BACKUP COMPLETE")
    print(f"   Path: {BACKUP_PATH}")
    print(f"   Size: {size:,} bytes ({size/1024:.1f} KB)")
    print(f"   Tables: {len(tables)}")

if __name__ == '__main__':
    main()
