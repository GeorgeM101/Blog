from flask import Flask, render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, PostBlog
from flask_bcrypt import bcrypt
from app import app, db
from .models import Users, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash,generate_password_hash

import os
import secrets



app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data,password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/post/new", methods=['GET','POST'])
def new_post():
    form = PostBlog()
    if form.validate_on_submit():
        # post = Post(title=form.title.data, content=form.content.data)
        new_blog = Post(title=form.title.data, content=form.content.data, user_id=1)
        db.session.add(new_blog)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='Create a blog',form=form)

# @app.route('/new_user')
# def new_user():
#     user_email = 'tests@gmail.com'
#     username = 'Leroy'
#     image_file = 'tests.jpg'
#     password = generate_password_hash('tests')
#     new_user = Users( username=username,email=user_email, image_file=image_file, password=password)
#     db.session.add(new_user)
#     db.session.commit()
#     return redirect(request.referrer)