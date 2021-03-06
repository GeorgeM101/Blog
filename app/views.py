from flask import abort, render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, PostBlog, UpdateAccountForm
from flask_bcrypt import bcrypt
from app import app, db
from .models import Users, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash,generate_password_hash
import requests



app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    data = requests.get(BASE_URL).json()
    return render_template('home.html', posts=posts, quote=data)


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
        user_email=form.email.data
        user = Users.query.filter_by(email=user_email).first()
        # useremail = user.password
        # checkpassword = check_password_hash()
        if (user):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
   
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data =  current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='prof/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostBlog()
    if form.validate_on_submit():
        # post = Post(title=form.title.data, content=form.content.data)
        new_blog = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_blog)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    
    return render_template('new_post.html', title='Create a blog',form=form, legend='New Blog')


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostBlog()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
     form.title.data = post.title
    form.content.data= post.content
    return render_template('new_post.html', title='Update Post' ,form=form, legend='Update Blog')


@app.route("/delete/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

