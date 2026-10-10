import sqlite3
from fastapi import FastAPI

conn = sqlite3.connect("library.db")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

# Insert the sample rows only when the table is empty, so rerunning this
# file does not add duplicate copies of the same sample data.
cursor.execute("SELECT COUNT(*) FROM books")
if cursor.fetchone()[0] == 0:
    books = [
        ("Python Basics", "Rao", 250),
        ("SQL Guide", "Mehta", 150),
        ("Web Dev", "Khan", 400),
    ]
    cursor.executemany(
        "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
        books
    )
    conn.commit()



# Delete books whose price is less than 200.
cursor.execute("DELETE FROM books WHERE price < ?", (200,))
conn.commit()

# Display the rows left in the table.
print("\nRemaining books:")
cursor.execute("SELECT id, title, author, price FROM books ORDER BY id")
for row in cursor.fetchall():
    print(row)

conn.close()

