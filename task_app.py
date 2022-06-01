from flask import Flask
from flask import make_response, render_template, redirect, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos/<todos>')
def todos(todos):
    tasks_list = [todo for todo in todos.split(' ') if todo]

    if len(tasks_list) >= 1:
        
        return render_template('todos.html', todos=tasks_list)

@app.route('/done')
def done():
    return redirect(url_for('index'))
