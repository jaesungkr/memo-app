# Memo App

A small shared memo board built with Flask, Flask-SocketIO, and SQLite. Notes added or deleted in one browser are broadcast to connected clients.

## Features

- Add and delete text notes.
- Show notes with creation timestamps.
- Store notes in a local SQLite database.
- Update connected browsers without a page reload.

The interface is currently in Korean. Save with **Ctrl+Enter** on Windows/Linux or **Cmd+Enter** on macOS. Plain Enter inserts a newline; the shortcut does not submit during IME composition.

## Run locally

Use Python 3.12, matching the included Dockerfile, and an isolated Python environment.

```bash
git clone https://github.com/jaesungkr/memo-app.git
cd memo-app
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start a loopback-only development server:

```bash
python -m pip install -r requirements.txt
python -c "from app import app, init_db, socketio; init_db(); socketio.run(app, host='127.0.0.1', port=5000, debug=False, allow_unsafe_werkzeug=True)"
```

Open **http://127.0.0.1:5000**. The browser loads the Socket.IO client from a CDN.

## Storage

The app creates `memo.db` in the working directory. Keep a backup before removing the directory or moving the app. All connected clients share the same notes.

## Files

| File | Purpose |
|---|---|
| [app.py](app.py) | Database helpers, page route, and Socket.IO events |
| [templates/index.html](templates/index.html) | Memo interface and browser event handlers |
| [requirements.txt](requirements.txt) | Python dependencies |
| [Dockerfile](Dockerfile) | Python 3.12 container configuration |

## Scope

This is a personal prototype, not a private or production-ready notes service. It has no authentication, and live note updates insert content as HTML. Use only trusted sample text and keep it local. The default `python app.py` entry point enables debugging and listens on all interfaces; the command above avoids those defaults.

## Shortcut tests

With Node.js installed, run `node --test tests/keyboard-shortcut.test.cjs`. These dependency-free tests execute the template script with DOM and Socket.IO stubs; they do not replace browser or server integration testing.
