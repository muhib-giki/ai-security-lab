import sqlite3
from flask import Flask, request

app = Flask(__name__)


def setup():
    db = sqlite3.connect("phase1/shop.db")
    db.execute("DROP TABLE IF EXISTS books")
    db.execute("CREATE TABLE books (id INTEGER, title TEXT, author TEXT, price TEXT, secret TEXT)")
    rows = [
        (1, "The Pragmatic Programmer", "Hunt & Thomas", "45", "-"),
        (2, "Clean Code", "Robert Martin", "40", "-"),
        (3, "The Web Application Hacker's Handbook", "Stuttard & Pinto", "55", "-"),
        (4, "INTERNAL - staff pricing sheet", "internal", "0", "COUPON-9X3K-STAFF50"),
    ]
    for r in rows:
        db.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)", r)
    db.commit()
    db.close()


@app.route("/")
def home():
    return """
    <h2>BookNook</h2>
    <form action="/search">
      <input name="q" placeholder="Search books by title" style="width:320px">
      <button>Search</button>
    </form>
    """


@app.route("/search")
def search():
    q = request.args.get("q", "")
    db = sqlite3.connect("phase1/shop.db")
    query = "SELECT id, title, author, price FROM books WHERE title LIKE '%" + q + "%'"
    try:
        rows = db.execute(query).fetchall()
    except Exception as e:
        db.close()
        return f"<pre>Error: {e}</pre>"
    db.close()
    out = "<h3>Results</h3>"
    for r in rows:
        out += f"<div>#{r[0]} - {r[1]} by {r[2]} (${r[3]})</div>"
    out += '<p><a href="/">back</a></p>'
    return out


@app.route("/book/<int:book_id>")
def book(book_id):
    db = sqlite3.connect("phase1/shop.db")
    row = db.execute("SELECT title, author, price FROM books WHERE id = ?", (book_id,)).fetchone()
    db.close()
    if not row:
        return "Not found", 404
    return f"<h3>{row[0]}</h3><p>by {row[1]} - ${row[2]}</p>"


if __name__ == "__main__":
    setup()
    app.run(port=5000, debug=True)