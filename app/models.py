from . import db

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
