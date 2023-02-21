import json

from flask import Flask, Response, render_template, flash, request, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from sqlalchemy.dialects.mysql import LONGTEXT
from werkzeug.debug import DebuggedApplication
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from _datetime import datetime

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practica.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Maiesch1_p@localhost/praticas'
app.config['SECRET_KEY'] = "Thisismysecretkeyy"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
# @login_required
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    parola = db.Column(db.String(200), nullable=False)
    calitatea = db.Column(db.String(200), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.parola = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.parola, password)

    def __repr__(self):
        return '<Username %r>' % self.username


class Studentprofiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    nume = db.Column(db.String(150))
    prenume = db.Column(db.String(150))
    facultatea = db.Column(db.String(150))
    studii = db.Column(db.String(150))
    an_studii = db.Column(db.String(150))
    telefon = db.Column(db.String(150))
    fisier = db.Column(db.String(50), nullable=True)
    cv = db.Column(db.LargeBinary)
    grade = db.Column(db.String(100))
    aboutme = db.Column(db.Text().with_variant(LONGTEXT, "mysql"))
    foto = db.Column(db.LargeBinary)
    adresa = db.Column(db.String(255))


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start = db.Column(db.String(255), nullable=False)
    graduation = db.Column(db.String(255), nullable=False)
    institution = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)


class Languages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(45), nullable=False)


class Experiences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text().with_variant(LONGTEXT, "mysql"), nullable=False)
    start = db.Column(db.String(45), nullable=False)
    finish = db.Column(db.String(45), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)


class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(45), nullable=False)


class Hobbies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hobbie = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.LargeBinary, nullable=True)


class Certificates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text().with_variant(LONGTEXT, "mysql"), nullable=False)


class Profesorprofiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_profesor = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    nume = db.Column(db.String(150))
    prenume = db.Column(db.String(150))
    facultatea = db.Column(db.String(150))


class Companieprofiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_companie = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    nume_companie = db.Column(db.String(150))
    adresa = db.Column(db.Text)
    adresa_web = db.Column(db.String(150))
    telefon = db.Column(db.String(150))
    descriere_companie = db.Column(db.Text(4294000000))
    nume_fisier = db.Column(db.String(50), nullable=True)
    logo = db.Column(db.LargeBinary)


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_job = db.Column(db.Integer, db.ForeignKey('companieprofiles.user_id_companie'))
    titlu = db.Column(db.String(250))
    descriere = db.Column(db.Text(4294000000))
    tip_job = db.Column(db.String(150))
    facultatea = db.Column(db.String(150))
    tag = db.Column(db.String(255))


class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    user_id_applicant = db.Column(db.Integer, db.ForeignKey('users.id'))


