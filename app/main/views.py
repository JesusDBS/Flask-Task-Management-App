from datetime import datetime
from flask import Flask, make_response, render_template, redirect, url_for, session, flash
from . import main
from .forms import NameForm, TaskForm
from ..import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    context = {
        'form': form,
        'name': session.get('name'),
        'known': session.get('known', False)
    }
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()

        if user:
            flash("Great to see you again!")
            session['known'] = True

        else:
            flash("Welcome here you can manage your tasks!")
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

        session['name'] = form.name.data
        return redirect(url_for('.index'))

    return render_template('index.html', **context)

@main.route('/todos', methods=['GET', 'POST'])
def todos():
    form = TaskForm()
    name = session.get('name')
    context = {
        'form': form,
        'name': name,
        'todos': session.get('task_list')
    }

    if form.validate_on_submit():
        session['task_list'] = [
            todo for todo in form.todos.data.split(' ') if todo]
        return redirect(url_for('.todos'))

    return render_template('todos.html', **context)


@main.route('/done')
def done():
    return redirect(url_for('.index'))


@main.route('/about')
def about():
    return render_template("about.html")