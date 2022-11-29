from flask import Flask, render_template, url_for, redirect, abort, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField, TextAreaField, PasswordField, URLField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField, CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

WTF_CSRF_SECRET_KEY='6LeYIbsSAAAAACRPIllx'
RECAPTCHA_PUBLIC_KEY = "6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J"
RECAPTCHA_PRIVATE_KEY = "6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu"

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '6LeYIbsSAAAAACRPIllx'
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

# FLASK WTF
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    mail_text= TextAreaField('Message', validators=[DataRequired()])
    recaptcha= RecaptchaField()
    submit= SubmitField('Send Email')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Tolken', validators=[DataRequired()])
    # recaptcha= RecaptchaField() # DESLIGUEI PARA TESTAR
    submit= SubmitField('Login in')

class AddProject(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    description = CKEditorField('Description', validators=[DataRequired()])
    sub_description = StringField('Sub Description', validators=[DataRequired()])
    image_url = URLField('Project Image URL', validators=[DataRequired()])
    source_code_url = URLField('Source Code URL', validators=[DataRequired()])
    # recaptcha= RecaptchaField() # DESLIGUEI PARA TESTAR
    submit= SubmitField('Add Project')

class AddSkills(FlaskForm):
    skill_type=StringField('Skill Type', validators=[DataRequired()])
    skill_name=StringField('Skill Name', validators=[DataRequired()])
    submit = SubmitField('Add Skill')

class EditAbout(FlaskForm):
    text=CKEditorField('Text', validators=[DataRequired()])
    submit= SubmitField('Save')

# SQLALCHEMY
class User(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(80), unique=True, nullable=False)
    password= db.Column(db.String(100), unique=True, nullable=False)

    # def __repr__(self) -> str:
    #     return '<User %r>' % self.email

class Projects(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    sub_description = db.Column(db.String(100), nullable=False) #RECRIAR TABLE NO DB
    image_url = db.Column(db.String(1000), nullable=False)
    source_code_url = db.Column(db.String(1000), unique=True, nullable=False)

class Skills(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    skill_type= db.Column(db.String(10), nullable=False)
    skill_name = db.Column(db.String(100), unique=True, nullable=False)

class AboutText(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    text= db.Column(db.String(250), unique=True, nullable=False)

admin = User(email='lucascostamr812@gmail.com', password=generate_password_hash('147874@', method='pbkdf2:sha256', salt_length=8))

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id !=1:
                return abort(403)
        except AttributeError:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# LEMBRAR DE COLOCAR AVISOS CASO OS PARAMETOS DO DB SEJAM IGUAIS

text =AboutText(text= "I'm a Brazilian, who loves technology, music, games and I'm also a student of Information Systems who decided to be a Developer to offer more accessible technology to society.") 
# with app.app_context():
#     # db.create_all()
#     db.session.add(text)
#     db.session.commit()
#     pass



# FLASK APP
@app.route("/", methods=['POST', 'GET'])
def home():
    mail_sent=False
    projects = Projects.query.all()
    form = ContactForm(meta={'csrf': False})
    about_text= AboutText.query.all()
    if form.validate_on_submit():
        mail_sent=True

        complete_email = {
            "name": form.name.data,
            "email": form.email.data,
            "mailText": form.mail_text.data,
        }
    return render_template(
        'index.html', 
        form=form, 
        mail_text=form.mail_text, 
        mail_sent=mail_sent, 
        all_projects=projects, 
        current_user=current_user,
        about_text= about_text,
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


@app.route("/addproject", methods=["POST", "GET"])
@admin_only
def add_project():
    form = AddProject(meta={'csrf': False})
    if form.validate_on_submit():

        new_project = Projects(
            title= form.title.data,
            description= form.description.data,
            sub_description= form.sub_description.data,
            image_url = form.image_url.data,
            source_code_url= form.source_code_url.data,
            )
        
        db.session.add(new_project)
        db.session.commit()

        return render_template('addProject.html', succefully_added=True)

    return render_template('addProject.html', form=form, succefully_added=False, current_user=current_user)

@app.route('/editabout', methods=['GET', 'POST'])
@admin_only
def edit_about():
    # CRIAR WTF E O IF VALIDATE_ON_SUBMIT E DEPOIS CRIAR UM OBJETO PARA EDITAR O DB
    form=EditAbout(meta={'csrf': False})
    about_text = AboutText.query.all()

    # if form.validate_on_submit():
    #     pass
    return render_template('editAbout.html', form=form, about_text=about_text)

@app.route('/editSkills', methods=['POST', 'GET'])
@admin_only
def edit_skills():
     # CRIAR WTF E O IF VALIDATE_ON_SUBMIT E DEPOIS CRIAR UM OBJETO PARA EDITAR O DB
    return render_template('editSkills.html')


if __name__ == '__main__':
    app.run(debug=True)

# CONTINUAR O COM A VALIDACAO DE LOGIN E PRIVILEGIOS COMO BOTAO DE ADICIONAR, REMOVER, EDITAR
# APLICAR A FUNCAO ADMIN ONLY PRA GALERA NAO CONSSEGUIR ENTRAR NA PAGINA DE ADDPROJECT
# CRIAR PAGINA DE EDIT
# MUDAR O IMAGEM DOS PROJETOS, IMAGENS EST'AO IGUAIS, MUDAR PARA A IMAGE URL DE CADA PROJETO