class SignupForm(FlaskForm):
    email = StringField("Adresa email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password1 = PasswordField("Parola", validators=[DataRequired(), EqualTo('password2', message='Parolele trebuie sa corespunda')])
    password2 = PasswordField("Confirma parola", validators=[DataRequired()])
    calitatea = SelectField("Alege: ", choices=[('student', 'Student'), ('profesor', 'Profesor'), ('companie', 'Companie')])
    cv = FileField("CV")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Adresa email", validators=[DataRequired(), Email()])
    password = PasswordField("Parola", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UpdateTipContForm(FlaskForm):
    calitatea = SelectField("Alege: ", choices=[('student', 'Student'), ('profesor', 'Profesor'), ('companie', 'Companie')])
    submit = SubmitField("Submit")


class JobForm(FlaskForm):
    titlu = StringField("Titlu", validators=[DataRequired()])
    descriere = StringField("Descriere", validators=[DataRequired()], widget = TextArea())
    tip_job = SelectField("Alege tipul de job: ", choices=[('partTime', 'Part-Time'), ('fullTime', 'Full-time'), ('internship', 'Internship'), ('stagiuPractica', 'Stagiu de Practica')])
    facultatea = SelectField("Alege facultatea: ", choices=[('fmi', 'FMI'), ('feaa', 'FEAA')])
    tag = StringField("Tag", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
    return render_template("home.html", userStudent=userStudent)


@app.route('/login', methods=['GET', 'POST'])
# @login_required
def login():
    userStudent = Studentprofiles.query.filter_by(user_id=current_user).first()
    email = None
    password = None
    form= LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        form.email.data = ''
        form.password.data = ''
        flash('Form submitted successfully')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.parola, password):
                flash('Logat cu succes!', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash('Parola incorecta, incercati din nou!', category='error')
        else:
            flash('Email-ul nu exista!', category='error')

    return render_template("login.html", email=email, password=password, form=form, user=current_user, userStudent=userStudent)


@app.route('/signup', methods=['GET', 'POST'])
# @login_required
def signup():
    userStudent = Studentprofiles.query.filter_by(user_id=current_user).first()
    email = None
    username = None
    password1 = None
    password2 = None
    form= SignupForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:
                print(request.form.get('gdpr'))
                if request.form.get('gdpr') == "gdpr":
                    hashed_pw = generate_password_hash(form.password1.data, "sha256")
                    user = Users(email=form.email.data, username = form.username.data, parola = hashed_pw, calitatea = form.calitatea.data)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)
                    return redirect(url_for('profil'))
                else:
                    flash("Nu ati bifat GDPR-ul")
                    return render_template("sign_up.html", form=form, userStudent=userStudent)
#                if form.password1.data == form.password2.data:
#                    user = Users(email=form.email.data, username = form.username.data, parola = form.password1.data, calitatea = form.calitatea.data)
#                    db.session.add(user)
#                    db.session.commit()
#                else:
#                    flash("PArolele nu sunt la fel!")
#                    return render_template("sign_up.html", form=form)

            else:
                flash("Username exista")
                return render_template("sign_up.html", form=form, userStudent=userStudent)
        else:
            flash("Email-ul exista")
            return render_template("sign_up.html", form=form, userStudent=userStudent)

        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        calitatea = form.calitatea.data
        form.email.data = ''
        form.username.data = ''
        form.password1.data = ''
        form.password2.data = ''
        form.calitatea.data = ''

        flash('User Added Successfully!')
    our_users = Users.query.order_by(Users.id)
    return render_template("sign_up.html", form=form, our_users=our_users, userStudent=userStudent)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if current_user.calitatea == "student":
        return redirect(url_for('profilStudent'))
    elif current_user.calitatea == "profesor":
        return redirect(url_for('profilProfesor'))
    elif current_user.calitatea == "companie":
        return redirect(url_for('profilCompanie'))


@app.route('/displayfoto')
@login_required
def display_foto():
    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()

    if userStudent:
        return Response(userStudent.foto)


@app.route('/delete_added_ecucation/<int:id>', methods=['POST'])
@login_required
def delete_Education(id):
    delete_education = json.loads(request.data)
    eduid = delete_education['id']
    edu = Education.query.get(eduid)
    if edu:
        if edu.userid == current_user.id:
            try:
                db.session.delete(edu)
                db.session.commit()
                return redirect('/profilCV/'+id)
            except:
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("404.html", userStudent=userStudent), 404


@app.route('/delete_added_language/<int:id>', methods=['POST'])
@login_required
def delete_language(id):
    delete_language = json.loads(request.data)
    langid = delete_language['id']
    lang = Languages.query.get(langid)
    if lang:
        if lang.userid == current_user.id:
            try:
                db.session.delete(lang)
                db.session.commit()
                return redirect('/profilCV/'+id)
            except:
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("404.html", userStudent=userStudent), 404


@app.route('/delete_added_experience/<int:id>', methods=['POST'])
@login_required
def delete_experience(id):
    delete_experience = json.loads(request.data)
    expid = delete_experience['id']
    exp = Experiences.query.get(expid)
    if exp:
        if exp.userid == current_user.id:
            try:
                db.session.delete(exp)
                db.session.commit()
                return redirect('/profilCV/'+id)
            except:
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("404.html", userStudent=userStudent), 404


@app.route('/delete_added_skills/<int:id>', methods=['POST'])
@login_required
def delete_skills(id):
    delete_skills = json.loads(request.data)
    skillid = delete_skills['id']
    skill = Skills.query.get(skillid)
    if skill:
        if skill.userid == current_user.id:
            try:
                db.session.delete(skill)
                db.session.commit()
                return redirect('/profilCV/'+id)
            except:
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("404.html", userStudent=userStudent), 404


@app.route('/delete_added_hobbies/<int:id>', methods=['POST'])
@login_required
def delete_hobbies(id):
    delete_hobbies = json.loads(request.data)
    hobbieid = delete_hobbies['id']
    hobbie = Hobbies.query.get(hobbieid)
    if hobbie:
        if hobbie.userid == current_user.id:
            try:
                db.session.delete(hobbie)
                db.session.commit()
                return redirect('/profilCV/'+id)
            except:
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("404.html", userStudent=userStudent), 404


@app.route('/update_foto/<int:id>', methods=['GET', 'POST'])
@login_required
def update_foto(id):
    user_to_update = Studentprofiles.query.get_or_404(id)
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        foto = request.files.get('poza')
        if foto:
            # filename = secure_filename(foto.filename)
            user_to_update.foto = foto.read()
            try:
                db.session.commit()
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
            except:
                flash("Database Error!!")
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
        else:
            flash("Grade field is empty")
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/update_grade/<int:id>', methods=['GET', 'POST'])
@login_required
def update_grade(id):

    user_to_update = Studentprofiles.query.get_or_404(id)
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        grade = request.form.get('gradeAvg')
        if grade:
            user_to_update.grade = grade
            try:
                db.session.commit()
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
            except:
                flash("Database Error!!")
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
        else:
            flash("Grade field is empty")
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/update_contact/<int:id>', methods=['GET', 'POST'])
@login_required
def update_contact(id):

    user_to_update = Studentprofiles.query.get_or_404(id)
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('cnt_address')
        if phoneNumber:
            if address:
                user_to_update.telefon = phoneNumber
                user_to_update.adresa = address
                try:
                    db.session.commit()
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                except:
                    flash("Database Error!!")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
            else:
                flash("Address field id empty")
        else:
            flash("Phone number field is empty")
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/add_education/<int:id>', methods=['GET', 'POST'])
@login_required
def add_education(id):
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        startyear = request.form.get('startyear')
        graduationyear = request.form.get('graduationyear')
        ongoing = request.form.get('ongoing')
        _institution = request.form.get('institution')
        _specialization = request.form.get('specialization')

        if startyear:
            if graduationyear:
                start = startyear.split("-")
                finish = graduationyear.split("-")
                date1 = datetime(int(start[0]), int(start[1]), int(start[2]))
                date2 = datetime(int(finish[0]), int(finish[1]), int(finish[2]))
                check_dates = date1 < date2
                if check_dates:
                    if _institution:
                        if _specialization:
                            new_education = Education(userid=current_user.id, start=startyear, graduation=graduationyear, institution=_institution, specialization=_specialization)
                            db.session.add(new_education)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        else:
                            flash("Specialization filed is empty")
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                    else:
                        flash("Institution filed is empty")
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                else:
                    flash("Start year is greater or equal to graduation year")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
            else:
                if ongoing:
                    if _institution:
                        if _specialization:
                            new_education = Education(userid=current_user.id, start=startyear, graduation="ongoing", institution=_institution, specialization=_specialization)
                            db.session.add(new_education)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        else:
                            flash("Specialization filed is empty")
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                    else:
                        flash("Institution filed is empty")
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                else:
                    flash("Error on the graduation field")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
        else:
            flash("Start filed is empty")
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user,
                                   userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies,
                                   certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user,
                               userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies,
                               certificates=user_to_update_certificates)


@app.route('/update_education/<int:id>', methods=['GET', 'POST'])
@login_required
def update_education(id):

    user_to_update = Studentprofiles.query.get_or_404(id)
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    user_to_update_education1 = Education.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        startyear = request.form.get('startyear_edit')
        graduationyear = request.form.get('graduationyear_edit')
        ongoing = request.form.get('edu_ongoing_edit')
        _institution = request.form.get('institution_edit')
        _specialization = request.form.get('specialization_edit')
        geteduID = request.form.get('geteduID')
        if startyear:
            if graduationyear:
                if _institution:
                    if _specialization:
                        user_to_update_education1 = Education.query.get_or_404(geteduID)
                        user_to_update_education1.start = startyear
                        user_to_update_education1.graduation = graduationyear
                        user_to_update_education1.institution = _institution
                        user_to_update_education1.specialization = _specialization
                        try:
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                        except:
                            flash("Database Error!!")
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                    else:
                        flash("Specialization field id empty")
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                else:
                    flash("Institution field id empty")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
            else:
                # flash(graduationyear)
                if _institution:
                    if _specialization:
                        user_to_update_education1 = Education.query.get_or_404(geteduID)
                        user_to_update_education1.start = startyear
                        user_to_update_education1.institution = _institution
                        user_to_update_education1.specialization = _specialization
                        try:
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                        except:
                            flash("Database Error!!")
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                    else:
                        flash("Specialization field id empty")
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                else:
                    flash("Institution field id empty")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
        else:
            flash("Start field id empty")
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user,
                                   userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies,
                                   certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/add_language/<int:id>', methods=['GET', 'POST'])
@login_required
def add_language(id):
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        _language = request.form.get('lang_select')
        lang_level = request.form.get('langLevel')
        if _language:
            if lang_level:
                user_to_update_language1 = Languages.query.filter_by(userid=current_user.id).first()
                # flash(user_to_update_language1.language)
                if user_to_update_language1:
                    user_to_update_language2 = Languages.query.filter_by(userid=current_user.id, language=_language).first()
                    # flash(user_to_update_language2)
                    if user_to_update_language2 is None:
                        if lang_level == 'Basic':
                            new_language = Languages(userid=current_user.id, language=_language, level='50')
                            db.session.add(new_language)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        elif lang_level == 'Intermediate':
                            new_language = Languages(userid=current_user.id, language=_language, level='70')
                            db.session.add(new_language)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        elif lang_level == 'Advanced':
                            new_language = Languages(userid=current_user.id, language=_language, level='90')
                            db.session.add(new_language)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        else:
                            new_language = Languages(userid=current_user.id, language=_language, level='100')
                            db.session.add(new_language)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                else:
                    if lang_level == 'Basic':
                        new_language = Languages(userid=current_user.id, language=_language, level='50')
                        db.session.add(new_language)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                    elif lang_level == 'Intermediate':
                        new_language = Languages(userid=current_user.id, language=_language, level='70')
                        db.session.add(new_language)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                    elif lang_level == 'Advanced':
                        new_language = Languages(userid=current_user.id, language=_language, level='90')
                        db.session.add(new_language)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
                    else:
                        new_language = Languages(userid=current_user.id, language=_language, level='100')
                        db.session.add(new_language)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
            else:
                flash('Choose a language level')
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
        else:
            flash('Choose a language')
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/update_aboutme/<int:id>', methods=['GET', 'POST'])
@login_required
def update_aboutme(id):
    user_to_update = Studentprofiles.query.get_or_404(id)
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        about = request.form.get('aboutmeTxt')
        if about:
            user_to_update.aboutme = about
            try:
                db.session.commit()
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
            except:
                flash("Database Error!!")
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
        else:
            flash("About field id empty")
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/update_experience/<int:id>', methods=['GET', 'POST'])
@login_required
def update_experience(id):
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        startexp = request.form.get('startexp')
        finishexp = request.form.get('finishexp')
        ongoing = request.form.get('ongoingexp')
        position_ = request.form.get('position_')
        company_ = request.form.get('company_')
        description_ = request.form.get('description_')

        if startexp:
            if finishexp:
                start = startexp.split("-")
                finish = finishexp.split("-")
                date1 = datetime(int(start[0]), int(start[1]), int(start[2]))
                date2 = datetime(int(finish[0]), int(finish[1]), int(finish[2]))
                check_dates = date1 < date2
                if check_dates:
                    if position_:
                        if company_:
                            if description_:
                                user_to_update_experience1 = Experiences.query.filter_by(userid=current_user.id).first()
                                if user_to_update_experience1:
                                    user_to_update_experience2 = Experiences.query.filter_by(userid=current_user.id, position=position_, description=description_).first()
                                    if user_to_update_experience2 is None:
                                        new_experience = Experiences(userid=current_user.id, description=description_, start=startexp, finish=finishexp, company=company_, position=position_)
                                        db.session.add(new_experience)
                                        db.session.commit()
                                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                                        return render_template("profile_student_cv.html", user=current_user,
                                                               userStudent=userStudent,
                                                               edu=user_to_update_education,
                                                               lang=user_to_update_language,
                                                               exp=user_to_update_experience,
                                                               skills=user_to_update_skills,
                                                               hobbies=user_to_update_hobbies,
                                                               certificates=user_to_update_certificates)
                                    else:
                                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                                        return render_template("profile_student_cv.html", user=current_user,
                                                               userStudent=userStudent,
                                                               edu=user_to_update_education,
                                                               lang=user_to_update_language,
                                                               exp=user_to_update_experience,
                                                               skills=user_to_update_skills,
                                                               hobbies=user_to_update_hobbies,
                                                               certificates=user_to_update_certificates)
                                else:
                                    new_experience = Experiences(userid=current_user.id, description=description_, start=startexp, finish=finishexp, company=company_, position=position_)
                                    db.session.add(new_experience)
                                    db.session.commit()
                                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                                    return render_template("profile_student_cv.html", user=current_user,
                                                           userStudent=userStudent,
                                                           edu=user_to_update_education, lang=user_to_update_language,
                                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                                           hobbies=user_to_update_hobbies,
                                                           certificates=user_to_update_certificates)
                            else:
                                flash('Description field empty')
                                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                                return render_template("profile_student_cv.html", user=current_user,
                                                       userStudent=userStudent,
                                                       edu=user_to_update_education, lang=user_to_update_language,
                                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                                       hobbies=user_to_update_hobbies,
                                                       certificates=user_to_update_certificates)
                        else:
                            flash("Company filed is empty")
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                    else:
                        flash("Position filed is empty")
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                else:
                    flash("Start year is greater or equal to graduation year")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
            else:
                if ongoing:
                    if position_:
                        if company_:
                            if description_:
                                new_experience = Experiences(userid=current_user.id, description=description_,
                                                             start=startexp, finish="ongoing", company=company_,
                                                             position=position_)
                                db.session.add(new_experience)
                                db.session.commit()
                                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                                return render_template("profile_student_cv.html", user=current_user,
                                                       userStudent=userStudent,
                                                       edu=user_to_update_education,
                                                       lang=user_to_update_language,
                                                       exp=user_to_update_experience,
                                                       skills=user_to_update_skills,
                                                       hobbies=user_to_update_hobbies,
                                                       certificates=user_to_update_certificates)
                            else:
                                flash("Description field is empty")
                                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                                return render_template("profile_student_cv.html", user=current_user,
                                                       userStudent=userStudent,
                                                       edu=user_to_update_education, lang=user_to_update_language,
                                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                                       hobbies=user_to_update_hobbies,
                                                       certificates=user_to_update_certificates)
                        else:
                            flash("Company filed is empty")
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                    else:
                        flash("Position filed is empty")
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                else:
                    flash("Error on the graduation field")
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
        else:
            flash("Start filed is empty")
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user,
                                   userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies,
                                   certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user,
                               userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies,
                               certificates=user_to_update_certificates)


