from flask import Flask, render_template, request, redirect, url_for
import _sqlite3 as sq

app = Flask(__name__)

def get_db():
    conn = sq.connect('todo.sqlite3')
    conn.row_factory = sq.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    rows = cur.fetchall()
    conn.close()
    return render_template('index.html', todos=rows)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (title, done) VALUES (?, ?)', (title, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
