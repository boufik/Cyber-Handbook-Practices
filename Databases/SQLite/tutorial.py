import sqlite3
from pathlib import Path

# 1a. Desired destination
DB_PATH = "/home/thomas/experiments/sqlite3-exp/scores.db"
# 1b. Make sure the parent directory exists
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

# 2. Connect, even file is missing - it is automatically created
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Query1: Create the table
SQL1 = """
CREATE TABLE IF NOT EXISTS demo (
id INTEGER PRIMARY KEY,
name TEXT,
score REAL
);
"""
cur.execute(SQL1)

# Query2: Insert one row - always use placeholders, never f-strings
SQL2 = """
INSERT INTO demo (name, score) VALUES (?, ?)
"""
cur.execute(SQL2, ("Alice", 9.5))

# Query3: Insert many rows (batch) at once - always use placeholders, never f-strings
SQL3 = """
INSERT INTO demo (name, score) VALUES (?, ?)
"""
rows = [
    ("Bob", 8.1),
    ("Carol", 9.7),
    ("Dave", 7.6)
]
cur.executemany(SQL3, rows)

# Query4: Get results
SQL4 = """
SELECT name, score FROM demo ORDER BY score DESC
"""
for row in cur.execute(SQL4):
    print(row)

# 3. Must commit to keep any insert before closing the connection
conn.commit()
# 4. Close the connection
conn.close()