@app.route('/add_skills/<int:id>', methods=['GET', 'POST'])
@login_required
def add_skills(id):
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        _skill = request.form.get('skills_select')
        skill_level = request.form.get('skillLevel')
        if _skill:
            if skill_level:
                user_to_update_skills1 = Skills.query.filter_by(userid=current_user.id).first()
                if user_to_update_skills1:
                    user_to_update_skills2 = Skills.query.filter_by(userid=current_user.id, skill=_skill).first()
                    if user_to_update_skills2 is None:
                        if skill_level == 'Basic':
                            new_skill = Skills(userid=current_user.id, skill=_skill, level='50')
                            db.session.add(new_skill)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        elif skill_level == 'Intermediate':
                            new_skill = Skills(userid=current_user.id, skill=_skill, level='70')
                            db.session.add(new_skill)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        elif skill_level == 'Advanced':
                            new_skill = Skills(userid=current_user.id, skill=_skill, level='90')
                            db.session.add(new_skill)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                        else:
                            new_skill = Skills(userid=current_user.id, skill=_skill, level='100')
                            db.session.add(new_skill)
                            db.session.commit()
                            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                            return render_template("profile_student_cv.html", user=current_user,
                                                   userStudent=userStudent,
                                                   edu=user_to_update_education, lang=user_to_update_language,
                                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                                   hobbies=user_to_update_hobbies,
                                                   certificates=user_to_update_certificates)
                else:
                    if skill_level == 'Basic':
                        new_skill = Skills(userid=current_user.id, skill=_skill, level='50')
                        db.session.add(new_skill)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                    elif skill_level == 'Intermediate':
                        new_skill = Skills(userid=current_user.id, skill=_skill, level='70')
                        db.session.add(new_skill)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                    elif skill_level == 'Advanced':
                        new_skill = Skills(userid=current_user.id, skill=_skill, level='90')
                        db.session.add(new_skill)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
                    else:
                        new_skill = Skills(userid=current_user.id, skill=_skill, level='100')
                        db.session.add(new_skill)
                        db.session.commit()
                        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                        return render_template("profile_student_cv.html", user=current_user,
                                               userStudent=userStudent,
                                               edu=user_to_update_education, lang=user_to_update_language,
                                               exp=user_to_update_experience, skills=user_to_update_skills,
                                               hobbies=user_to_update_hobbies,
                                               certificates=user_to_update_certificates)
            else:
                flash('Choose a Skill level')
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
        else:
            flash('Choose a Skill')
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/add_hobbies/<int:id>', methods=['GET', 'POST'])
@login_required
def add_hobbies(id):
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)

    if request.method == "POST":
        hobbie_ = request.form.get('hobbie_select')
        if hobbie_:
            user_to_update_hobbies1= Hobbies.query.filter_by(userid=current_user.id)
            if user_to_update_hobbies1:
                user_to_update_hobbies2 = Hobbies.query.filter_by(userid=current_user.id, hobbie=hobbie_).first()
                if user_to_update_hobbies2 is None:
                    new_hobbbie = Hobbies(userid=current_user.id, hobbie=hobbie_)
                    db.session.add(new_hobbbie)
                    db.session.commit()
                    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                    return render_template("profile_student_cv.html", user=current_user,
                                           userStudent=userStudent,
                                           edu=user_to_update_education, lang=user_to_update_language,
                                           exp=user_to_update_experience, skills=user_to_update_skills,
                                           hobbies=user_to_update_hobbies,
                                           certificates=user_to_update_certificates)
            else:
                new_hobbbie = Hobbies(userid=current_user.id, hobbie=hobbie_)
                db.session.add(new_hobbbie)
                db.session.commit()
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profile_student_cv.html", user=current_user,
                                       userStudent=userStudent,
                                       edu=user_to_update_education, lang=user_to_update_language,
                                       exp=user_to_update_experience, skills=user_to_update_skills,
                                       hobbies=user_to_update_hobbies,
                                       certificates=user_to_update_certificates)
        else:
            flash('Choose Hobbies')
            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                                   edu=user_to_update_education, lang=user_to_update_language,
                                   exp=user_to_update_experience, skills=user_to_update_skills,
                                   hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)
    else:
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent,
                               edu=user_to_update_education, lang=user_to_update_language,
                               exp=user_to_update_experience, skills=user_to_update_skills,
                               hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/profilCV/<int:id>', methods=['GET', 'POST'])
