from flask import Flask, render_template, request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user, logout_user, login_required,login_manager
# from flask_loginmanager import
from flask_mysqldb import MySQL
from flask_mail import Mail
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import json
import math
import os
import re
import MySQLdb.cursors

with open('config.json','r') as c:
    params = json.load(c)['params']


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'photocontest3'

local_server = True
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)
mysql = MySQL(app)
class Accounts(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)

class Register(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(20), nullable=False)
    image_id = db.Column(db.String(50), nullable=False)
    image_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(100), nullable=False)

class Contestinfo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    theme = db.Column(db.String(80), nullable=False)
    startedon = db.Column(db.String(12), nullable=True)
    endson = db.Column(db.String(12), nullable=True)
    slug = db.Column(db.String(100), nullable=False)

class Vote_count(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(80), nullable=False)
    vote = db.Column(db.String(80), nullable=False)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(120), nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/result", methods = ['GET', 'POST'])
def result():
    likes = {}
    vote = {}
    register = Register.query.filter_by().all()


    if params['result_day'] == True:
        for i in register:
            vote[i.username] = Vote_count.query.filter_by(vote=i.username).count()

        no_of_likes = max(vote.values())
        for i in vote.keys():
            if vote[i] == no_of_likes:
                name = i

        for i in register:
            if i.username == name:
                email = i.email
                image_id = i.image_id

        return render_template("result_final.html", name=name, no_of_likes=no_of_likes, email=email, image_id=image_id,
                               register=register)
    for i in register:
        vote[i.username] = Vote_count.query.filter_by(vote=i.username).count()
        # likes[i.username] = vote[i]
    print(vote)
    return render_template("result.html",register=register,vote=vote)


@app.route("/register", methods = ['GET', 'POST'])
def register():
     msg=''
     color = ''
     if (request.method == 'POST'):
        username = request.form.get('username')
        email = request.form.get('email')
        description = request.form.get('description')
        image_id = request.form.get('image_id')
        image_name = request.form.get('image_name')
        slug = request.form.get('image_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE username = %s AND email = %s', (username,email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!Try another username'
            color = '#c0232c'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            color = '#c0232c'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            color = '#c0232c'
        elif not username or not image_id or not email or not image_name or not description:
            msg = 'Please fill out the form!'
            color = '#c0232c'
        else:
            entry = Register(username=username, email=email,description=description,image_id=image_id,image_name=image_name,slug=slug)
            db.session.add(entry)
            db.session.commit()
            msg = 'You have successfully registered!'
            color = '#037d50'
     return render_template("register.html",msg=msg,colour=color)

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/vote")

def vote():
    msg = ''
    if 'loggedin' in session:
        register = Register.query.filter_by().all()
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('vote.html', username=session['username'],register=register,account=account,msg=msg)
    return redirect(url_for('ulogin'))

@app.route("/contest", methods = ['GET', 'POST'])
def contest():
    if (request.method == 'POST'):
            name = request.form.get('name')
            theme = request.form.get('theme')
            startedon = request.form.get('startson')
            endson = request.form.get('endson')
            slug = request.form.get('name')
            entry = Contestinfo(name=name, theme=theme, startedon=startedon, endson=endson,slug=slug)
            db.session.add(entry)
            db.session.commit()
    return render_template("contest.html")

@app.route("/edit", methods = ['GET', 'POST'])
def edit():
    return render_template("edit.html")

@app.route("/ulogin", methods = ['GET', 'POST'])
def ulogin():
    msg = ''
    color = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('vote'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            color = '#c0232c'
    return render_template("ulogin.html",msg=msg,colour=color)
@app.route("/uregister", methods = ['GET', 'POST'])
def uregister():
    # Output message if something goes wrong...
    msg = ''
    color = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            color = '#c0232c'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            color = '#c0232c'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            color = '#c0232c'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
            color = '#c0232c'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            color = '#037d50'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        color = '#c0232c'
    # Show registration form with message (if any)
    return render_template('uregister.html', msg=msg , colour=color)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('ulogin'))

@app.route('/votebutton',methods = ['GET', 'POST'])
def votebutton():
    msg = ''
    color = ''
    vote_count = Vote_count.query.filter_by().all()
    for v in vote_count:
        if v.user_email == session['email']:
           #############################################################################################################
            register = Register.query.filter_by().all()
           # User is loggedin show them the home page
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
            account = cursor.fetchone()
            msg = "You Have Already Voted"
            color = '#c0232c'
            return render_template('vote.html', username=session['username'], register=register, account=account,msg=msg)
           #############################################################################################################
            # return "You Have Already Voted"
    name = request.form.get('voter')
    entry = Vote_count(vote=name[6:],user_email=session['email'])
    db.session.add(entry)
    db.session.commit()
    #############################################################################################################
    register = Register.query.filter_by().all()
    # User is loggedin show them the home page
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    msg = "Votted Successfully"
    color = '#037d50'
    return render_template('vote.html', username=session['username'], register=register, account=account, msg=msg, colour=color)
    #############################################################################################################
    # return "Voted Successfully"

@app.route('/contact',methods = ['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('phone')
        message = request.form.get('message')

        entry = Contact(name=name,email=email,phone_num=phone_num,message=message)
        db.session.add(entry)
        db.session.commit()

    return render_template("contact-us.html")

@app.route('/about',methods = ['GET', 'POST'])
def about():

    return render_template("about.html")

app.run(debug=True)