import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Retrieve form data
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    
    # Insert into database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()
    
    return render_template("result.html", name=name, email=email, message=message)

@app.route("/messages")
def messages():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return render_template("messages.html", messages=rows)

@app.route("/edit/<int:message_id>")
def edit(message_id):
    # Retrieve the message by ID
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message FROM messages WHERE id = ?", (message_id,))
    message = cursor.fetchone()
    conn.close()
    return render_template("edit.html", id=message[0], name=message[1], email=message[2], message=message[3])

@app.route("/update/<int:message_id>", methods=["POST"])
def update(message_id):
    # Retrieve updated data from the form
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    
    # Update the database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE messages
        SET name = ?, email = ?, message = ?
        WHERE id = ?
    """, (name, email, message, message_id))
    conn.commit()
    conn.close()
    
    return redirect(url_for("messages"))

@app.route("/delete/<int:message_id>")
def delete(message_id):
    # Retrieve the message by ID
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message FROM messages WHERE id = ?", (message_id,))
    message = cursor.fetchone()
    conn.close()
    return render_template("delete.html", id=message[0], name=message[1], email=message[2], message=message[3])

@app.route("/confirm/<int:message_id>", methods=["POST"])
def confirm(message_id):
    # Delete the message by ID
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM messages
        WHERE id = ?
    """, (message_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("messages"))
  

if __name__ == "__main__":
    init_db()  # Initialize the database on startup
    app.run(debug=True)

