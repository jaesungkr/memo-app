from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'memo.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/')
def index():
    with get_db() as conn:
        memos = conn.execute('SELECT * FROM memos ORDER BY created_at DESC').fetchall()
    return render_template('index.html', memos=memos)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    if content:
        with get_db() as conn:
            conn.execute('INSERT INTO memos (content) VALUES (?)', (content,))
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    with get_db() as conn:
        conn.execute('DELETE FROM memos WHERE id = ?', (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)