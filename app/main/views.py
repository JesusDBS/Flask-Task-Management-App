from datetime import datetime
from flask import Flask, make_response, render_template, redirect, url_for, session, flash
from . import main
from .forms import NameForm, TaskForm
from .. import db
from ..models import User


@main.route('/')
def index():
    return render_template('index.html')
