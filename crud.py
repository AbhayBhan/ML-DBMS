import sqlite3

conn = sqlite3.connect('books.db')
cursor = conn.cursor()



cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        year INTEGER
    )
''')
conn.commit()

def create_book(title, author, year):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, year)
        VALUES (?, ?, ?)
    ''', (title, author, year))
    conn.commit()
    conn.close()

def read_books():
    cursor.execute('SELECT * FROM books')
    return cursor.fetchall()

def update_book(book_id, title, author, year):
    cursor.execute('''
        UPDATE books
        SET title = ?, author = ?, year = ?
        WHERE id = ?
    ''', (title, author, year, book_id))
    conn.commit()

def delete_book(book_id):
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()

conn.close()
