import sqlite3
from pathlib import Path

DB = "bluestock_mf.db"
QUERY_FILE = Path("sql/queries.sql")

conn = sqlite3.connect(DB)

with open(QUERY_FILE, "r", encoding="utf-8") as f:
    sql = f.read()

# Split queries using semicolon
queries = [q.strip() for q in sql.split(";") if q.strip()]

for i, query in enumerate(queries, start=1):
    print(f"\n{'=' * 60}")
    print(f"QUERY {i}")
    print("=" * 60)

    try:
        cursor = conn.execute(query)
        rows = cursor.fetchall()

        for row in rows[:10]:
            print(row)

        print(f"\nRows returned: {len(rows)}")

    except Exception as e:
        print("ERROR:", e)

conn.close()