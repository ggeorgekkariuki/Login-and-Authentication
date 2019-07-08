# Basically, a flask blueprint is a way for you to organize your flask application into smaller
# and re-usable application.
# Just like a normal flask application, a blueprint defines a collection of views, templates
# and static assets.

# For our main blueprint, we'll have a home page (/)
# and profile page (/profile) for after we log in.
# If the user tries to access the profile page without being logged in,
# they'll be sent to our login route.


from flask import Blueprint, render_template, redirect, request, url_for
from models.UsersModel import User
from flask_login import current_user, login_required
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

# To protect a page when using Flask-Login is very simple:
# we add the @login_required decorator between the route and the function.
# This will prevent a user who isn't logged in from seeing the route.
# If the user isn't logged in, the user will get redirected to the login page,
# per the Flask-Login configuration.


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
