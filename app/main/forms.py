from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    description = StringField(
        "Task description", validators=[DataRequired()])
    submit = SubmitField("Submit")


class Delete(FlaskForm):
    submit = SubmitField('Delete')


class UpDate(FlaskForm):
    submit = SubmitField('Update')
