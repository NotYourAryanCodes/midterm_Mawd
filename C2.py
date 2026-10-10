import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_NAME = "shop.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


create_table()
app = FastAPI(title="Books API")


# (a) Pydantic model for a book.
class Book(BaseModel):
    title: str
    author: str
    price: float


# (b) Create a book. Return its new id and details.
@app.post("/books", status_code=201)
def add_book(book: Book):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
        (book.title, book.author, book.price)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }


# (c) Get all books.
@app.get("/books")
def get_books():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM books ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


# (c) Get one book by id.
@app.get("/books/{book_id}")
def get_book(book_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM books WHERE id = ?", (book_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)


# (d) Update a book, or return 404 if the id does not exist.
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?",
        (book.title, book.author, book.price, book_id)
    )
    conn.commit()
    changed = cursor.rowcount
    conn.close()
    if changed == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "id": book_id,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }


# (e) Delete a book, or return 404 if the id does not exist.
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    changed = cursor.rowcount
    conn.close()
    if changed == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted", "id": book_id}