@login_required
def CVprofil(id):
    user_to_update_education = Education.query.filter_by(userid=current_user.id)
    user_to_update_language = Languages.query.filter_by(userid=current_user.id)
    user_to_update_experience = Experiences.query.filter_by(userid=current_user.id)
    user_to_update_skills = Skills.query.filter_by(userid=current_user.id)
    user_to_update_hobbies = Hobbies.query.filter_by(userid=current_user.id)
    user_to_update_certificates = Certificates.query.filter_by(userid=current_user.id)
    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
    return render_template("profile_student_cv.html", user=current_user, userStudent=userStudent, edu=user_to_update_education, lang=user_to_update_language, exp=user_to_update_experience, skills=user_to_update_skills, hobbies=user_to_update_hobbies, certificates=user_to_update_certificates)


@app.route('/profilStudent/', methods=['GET', 'POST'])
@login_required
def profilStudent():
    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
    if userStudent:
        return render_template("profil_student_completat.html", user=current_user, userStudent=userStudent)
    else:
        
        if request.method == 'POST':
            nume = request.form.get('nume')
            prenume = request.form.get('prenume')
            facultatea = request.form.get('facultatea')
            studii = request.form.get('studii')
            anStudii = request.form.get('anStudii')
            telefon = request.form.get('telefon')
            fisier = request.files['file']

            userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
            

            if userStudent:
                flash('User-ul exista deja', category='success')
                return render_template("profil_student_completat.html", user=current_user, userStudent=userStudent)
            elif len(nume) < 2:
                flash('Numele este prea scurt', category = 'error')
            elif len(prenume) < 2:
                flash('Prenumele este prea scurt', category = 'error') 
            elif len(facultatea) < 1:
                flash('Alegeti o facultate', category = 'error')
            elif len(studii) < 1:
                flash('Alegeti studiile', category = 'error')
            elif len(anStudii) < 1:
                flash('Anul de studii nu este corect', category = 'error')
            elif len(telefon) < 1:
                flash('Introduceti un numar de telefon', category = 'error')
            else:
                new_userStudent = Studentprofiles(nume=nume, prenume=prenume, facultatea=facultatea, studii=studii, an_studii=anStudii, telefon=telefon, user_id = current_user.id, fisier = fisier, cv=fisier.read())
                db.session.add(new_userStudent)
                db.session.commit()
                userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
                return render_template("profil_student_completat.html", user=current_user, userStudent=userStudent)
        return render_template("profil_student.html", user=current_user, userStudent=userStudent)


