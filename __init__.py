from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Development
from flask_login import UserMixin, LoginManager

# Create an object of SQL Alchemy called db
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Development)

    db.init_app(app)

    # We need to specify our user loader.
    # A user loader tells Flask-Login how to find a specific user from the ID that is stored in
    # their session cookie.
    # We can add this in our create_app function along with basic init code for Flask-Login.

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Blueprint for the auth routes of the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for the non-auth routes of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # A method to create the table in model.py called users_log
    from models.UsersModel import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    class User(db.Model, UserMixin):
        _tablename_ = 'users_log'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(500))

    @app.before_first_request
    def create_table():
        db.create_all()

    if __name__ == '__main__':
        app.run()

    return app
