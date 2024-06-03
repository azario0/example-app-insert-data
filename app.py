# app.py
from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)''')
conn.commit()
conn.close()
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('index.html', users=users)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    # Protect against SQL injection
    name = ''.join([c for c in name if c.isalnum() or c.isspace()])
    email = ''.join([c for c in email if c.isalnum() or c in ['@', '.']])
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    return render_template('success.html', name=name, email=email)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

