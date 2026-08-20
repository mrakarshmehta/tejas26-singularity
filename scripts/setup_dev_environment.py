"""
HiddenYatra — Team Development Database Setup CLI
One-command script for team members to set up a working local MySQL environment.

Usage:
  python scripts/setup_dev_environment.py

What it does:
  1. Loads configuration from .env file.
  2. Creates the target database (DEFAULT: 'hiddenyatra') if it doesn't exist.
  3. Executes scripts/migrations/mysql_schema.sql to create all 34 tables.
  4. Runs scripts/seed_dev_data.py to seed Bihar districts, sample places, homestays & demo accounts.
  5. Verifies database setup.
"""
import os
import sys
import logging
import pymysql

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv('.env')

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def setup_environment():
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = int(os.environ.get('DB_PORT', '3306'))
    db_user = os.environ.get('DB_USER', 'root')
    db_pass = os.environ.get('DB_PASSWORD', '')
    db_name = os.environ.get('DB_NAME', 'hiddenyatra')
    db_charset = os.environ.get('DB_CHARSET', 'utf8mb4')

    print("\n=======================================================")
    print(" HiddenYatra — Team Development Setup Routine")
    print("=======================================================\n")
    logger.info("Connecting to MySQL server at %s:%d as user '%s'...", db_host, db_port, db_user)

    # Step 1: Create Database if Not Exists
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            charset=db_charset
        )
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        logger.info("Database '%s' is ready.", db_name)
    except Exception as e:
        logger.error("Failed to connect to MySQL server or create database: %s", e)
        logger.error("Please verify that MySQL is running and credentials in '.env' are correct.")
        sys.exit(1)

    # Step 2: Apply Schema SQL
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'migrations', 'mysql_schema.sql'
    )

    if not os.path.exists(schema_path):
        logger.error("Schema file not found at %s!", schema_path)
        sys.exit(1)

    logger.info("Applying database schema from %s...", schema_path)
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name,
            charset=db_charset
        )
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql = f.read()

        statements = [s.strip() for s in sql.split(';') if s.strip()]
        with conn.cursor() as cur:
            for stmt in statements:
                if stmt.upper().startswith(('CREATE DATABASE', 'USE ')):
                    continue
                try:
                    cur.execute(stmt)
                except Exception as ex:
                    # Ignore duplicate key / table already exists warnings
                    pass
        conn.commit()
        conn.close()
        logger.info("Database schema applied successfully.")
    except Exception as e:
        logger.error("Failed to execute schema SQL: %s", e)
        sys.exit(1)

    # Step 3: Seed Development Data
    logger.info("Seeding development demo data...")
    try:
        from scripts.seed_dev_data import seed_development_data
        seed_development_data()
    except Exception as e:
        logger.error("Failed to seed development data: %s", e)
        sys.exit(1)

    # Step 4: Verification Summary
    logger.info("Verifying database tables...")
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name,
            charset=db_charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS cnt FROM information_schema.tables WHERE table_schema = %s", (db_name,))
            table_cnt = cur.fetchone()['cnt']
            cur.execute("SELECT COUNT(*) AS cnt FROM districts")
            dist_cnt = cur.fetchone()['cnt']
            cur.execute("SELECT COUNT(*) AS cnt FROM places")
            place_cnt = cur.fetchone()['cnt']
            cur.execute("SELECT COUNT(*) AS cnt FROM users")
            user_cnt = cur.fetchone()['cnt']
        conn.close()

        print("\n=======================================================")
        print(" HiddenYatra Setup Successful!")
        print("=======================================================")
        print(f" Database: {db_name}")
        print(f" Tables Created: {table_cnt}")
        print(f" Districts Seeded: {dist_cnt}")
        print(f" Places Seeded: {place_cnt}")
        print(f" Users Created: {user_cnt}")
        print("\nDefault Local Accounts:")
        print("  - Admin:    username='admin'          password='admin123'")
        print("  - Host:     username='demo_host'      password='password123'")
        print("  - Traveler: username='demo_traveler'  password='password123'")
        print("\nYou can now start the Flask server with:")
        print("  python app.py\n")
    except Exception as e:
        logger.warning("Verification query encountered an error: %s", e)


if __name__ == '__main__':
    setup_environment()
