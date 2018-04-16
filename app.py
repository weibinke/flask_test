from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import time

app = Flask(__name__, instance_relative_config=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/users.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:weibin@119.28.135.135:3306/test_flask?charset=utf8mb4'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.secret_key = '123456'

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
admin = Admin(app, name = app.config['ADMIN_TITLE'], template_mode='bootstrap3')


class User(db.Model):
    """......"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


admin.add_view(ModelView(User, db.session))

@app.route("/")
def index():
    return "Hello world!"

@app.route("/hello")
def hello():
    t = time.time()
    maxid = db.session.query(User).order_by(User.id.desc()).first()
    if maxid:
        newid = maxid.id + 1
    else:
        newid = 1
    u = User(username='testname_%d' % (newid),email='test@qq.com_%d' % (newid))
    db.session.add(u)
    db.session.commit()
    return "Hello hello user:%s" % (u.username)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=80)

