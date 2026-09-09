import sqlite3
from pathlib import Path

db_file = Path("bluestock_mf.db")
schema_file = Path("sql/schema.sql")

conn = sqlite3.connect(db_file)

with open(schema_file, "r", encoding="utf-8") as f:
    schema = f.read()

conn.executescript(schema)
conn.commit()

print("SQLite database created successfully:", db_file)

cursor = conn.cursor()
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""")

print("\nTables created:")
for table in cursor.fetchall():
    print("-", table[0])

conn.close()