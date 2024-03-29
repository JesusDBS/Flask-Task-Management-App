from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    tasks = db.relationship('Tasks', backref='task_ids', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @staticmethod
    def add_user(email, username, password):
        user = User(email=email,
                    username=username,
                    password=password)
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), unique=True)
    done = db.Column(db.Boolean, default=False)
    user_ids = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def get_tasks():
        tasks = current_user.tasks
        return tasks

    @staticmethod
    def get_task_by_description(description):
        task = Tasks.query.filter_by(description=description).first()
        if task:
            return task
        return None

    @staticmethod
    def add_task(description, done=False):
        new_task = Tasks(description=description, done=done,
                         user_ids=current_user.id)
        db.session.add(new_task)
        db.session.commit()

    @staticmethod
    def delete_task(task_id):
        task_deleted = Tasks.query.filter_by(
            id=int(task_id), user_ids=current_user.id).first()
        db.session.delete(task_deleted)
        db.session.commit()
        return task_deleted

    @staticmethod
    def update_task(task_id):
        task_update = Tasks.query.filter_by(
            id=int(task_id), user_ids=current_user.id).first()
        task_update.done = False if task_update.done else True
        db.session.commit()

    def __repr__(self):
        return '<Tasks %r>' % self.name
