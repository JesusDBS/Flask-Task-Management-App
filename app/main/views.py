from datetime import datetime
from flask import Flask, make_response, render_template, redirect, url_for, session, flash
from . import main
from .forms import NameForm
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