import requests
import urllib3
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_tata_metalics'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class Motors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    temperature = db.Column(db.Integer, unique=True)
    specification = db.Column(db.Integer, unique=True)
    current = db.Column(db.Integer, unique=True)
    rpm = db.Column(db.Integer, unique=True)
    vibration = db.Column(db.Integer, unique=True)
    voltage = db.Column(db.Integer, unique=True)

    def __init__(self, id, name, temperature, specification, current, rpm, vibration, voltage):
        self.id = id
        self.name = name
        self.temperature = temperature
        self.specification = specification
        self.current = current
        self.rpm = rpm
        self.vibration = vibration
        self.voltage = voltage


##class User_role(db.Model):
    ##id = db.Column(db.Integer, primary_key=True)
    ##name = db.Column(db.String(15), unique=True)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('profile'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/user-management')
@login_required
def management():
    return render_template('user-management.html')

@app.route('/role-management')
@login_required
def role():
    return render_template('role-management.html')

@app.route('/by-pass-line')
@login_required
def bypassline():
    return render_template('choose-bypass-line.html')

@app.route('/status')
@login_required
def status():
    return render_template('bypass-line-status.html')


@app.route('/choose-motors')
@login_required
def motors():
    return render_template('choose-motors.html')

@app.route('/current')
@login_required
def current():
    return render_template('current.html')

@app.route('/voltage')
@login_required
def voltage():
    return render_template('voltage.html')

@app.route('/temperature',methods = ['POST', 'GET'])
@login_required
def temperature():
    req = requests.get('https://api.thingspeak.com/channels/749546/feeds.json?api_key=ABOY5XYP3Z83KB28&results')

    data = {
        'field1': 'temp'

        'field2', 'pressure': ''
    }

    d = dict(req.json())
    #print(d)
    #print(d.get('feeds'))
    f1 = []
    f2 = []
    for x in d.get('feeds'):
        field1 = x.get('field1')
        field2 = x.get('field2')
        #print("Field 1 : "+field1+" Field 2 : "+field2)
        f1.append(field1)
        f2.append(field2)
    return render_template('temperature.html', thingspeak_data=field1, data=field2)


@app.route('/rpm')
@login_required
def rpm():
    return render_template('rpm.html')

@app.route('/raise-issue')
@login_required
def issue():
    return render_template('raise-issue.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/manage-motors')
@login_required
def managemotors():
    return render_template('manage-motors.html')

@app.route('/manage-plants')
@login_required
def plants():
    return render_template('manage-plant.html')

@app.route('/specifications')
@login_required
def specifications():
    return render_template('motor-specification.html')

@app.route('/notifications')
@login_required
def notifications():
    return render_template('manage-notifications.html')

@app.route('/tickets')
@login_required
def tickets():
    return render_template('tickets.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/ticket-status')
@login_required
def tikstatus():
    return render_template('tickets-status.html')

@app.route('/forgot-password')
@login_required
def password():
    return render_template('forgot-password.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(id=6, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('profile.html', form=form)

    return render_template('signup.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
