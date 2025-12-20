"""Create apollo database in PostgreSQL"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to PostgreSQL server (not to a specific database)
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="1234"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE apollo;")
    print("✅ Database 'apollo' created successfully!")

    cursor.close()
    conn.close()

except psycopg2.errors.DuplicateDatabase:
    print("✅ Database 'apollo' already exists!")
except Exception as e:
    print(f"❌ Error creating database: {e}")
