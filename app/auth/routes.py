# app/auth/routes.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("Missing username or password.")
            return render_template('register.html'), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.')
            return render_template('register.html'), 400

        try:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully! You can now login.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            # Log the exception or return it in the response for debugging
            flash(f"An error occurred: {str(e)}")
            return render_template('register.html'), 500
    return render_template('register.html')
    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()
    
        if user and user.check_password(password):
            login_user(user, remember=True)  # Optionally add "remember=True" if you want to remember the session
            return redirect(url_for('uploader.upload'))
        else:
            flash('Login failed. Check your username and password.', 'error')
    
    # This line handles the GET request to display the login form
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))
