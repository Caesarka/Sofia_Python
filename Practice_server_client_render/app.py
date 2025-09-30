from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# -------- СЕРВЕРНЫЙ РЕНДЕРИНГ ----------
@app.route('/books-server')
def books_server():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('books_server.html', books=books)

# -------- API ДЛЯ КЛИЕНТСКОГО ----------
@app.route('/api/books')
def books_api():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(row) for row in books])

# -------- КЛИЕНТСКИЙ РЕНДЕРИНГ ----------
@app.route('/books-client')
def books_client():
    return render_template('books_client.html')

if __name__ == '__main__':
    app.run(debug=True)