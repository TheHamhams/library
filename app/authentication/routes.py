from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import UserLoginForm
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
        
    return render_template('signup.html', title='Sign Up', form = form) 