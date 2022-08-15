from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
        
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            user = User(email, password=password)
            
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('site.home'))
        
    except:
        raise Exception('Invalid Form Data: Please check your form')
    
    return render_template('signup.html', title='Sign Up', form = form) 

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            user = User.query.filter(User.email == email).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('site.profile'))
                else:

                    return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('signin.html', form=form, title="Sign In")

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))