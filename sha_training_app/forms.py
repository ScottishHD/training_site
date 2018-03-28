from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField, StringField, SubmitField, IntegerField, TextAreaField, BooleanField, FieldList, \
    FormField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class OrganisationRegisterForm(FlaskForm):
    organisation_name = StringField('Organisation Name', validators=[DataRequired()])
    contact_email = StringField('Assigned Person Email', validators=[DataRequired(), Email()])
    size = IntegerField('Size of Organisation')
    submit = SubmitField('Create Organisation')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# class ModuleListingForm(FlaskForm):
#     title =


class EditCourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    description = TextAreaField('Course Description', validators=[DataRequired()])
    # modules = FieldList('Add Module', FormField(ModuleListingForm))
    submit = SubmitField('Apply')


class DeleteCourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    submit = SubmitField('Delete Course')


class CreateCourseForm(FlaskForm):
    course_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Header Image', validators=[DataRequired()])
    submit = SubmitField('Create')


class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])


class ModuleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    number_of_questions = IntegerField('Number of questions')
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    false_answers = TextAreaField('False Answers')
    submit = SubmitField('Create')


class OutcomeForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    external_link = BooleanField('External Video')
    resource = FileField('Resource File')
    location = StringField('External URL')
    submit = SubmitField('Create')