@app.route('/profilProfesor', methods=['GET', 'POST'])
@login_required
def profilProfesor():
    userProfesor = Profesorprofiles.query.filter_by(user_id_profesor=current_user.id).first()
    if userProfesor:
        return render_template("profil_profesor_completat.html", user=current_user, userProfesor=userProfesor)
    else:
        
        if request.method == 'POST':
            nume = request.form.get('nume')
            prenume = request.form.get('prenume')
            facultatea = request.form.get('facultatea')
            

            userProfesor = Profesorprofiles.query.filter_by(user_id_profesor=current_user.id).first()
            

            if userProfesor:
                return render_template("profil_profesor_completat.html", user=current_user, userProfesor=userProfesor)
            elif len(nume) < 2:
                flash('Numele este prea scurt', category = 'error')
            elif len(prenume) < 2:
                flash('Prenumele este prea scurt', category = 'error') 
            elif len(facultatea) < 1:
                flash('Alegeti o facultate', category = 'error')
            else:
                new_userProfesor = Profesorprofiles(nume=nume, prenume=prenume, facultatea=facultatea, user_id_profesor = current_user.id)
                db.session.add(new_userProfesor)
                db.session.commit()
                userProfesor = Profesorprofiles.query.filter_by(user_id_profesor=current_user.id).first()
                return render_template("profil_profesor_completat.html", user=current_user, userProfesor=userProfesor)
        return render_template("profil_profesor.html", user=current_user)


