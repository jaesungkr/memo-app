from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'memo-secret'
socketio = SocketIO(app, cors_allowed_origins="*")
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

def get_all_memos():
    with get_db() as conn:
        memos = conn.execute('SELECT * FROM memos ORDER BY created_at DESC, id DESC').fetchall()
    return [dict(m) for m in memos]

@app.route('/')
def index():
    memos = get_all_memos()
    return render_template('index.html', memos=memos)

@socketio.on('add_memo')
def handle_add(data):
    content = data.get('content', '').strip()
    if content:
        with get_db() as conn:
            conn.execute('INSERT INTO memos (content) VALUES (?)', (content,))
        emit('refresh', get_all_memos(), broadcast=True)

@socketio.on('delete_memo')
def handle_delete(data):
    memo_id = data.get('id')
    if memo_id:
        with get_db() as conn:
            conn.execute('DELETE FROM memos WHERE id = ?', (memo_id,))
        emit('refresh', get_all_memos(), broadcast=True)

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)