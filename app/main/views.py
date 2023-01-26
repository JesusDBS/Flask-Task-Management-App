from flask import render_template, redirect, url_for
from flask_login import current_user
from . import main
# from .forms import NameForm, TaskForm
from .. import db
# from ..models import User


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('auth.login'))
