import sqlite3
from fastapi import FastAPI

DB_NAME = "college.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def make_table_if_needed():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT,
            city TEXT,
            marks INTEGER
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO students (name, course, city, marks) VALUES (?, ?, ?, ?)",
            [
                ("Aman", "BSc", "Jaipur", 78),
                ("Priya", "BCA", "Pali", 89),
                ("Rahul", "BSc", "Jodhpur", 45),
                ("Sneha", "BSc", "Pali", 92),
                ("Karan", "BCA", "Jaipur", 30),
            ]
        )
    conn.commit()
    conn.close()


# B1. Print names and marks for marks above 80, highest marks first.
def question_b1():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, marks FROM students WHERE marks > ? ORDER BY marks DESC",
        (80,)
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row["name"], row["marks"])
    conn.close()




# B2. Insert Vikram safely. Existing ids are 1 to 5, so his id will be 6.
def question_b2():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, course, city, marks) VALUES (?, ?, ?, ?)",
        ("Vikram", "BCA", "Udaipur", 67)
    )
    conn.commit()
    print("Vikram's id:", cursor.lastrowid)
    conn.close()

# B3. CRUD means:
# Create: INSERT, HTTP POST
# Read:   SELECT, HTTP GET
# Update: UPDATE, HTTP PUT
# Delete: DELETE, HTTP DELETE

# B4.
app = FastAPI()


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": "Hello " + name}


# B5. Two common corrections in the student lookup code:
# 1. SQL parameters must be supplied as a one-item tuple: (student_id,)
# 2. The condition must use 'is None' and end with a colon.
# Correct lines:
# row = conn.execute(
#     "SELECT * FROM students WHERE id = ?", (student_id,)
# ).fetchone()
# if row is None:
#     raise HTTPException(status_code=404, detail="Student not found")


if __name__ == "__main__":
    make_table_if_needed()
    print("B1 output:")
    question_b1()
    print("\nB2 output:")
    question_b2()
