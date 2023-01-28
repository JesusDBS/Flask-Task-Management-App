from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from . import main
from .forms import TaskForm
# from .. import db
from ..models import Tasks


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))
    return redirect(url_for('auth.login'))


@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    tasks = Tasks.get_tasks()
    context = {
        'form': form,
        'tasks': tasks,
    }

    if form.validate_on_submit():
        description = form.description.data
        task = Tasks.get_task_by_description(description)
        if not task:
            Tasks.add_task(description)
            flash('Your task were created succesfully')
        else:
            flash('This task already exists. Try another one!')

        return redirect(url_for('.index'))
    return render_template('index.html', **context)
