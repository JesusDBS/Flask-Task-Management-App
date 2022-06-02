from flask import Flask, make_response, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 


app = Flask(__name__)
app.config['SECRET_KEY'] = "Super Secret String"

bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    old_name = session.get('name')
    if form.validate_on_submit():
        if old_name is not None and old_name != form.name.data:
            flash("You changed your name!")
        session['name'] = form.name.data 
        
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
        name=session.get('name'))

@app.route('/todos/<todos>')
def todos(todos):
    tasks_list = [todo for todo in todos.split(' ') if todo]

    if len(tasks_list) >= 1:
        
        return render_template('todos.html', todos=tasks_list)

@app.route('/done')
def done():
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template("about.html")
