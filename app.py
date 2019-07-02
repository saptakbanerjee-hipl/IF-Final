from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

admin = Admin(app, name='Control Panel')

app.config['SECRET_KEY'] = 'thisismysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
        return current_user.is_authenticated

    def not_auth(self):
        return "You are not authorized to use this "


admin.add_view(Controller(Users, db.session))


class User(UserMixin):

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.user_id = None



@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(User == int(user_id)).first()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user)

                return redirect(url_for("index.index"))
            else:
                return "Invalid email or password"
        return render_template("login.html")



@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    new_user = Users(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return "Welcome signup complete"

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("my-profile.html")

@app.route('/dashboard', methods=['GET'])

@app.route('/profile')
@login_required
def profile():
    return render_template('')

@app.route('/motors')
def motors():
    return render_template('choose-motors.html')

@app.route('/myprofile')
@login_required
def myprofile():
    users = Users.query.all()
    return render_template('my-profile.html', users=users)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
