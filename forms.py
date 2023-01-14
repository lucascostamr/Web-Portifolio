from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField, TextAreaField, PasswordField, URLField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField, CKEditor


# FLASK WTF
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    mail_text = TextAreaField('Message', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Send Email')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Tolken', validators=[DataRequired()])
    recaptcha= RecaptchaField()
    submit = SubmitField('Login in')


class AddProject(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    description = CKEditorField('Description', validators=[DataRequired()])
    sub_description = StringField('Sub Description', validators=[DataRequired()])
    image_url = URLField('Project Image URL', validators=[DataRequired()])
    source_code_url = URLField('Source Code URL', validators=[DataRequired()])
    recaptcha= RecaptchaField()
    submit = SubmitField('Add Project')


class EditAbout(FlaskForm):
    text = CKEditorField('Text', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditSKills(FlaskForm):
    softskillText = TextAreaField('SOFTSKILL', validators=[DataRequired()])
    hardskillText = TextAreaField('HARDSKILL', validators=[DataRequired()])
    submit = SubmitField('Save')
