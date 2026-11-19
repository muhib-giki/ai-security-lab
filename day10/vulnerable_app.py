import sqlite3
import secrets

from flask import Flask, request, make_response

app = Flask(__name__)

SESSIONS = {}      # session id -> username

def setup_database():
    db = sqlite3.connect("day10/app.db")
    db.execute("DROP TABLE IF EXISTS notes")
    db.execute("CREATE TABLE notes (id INTEGER, owner TEXT, content TEXT)")
    db.execute("INSERT INTO notes VALUES (1, 'muhib', 'Muhib private: my bank PIN is 1234')")
    db.execute("INSERT INTO notes VALUES (2, 'alice', 'Alice private: my diary password')")
    db.execute("INSERT INTO notes VALUES (3, 'admin', 'Admin private: master key is XYZ')")
    db.commit()
    db.close()


@app.route("/login/<username>")
def login(username):
    session_id = secrets.token_hex(16)
    SESSIONS[session_id] = username
    resp = make_response(f"Logged in as {username}. Go to /note/<id>")
    resp.set_cookie("session_id", session_id)
    return resp

@app.route("/note/<int:note_id>")
def view_note(note_id):
    username = SESSIONS.get(request.cookies.get("session_id"))
    if not username:
        return "Please log in first", 401

    db = sqlite3.connect("day10/app.db")
    row = db.execute("Select owner, content from notes where id = ?", (note_id,)).fetchone()
    db.close()

    if not row:
        return "Note not found", 404

    owner, content = row 
    owner, content = row
    if owner != username:
        return "Forbidden", 403        # <-- the missing check
    return f"<h3>Note #{note_id}</h3><p>Owner: {owner}</p><p>{content}</p>"


@app.route("/admin")
def admin_panel():
    username = SESSIONS.get(request.cookies.get("session_id"))
    if not username:
        return "Please log in first", 401

    # The UI only shows this page's controls to admin... supposedly
    if username != "admin":
        return "You are not an admin.", 403

    return """
    <h3>Admin Panel</h3>
    <form method="POST" action="/delete-note">
      <input name="note_id" placeholder="Note ID to delete">
      <button>Delete note</button>
    </form>
    """


@app.route("/delete-note", methods=["POST"])
def delete_note():
    username = SESSIONS.get(request.cookies.get("session_id"))
    if not username:
        return "Please log in first", 401
    if username != "admin":
        return "Forbidden: admins only", 403     # <-- the missing check, on the ACTION
    
    note_id = request.form.get("note_id")
    db = sqlite3.connect("day10/app.db")
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    db.close()
    print(f"!!! Note {note_id} deleted by {username} !!!")
    return f"Note {note_id} deleted."


if __name__ == "__main__":
    setup_database()
    app.run(port=5000, debug=True)