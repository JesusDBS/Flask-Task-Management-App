import os
from flask import Flask, make_response, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 

#App Config-------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "Super Secret String"
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'tasks.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

#WTForm classes---------------------------------
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class TaskForm(FlaskForm):
    todos = StringField("Insert your tasks separate by blank space", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Models----------------------------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    tasks = db.relationship('Tasks', backref='task_ids', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), unique=True)
    done = db.Column(db.Boolean, default=False)
    user_ids = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Tasks %r>' % self.name

#Ingetration with shell------------------------
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Tasks=Tasks)

#Error handlers---------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#Routes-----------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    old_name = session.get('name')
    context = {
        'form': form,
        'name': session.get('name')
    }
    if form.validate_on_submit():
        if old_name is not None and old_name != form.name.data:
            flash("You changed your name!")
            session['task_list'] = ''

        session['name'] = form.name.data 
        return redirect(url_for('index'))

    return render_template('index.html', **context)

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    form = TaskForm()
    name = session.get('name')
    context = {
            'form': form,
            'name': name,
            'todos': session.get('task_list')
    }

    if form.validate_on_submit():
        session['task_list'] = [todo for todo in form.todos.data.split(' ') if todo]
        return redirect(url_for('todos')) 

    return render_template('todos.html', **context)

@app.route('/done')
def done():
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template("about.html")