@app.route('/profilCompanie', methods=['GET', 'POST'])
@login_required
def profilCompanie():
    userCompanie = Companieprofiles.query.filter_by(user_id_companie=current_user.id).first()
    if userCompanie:
        return render_template("profil_companie_completat.html", user=current_user, userCompanie=userCompanie)
    else:
        
        if request.method == 'POST':
            nume_companie = request.form.get('denumire')
            adresa = request.form.get('adresa')
            adresa_web = request.form.get('web')
            telefon = request.form.get('telefon')
            descriere_companie = request.form.get('descriere')
            fisier = request.files['fisier']

            userCompanie = Companieprofiles.query.filter_by(user_id_companie=current_user.id).first()
            

            if userCompanie:
                flash('User-ul exista deja', category='success')
                return render_template("profil_companie_completat.html", user=current_user, userCompanie=userCompanie)
            elif len(nume_companie) < 2:
                flash('Numele este prea scurt', category = 'error')
            else:
                new_userCompanie = Companieprofiles(nume_companie=nume_companie, adresa=adresa, adresa_web=adresa_web, descriere_companie=descriere_companie, telefon=telefon, user_id_companie = current_user.id, nume_fisier = fisier, logo=fisier.read())
                db.session.add(new_userCompanie)
                db.session.commit()
                userCompanie = Companieprofiles.query.filter_by(user_id_companie=current_user.id).first()
                return render_template("profil_companie_completat.html", user=current_user, userCompanie=userCompanie)
        return render_template("profil_companie.html", user=current_user)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user_to_update = Studentprofiles.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.nume = request.form.get('nume')
        user_to_update.prenume = request.form.get('prenume')
        user_to_update.facultatea = request.form.get('facultatea')
        user_to_update.studii = request.form.get('studii')
        user_to_update.an_studii = request.form.get('anStudii')
        user_to_update.telefon = request.form.get('telefon')
        user_to_update.fisier = request.files['file']
        user_to_update.cv = request.files['file'].read()

        db.session.commit()
        flash("Profilul a fost modificat cu succes!")
        userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
        return render_template("profil_student_completat.html", user=current_user, userStudent=userStudent)
    else:
        return render_template("update_profil_student.html", user = user_to_update, id=id)


