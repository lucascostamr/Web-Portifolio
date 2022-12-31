from flask import Flask, render_template, url_for, redirect, abort, flash, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from forms import *
from sendEmail import NotificationManager

# FlaskWTF
WTF_CSRF_SECRET_KEY = '6LeYIbsSAAAAACRPIllx'
RECAPTCHA_PUBLIC_KEY = "6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J"
RECAPTCHA_PRIVATE_KEY = "6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu"

# Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '6LeYIbsSAAAAACRPIllx'

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website-data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)
CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# SQLALCHEMY TABLES
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    profile_picture_url = db.Column(db.String(1000), nullable=False)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    sub_description = db.Column(db.String(100), nullable=False)  # RECRIAR TABLE NO DB
    image_url = db.Column(db.String(1000), nullable=False)
    source_code_url = db.Column(db.String(1000), unique=True, nullable=False)

class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_type = db.Column(db.String(10), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)

class AboutText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), unique=True, nullable=False)

# LEMBRAR DE COLOCAR AVISOS CASO OS PARAMETOS DO DB SEJAM IGUAIS

# admin = User(email='lucascostamr812@gmail.com', password=generate_password_hash('147874@', method='pbkdf2:sha256', salt_length=8), profile_picture_url="")
# softskill = Skills(skill_type='softskill', skill_name='Great Comunicator,Teamwork,Work under pressure')
# hardskill = Skills(skill_type='hardskill', skill_name='Language:Python,Java;Framework:Flask,Bootstrap,Selenium')
# CRIAR AS SKILLS (SOFT AND HARD) NO DB E DEPOIS TESTAR A PARTE DAS SKILLS
# text =AboutText(text= "I'm a Brazilian, who loves technology, music, games and I'm also a student of Information Systems who decided to be a Developer to offer more accessible technology to society.")
# with app.app_context():
#     db.create_all()
#     db.session.add(admin)
#     db.session.add(softskill)
#     db.session.add(hardskill)
#     db.session.add(text)
#     db.session.commit()
    # pass


# FLASK APP
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id != 1:
                return abort(403)
        except AttributeError:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=['POST', 'GET'])
def home():
    mail_sent = False
    projects = Projects.query.all()
    form = ContactForm(meta={'csrf': False})
    about_text = AboutText.query.all()
    user = User.query.filter_by(id=1).first()

    softskills = ((Skills.query.filter_by(
        skill_type='softskill').first()).skill_name).split(',')
    hardskills = ((Skills.query.filter_by(
        skill_type='hardskill').first()).skill_name).split(';')

    if request.method == "POST":
        new_photo = User(email=user.email, password=user.password, profile_picture_url=request.form["photoURL"])

        db.session.delete(user)
        db.session.commit()
        db.session.add(new_photo)
        db.session.commit()


# TO SEND EMAIL:
    if form.validate_on_submit():
        mail_sent = True

        complete_email = {
            "name": form.name.data,
            "email": form.email.data,
            "mailText": form.mail_text.data,
        }

        NotificationManager().send_email(complete_email["name"], complete_email["email"], complete_email["mailText"])
        
        return render_template(
            'index.html',
            form=form,
            mail_text=form.mail_text,
            mail_sent=mail_sent,
            all_projects=projects,
            current_user=current_user,
            about_text=about_text,
            hardskills=hardskills,
            softskills=softskills,
            profile_picture_url=user.profile_picture_url,
        )
    return render_template(
        'index.html',
        form=form,
        mail_text=form.mail_text,
        mail_sent=mail_sent,
        all_projects=projects,
        current_user=current_user,
        about_text=about_text,
        hardskills=hardskills,
        softskills=softskills,
        profile_picture_url=user.profile_picture_url,
    )


@app.route("/projects/<id>")
def projects(id):
    projects = Projects.query.all()
    return render_template("projects.html", current_user=current_user, all_projects=projects, index=int(id))


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(meta={'csrf': False})
    if form.validate_on_submit():
        email = form.email.data
        passwd = form.password.data
        user = User.query.filter_by(email=email).first()
        try:
            if check_password_hash(user.password, passwd):
                login_user(user)
                return redirect(url_for('home'))
        except AttributeError:
            abort(401)
    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/addproject/<edit>", methods=["POST", "GET"])
@admin_only
def add_project(edit):
    if int(edit) != 0:
        project = Projects.query.filter_by(id=edit).first()
        form = AddProject(
            meta={'csrf': False},
            title=project.title,
            description=project.description,
            sub_description=project.sub_description,
            image_url=project.image_url,
            source_code_url=project.source_code_url,
        )
    else:
        form = AddProject(meta={'csrf': False})
    if form.validate_on_submit():
        new_project = Projects(
            title=form.title.data,
            description=form.description.data,
            sub_description=form.sub_description.data,
            image_url=form.image_url.data,
            source_code_url=form.source_code_url.data,
        )
        if int(edit) != 0:
            db.session.delete(project)
            db.session.commit()
            db.session.add(new_project)
            db.session.commit()
        else:
            db.session.add(new_project)
            db.session.commit()
        return render_template('addProject.html', succefully_added=True)
    return render_template('addProject.html', form=form, succefully_added=False, current_user=current_user)


@app.route("/<int:index>", methods=("POST", "GET"))
@admin_only
def delete_project(index):
    project = Projects.query.filter_by(id=index).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/editabout', methods=['GET', 'POST'])
@admin_only
def edit_about():
    form = EditAbout(meta={'csrf': False})
    about_text = AboutText.query.first()

    if request.method == 'POST':
        text = request.form.get('ckeditor')
        new_about_text = AboutText(text=text)
        db.session.delete(about_text)
        db.session.add(new_about_text)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('editAbout.html', form=form, about=about_text)


@app.route('/editskills', methods=['POST', 'GET'])
@admin_only
def edit_skills():
    hardskills = Skills.query.filter_by(skill_type='hardskill').first()
    softskills = Skills.query.filter_by(skill_type='softskill').first()
    form = EditSKills(
        meta={'csrf': False},
        softskillText=softskills.skill_name,
        hardskillText=hardskills.skill_name,
    )
    if form.validate_on_submit():
        new_softskill = Skills(
            skill_type='softskill',
            skill_name=form.softskillText.data,
        )
        new_hardskill = Skills(
            skill_type='hardskill',
            skill_name=form.hardskillText.data,
        )

        db.session.delete(hardskills)
        db.session.delete(softskills)
        db.session.add(new_softskill)
        db.session.add(new_hardskill)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('editSkills.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.2.179')
