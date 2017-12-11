#export ADMIN=alliswanderer@gmail.com MAIL_USERNAME=alliswanderer@gmail.com MAIL_PASSWORD=hello12345
#ALLISON
## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from threading import Thread
from werkzeug import secure_filename
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
import tweepy
from werkzeug.security import generate_password_hash, check_password_hash
import time 
from werkzeug.utils import secure_filename
from flask import send_from_directory, jsonify
import os.path



auth = tweepy.OAuthHandler("Jmp3oFFpbtwAzV1Qx9AEv8CnB", "f3nPvgOjZTVMHh80cqQiBtVPZM58cmrvr0lPz3yyfwoExD4AHZ")
auth.set_access_token("3106532969-R5xaGW5Y5dSqrEtAvRG0xvbv1iDbNNELzBolxRA","UeTRQ58orwMtgJN9E9gUEfMPRfnUYSWcsAzYdc0PfhaXO")
api = tweepy.API(auth)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364(thisisnotsupersecure)'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/alliwan364final"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587 #default
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = '[Tweets App]'
app.config['MAIL_SENDER'] = 'Admin <{}>'.format(os.environ.get('MAIL_USERNAME'))
app.config['ADMIN'] = os.environ.get('MAIL_USERNAME')

manager = Manager(app)
db = SQLAlchemy(app) 
migrate = Migrate(app, db) 
manager.add_command('db', MigrateCommand) 
mail = Mail(app) 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = 'uploaded_images/'
ALLOWED_EXTENSIONS = set(['png'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def make_shell_context():
    return dict(app=app, db=db, Tweet=Tweet, User=User, Hashtag=Hashtag)

manager.add_command("shell", Shell(make_context=make_shell_context))

def getFollowers(twitter_handle, current_user):
    followed_user = api.get_user(twitter_handle)
    fol_user = get_or_create_twitter_user(followed_user.name, followed_user.screen_name, followed_user.location, followed_user.description)
    new_search = Search(user_id=current_user.id, twitter_user_id=fol_user.id, date=time.time())
    db.session.add(new_search)
    db.session.commit()
    data = [{"name" : follower.name, "screen_name" : follower.screen_name, "location" : follower.location, "description": follower.description} for follower in api.followers(twitter_handle)]
    for user in data:
        follower = get_or_create_twitter_user(user["name"], user["screen_name"], user["location"], user["description"])
        connection = get_or_create_twitter_relation(fol_user.id, follower.id)
    return data

def send_this_email(app, msg):
    with app.app_context():
        mail.send(msg)

def sendemailtowhensubmit(to, subject, template, **kwargs): 
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    messagesent = Thread(target=send_this_email, args=[app, msg]) # 
    messagesent.start()
    return messagesent 


#MODELS

class Twitter_User(db.Model):
    __tablename__ = "twitter_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(285))
    screen_name = db.Column(db.String(285), unique=True)
    location = db.Column(db.String(285))
    description = db.Column(db.String(285))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(200))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None


class Search(db.Model):
    __tablename__ = 'searches'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    twitter_user_id = db.Column(db.Integer, db.ForeignKey('twitter_users.id'))
    date = db.Column(db.String(285))

class Twitter_Relation(db.Model):
    __tablename__ = 'twitter_connections'
    id = db.Column(db.Integer, primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('twitter_users.id'))
    id_follower = db.Column(db.Integer, db.ForeignKey('twitter_users.id'))


#Helper Functions

def get_or_create_twitter_user(name, screen_name, location, description):
    twitter_user = db.session.query(Twitter_User).filter_by(screen_name = screen_name).first()
    if twitter_user:
        return twitter_user
    else:
        twitter_user = Twitter_User(name=name, screen_name=screen_name, location=location, description=description)
        db.session.add(twitter_user)
        db.session.commit()
        return twitter_user

def get_or_create_twitter_relation(followed_id, id_follower):
    connection = db.session.query(Twitter_Relation).filter_by(followed_id=followed_id, id_follower=id_follower).first()
    if connection:
        return connection
    else:
        connection = Twitter_Relation(followed_id=followed_id, id_follower=id_follower)
        db.session.add(connection)
        db.session.commit()
        return connection

#ERRORS

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#FORM
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')


class UserSearchForm(FlaskForm):
    twitter_handle = StringField("Enter Twitter username ", validators=[Required()])
    submit = SubmitField('Submit')

#LOG IN VIEWS

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

#OTHER VIEWS

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template("index.html", user=current_user)

@app.route('/search', methods=['GET'])
@login_required
def search():
    form = UserSearchForm()
    return render_template("search.html", user=current_user, form=form)

@app.route('/results', methods=['POST'])
@login_required
def results():
    form = UserSearchForm()
    if form.validate_on_submit():
        sendemailtowhensubmit(current_user.email, "Your New Search", "mail/new_search", data=getFollowers(form.twitter_handle.data, current_user), searchTerm=form.twitter_handle.data)
        return render_template("results.html", data=getFollowers(form.twitter_handle.data, current_user), searchTerm=form.twitter_handle.data)

@app.route('/user/<handle>')
@login_required
def user(handle):
    return render_template("user.html", data=getFollowers(handle, current_user), searchTerm=handle)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(current_user.id) + ".png")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/get_profile_picture")
@login_required
def get_prof_pic():
    return jsonify({
        "hasPic" :  os.path.exists("uploaded_images/{}.png".format(current_user.id))
        })

if __name__ == '__main__':
    db.create_all()
    manager.run()
