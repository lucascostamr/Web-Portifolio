from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField, CKEditor

WTF_CSRF_SECRET_KEY='key'
RECAPTCHA_PUBLIC_KEY = "6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J"
RECAPTCHA_PRIVATE_KEY = "6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu"

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    mail_text= TextAreaField('Message', validators=[DataRequired()])
    recaptcha= RecaptchaField()
    submit= SubmitField('Send Email')


app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)
CKEditor(app)

projectName= 'Test Name'



@app.route("/", methods=['POST', 'GET'])
def home():
    mail_sent=False
    complete_email=None
    form = ContactForm(meta={'csrf': False})
    if form.validate_on_submit():
        mail_sent=True

        complete_email = {
            "name": form.name.data,
            "email": form.email.data,
            "mailText": form.mail_text.data,
        }

    return render_template('index.html', form=form, mail_text=form.mail_text, mail_sent=mail_sent)


@app.route("/projects")
def projects():
    return render_template("projects.html")


if __name__ == '__main__':
    app.run(debug=True)
