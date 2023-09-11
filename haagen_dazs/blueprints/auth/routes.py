from flask import Blueprint, render_template, redirect, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

from haagen_dazs.forms import RegisterForm, LoginForm
from haagen_dazs.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate_on_submit():

        first = register_form.first.data
        last = register_form.last.data
        username = register_form.username.data
        email = register_form.username.data
        password = register_form.username.data
        profile_image = register_form.profile_image.data
        p_number = register_form.p_number.data

        #check the database for same username and/or email
        if User.query.filter(User.username == username).first():
            flash('Username already exists. Please try again', category='warning')
            return redirect('/signup')
        
        if User.query.filter(User.email == email).first():
            flash('Email address is already in use.  Please try again', category='warning')
            return redirect('/signup')
        
        user = User(username, password, email, p_number, first, last, profile_image)
        db.session.add(User)
        db.session.commit()

        flash(f"You have successfully registered user {username}", category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=register_form)



@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    
    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Successfully logged in user {email}', category='success')
            return redirect('/')
        else:
            flash(f'Invalid Email and/or Password.  Please try again', category='warning')
            return redirect('signin')
        
    return render_template('sign_in.html', form=login_form)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')