from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .validator import UserModel
from sqlalchemy.exc import IntegrityError
from . import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username_email = request.form.get('username_email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=username_email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=remember)  # Login the user
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid password')
    else:
        user = User.query.filter_by(username=username_email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=remember)  # Login the user
                return redirect(url_for('main.profile'))
            else:
                flash('Invalid password')
        else:
            flash('Invalid email or username')

    return redirect(url_for('auth.login'))

@auth.route('/signin')
def signin():
    return render_template('signin.html')

@auth.route('/signin', methods=['POST'])
def signin_post():
    try:
        user_data = UserModel(**request.form)
        user = User(**user_data.dict())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    except ValueError as e:
        errors = e.errors()
        flash(errors)
        return redirect(url_for('auth.signin'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
