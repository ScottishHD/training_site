from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, SubmitField, ValidationError, TextAreaField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class CreateCourseForm(FlaskForm):
    course_title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    # Could we suggest modules based on what is entered,  using ajax