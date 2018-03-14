from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, SubmitField, IntegerField, TextAreaField, BooleanField, FileField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EditCourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    description = TextAreaField('Course Description', validators=[DataRequired()])
    submit = SubmitField('Apply')


class DeleteCourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    submit = SubmitField('Delete Course')


class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])


class CreateCourseForm(FlaskForm):
    course_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    # Could we suggest modules based on what is entered,  using ajax
    submit = SubmitField('Create')

class Module(FlaskForm):
    module_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    number_of_questions = IntegerField('Number of questions')
    questions = FieldList(FormField(QuestionForm))
    submit = SubmitField('Create')

class OutcomeForm(FlaskForm):
    content = FileField('Content', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])