@app.route('/updateProfilProfesor/<int:id>', methods=['GET', 'POST'])
@login_required
def updateProfilProfesor(id):
    user_to_update = Profesorprofiles.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.nume = request.form.get('nume')
        user_to_update.prenume = request.form.get('prenume')
        user_to_update.facultatea = request.form.get('facultatea')
        db.session.commit()
        userProfesor = Profesorprofiles.query.filter_by(user_id_profesor=current_user.id).first()
        return render_template("profil_profesor_completat.html", user=current_user, userProfesor=userProfesor)
    else:
        return render_template("update_profil_profesor.html", user = user_to_update, id=id)


@app.route('/updateProfilCompanie/<int:id>', methods=['GET', 'POST'])
@login_required
def updateProfilCompanie(id):
    user_to_update = Companieprofiles.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.nume_companie = request.form.get('denumire')
        user_to_update.adresa = request.form.get('adresa')
        user_to_update.adresa_web = request.form.get('web')
        user_to_update.telefon = request.form.get('telefon')
        user_to_update.descriere_companie = request.form.get('descriere')
        user_to_update.nume_fisier = request.files['fisier']
        user_to_update.logo = request.files['fisier'].read()

        db.session.commit()
        userCompanie = Companieprofiles.query.filter_by(user_id_companie=current_user.id).first()
        return render_template("profil_companie_completat.html", user=current_user, userCompanie=userCompanie)
    else:
        return render_template("update_profil_companie.html", user = user_to_update, id=id)


