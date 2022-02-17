from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,PasswordField,BooleanField,SubmitField, TextAreaField
from .models import Users
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_field(self,username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already exists')

    def validate_field(self,email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostBlog(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png'])])
    submit = SubmitField('Update')