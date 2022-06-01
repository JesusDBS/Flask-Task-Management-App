from flask import Flask
from flask import make_response, render_template, redirect, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

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
