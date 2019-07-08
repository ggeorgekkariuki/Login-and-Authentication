# Basically, a flask blueprint is a way for you to organize your flask application into smaller
# and re-usable application.
# Just like a normal flask application, a blueprint defines a collection of views, templates
# and static assets.

# We'll have routes to retrieve both the login page (/login) and signup page (/signup).
# We'll also have routes for handling the POST request from both of those two routes.
# Finally, we'll have a logout route (/logout) to logout an active user.

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.UsersModel import User
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

    # We will compare the email address entered to see if it's in the database
    user = User.query.filter_by(email=email).first()

    # If the user whose email was used, does not exist and the hashed password is not the same
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    # If the user exists and the passwords match
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

    #     Create a User model object and ensure there is only one unique email exists
    user = User.query.filter_by(email=email).first()

    # If the email exists, redirect to the signup page
    if user:
        flash('Email already exists')
        return redirect(url_for('auth.signup'))

    # If the user's email is unique, add the new user to the database
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'),
                    name=name)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

