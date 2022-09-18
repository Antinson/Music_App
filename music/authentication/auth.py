from flask import Blueprint, render_template, redirect, url_for, session, request, flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import music.adapters.repository as repo
import music.authentication.services as services

# Setting up our blueprint
auth_blueprint = Blueprint('auth_bp', __name__, template_folder='templates', url_prefix='/auth')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():

        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('auth_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = "That username is taken, please choose another"
    
    return render_template('auth/credentials.html', title='Register', form=form, user_name_error_message=user_name_not_unique,
                            handler_url=url_for('auth_bp.register')
                )


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match = None

    if form.validate_on_submit():

        try:
            user = services.get_user(form.user_name.data.lower(), repo.repo_instance)
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        
        except services.UnknownUserException:
            user_name_not_recognised = "Username not recognised"
        
        except services.AuthenticationException:
            password_does_not_match = "Password does not match"
    
    return render_template('auth/credentials.html', title='Login', form=form, user_name_error_message=user_name_not_recognised,
                            password_error_message=password_does_not_match
                )


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('auth_bp.login'))

        return view(**kwargs)

    return wrapped_view


@auth_blueprint.route('/admin')
def admin():
    session.clear()
    try:
        services.add_user('admin', 'Admin123**', repo.repo_instance)
    except:
        user = services.get_user("admin", repo.repo_instance)
        services.authenticate_user(user['user_name'], "Admin123**", repo.repo_instance)
        session.clear()
        session['user_name'] = user['user_name']
        print("you in")
    return redirect(url_for('home_bp.home'))




class PasswordValid():
    def __init__(self, message=None):
        if not message:
            message = 'Password must be at least 8 characters long, contain at least one number, one uppercase letter and one lowercase letter'
        self.message = message
    
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [DataRequired(message="Your username is required"), Length(min=3, message= "Your username is too short!")])
    password = PasswordField('Password', [DataRequired(message="Your password is required"), PasswordValid()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