@app.route('/updateTipCont/<int:id>', methods=['GET', 'POST'])
@login_required
def updateTipCont(id):
    user_to_update = Users.query.get_or_404(id)
    old_tip = user_to_update.calitatea
    if request.method == "POST":
        new_tip = request.form['calitatea']
        user_to_update.calitatea = request.form['calitatea']
        if old_tip != new_tip:
            user = Users.query.filter_by(id=id).first()
            if user.calitatea == "student":
                user_profile = Studentprofiles.query.filter_by(user_id=id).first()
                if user_profile:
                    user_profile_to_delete = Studentprofiles.query.get_or_404(user_profile.id)
                    db.session.delete(user_profile_to_delete)
                    db.session.commit()
            elif user.calitatea == "profesor":
                user_profile = Profesorprofiles.query.filter_by(user_id_profesor=id).first()
                if user_profile:
                    user_profile_to_delete = Profesorprofiles.query.get_or_404(user_profile.id)
                    db.session.delete(user_profile_to_delete)
                    db.session.commit()
            db.session.commit()
        return redirect(url_for('profil'))
    else:
        return render_template("update_tip_cont.html", user_to_update = user_to_update)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = Users.query.filter_by(id=id).first()
    user_to_delete = Users.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    if user.calitatea == "student":
        user_profile = Studentprofiles.query.filter_by(user_id=id).first()
        if user_profile:
            user_profile_to_delete = Studentprofiles.query.get_or_404(user_profile.id)
            db.session.delete(user_profile_to_delete)
            db.session.commit()
    elif user.calitatea == "profesor":
        user_profile = Profesorprofiles.query.filter_by(user_id_profesor=id).first()
        if user_profile:
            user_profile_to_delete = Profesorprofiles.query.get_or_404(user_profile.id)
            db.session.delete(user_profile_to_delete)
            db.session.commit()
    
    return redirect(url_for('signup'))


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobForm()
    userCompanie = Companieprofiles.query.filter_by(user_id_companie=current_user.id).first() 
    if form.validate_on_submit():
        job = Jobs(titlu = form.titlu.data, descriere = form.descriere.data, tip_job = form.tip_job.data, facultatea = form.facultatea.data, tag = form.tag.data, user_id_job = userCompanie.user_id_companie)
        form.titlu.data = ''
        form.descriere.data = ''
        form.tip_job.data = ''
        form.facultatea.data = ''
        form.tag.data = ''
        db.session.add(job)
        db.session.commit()
        flash("Job a fost adaugat cu succes.")
        return redirect(url_for('dashboard'))
    return render_template("add_job.html", form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    jobs = Jobs.query.filter_by(user_id_job=current_user.id)

    return render_template("dashboard.html", jobs=jobs)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def job(id):
    job = Jobs.query.get_or_404(id)

    return render_template("job.html", job=job)


@app.route('/modificaJob/<int:id>', methods=['GET', 'POST'])
@login_required
def modificaJob(id):
    form = JobForm()
    job_to_update = Jobs.query.get_or_404(id)

    if request.method == "POST":
        job_to_update.titlu = request.form.get('titlu')
        job_to_update.descriere = request.form.get('descriere')
        job_to_update.tip_job = request.form.get('tip_job')
        job_to_update.facultatea = request.form.get('facultatea')
        job_to_update.tag = request.form.get('tag')

        db.session.commit()
    
        return redirect(url_for('dashboard'))
    else:
        return render_template("update_job.html", job=job_to_update, form=form)


@app.route('/stergeJob/<int:id>', methods=['GET', 'POST'])
@login_required
def stergeJob(id):
    job = Jobs.query.filter_by(id=id).first()
    job_to_delete = Jobs.query.get_or_404(id)
    db.session.delete(job_to_delete)
    db.session.commit()
    
    return redirect(url_for('dashboard'))


@app.route('/internshipuri', methods=['GET', 'POST'])
@login_required
def internshipuri():
    jobs = Jobs.query.all()

    return render_template("internships.html", jobs=jobs)


@app.route('/aplica/<int:id>', methods=['GET', 'POST'])
@login_required
def aplica(id):
    applicant = Applicants(job_id=id, user_id_applicant = current_user.id)
    db.session.add(applicant)
    db.session.commit()
    return redirect(url_for('internshipuri'))


@app.route('/vizualizeazaAplicanti/<int:id>', methods=['GET', 'POST'])
@login_required
def vizualizeazaAplicanti(id):
    job = Jobs.query.get_or_404(id)
    applicants = Applicants.query.filter_by(job_id=id)
    students = Studentprofiles.query.all()

    return render_template("applicants.html", job=job, applicants=applicants, students=students)


@app.route('/studentCV/<int:id>', methods=['GET', 'POST'])
@login_required
def studentCV(id):
    
    userStudent = Studentprofiles.query.filter_by(user_id=id).first()
    user = Users.query.filter_by(id=userStudent.user_id).first()
    user_education = Education.query.filter_by(userid=id)
    user_language = Languages.query.filter_by(userid=id)
    user_experience = Experiences.query.filter_by(userid=id)
    user_skills = Skills.query.filter_by(userid=id)
    user_hobbies = Hobbies.query.filter_by(userid=id)
    user_certificates = Certificates.query.filter_by(userid=id)
    return render_template("student_cv.html", user = user, userStudent=userStudent, edu=user_education, lang=user_language, exp=user_experience, skills=user_skills, hobbies=user_hobbies, certificates=user_certificates)

    return render_template("student_cv.html", job=job, applicants=applicants, students=students)


@app.errorhandler(404)
@login_required
def page_not_found(e):
    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
    return render_template("404.html", userStudent=userStudent), 404


@app.errorhandler(500)
@login_required
def page_not_found(e):
    userStudent = Studentprofiles.query.filter_by(user_id=current_user.id).first()
    return render_template("500.html", userStudent=userStudent), 500


if __name__ == '__main__':
    app.run(debug=True)
application = DebuggedApplication(app, True)
