from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, SubmitField, ValidationError, TextAreaField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateCourseForm(FlaskForm):
    course_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    # Could we suggest modules based on what is entered,  using ajax
    submit = SubmitField('Create')

class Module(FlaskForm):
    module_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')

class OutcomeForm(FlaskForm):
    content = FileField('Content', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    


class Set(FlaskForm):
    content = FileField('Feature File', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
