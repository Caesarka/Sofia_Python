import sqlite3

conn = sqlite3.connect('books.db')
c = conn.cursor()

# Создать таблицу
c.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    price REAL
)
''')

# Вставить данные
books = [
    ('Clean Code', 'Robert Martin', 30),
    ('The Pragmatic Programmer', 'Andy Hunt', 25),
    ('Fluent Python', 'Luciano Ramalho', 40)
]

c.executemany('INSERT INTO books (title, author, price) VALUES (?, ?, ?)', books)

conn.commit()
conn.close()