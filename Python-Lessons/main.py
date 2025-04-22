from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from game import Case

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<Users {self.username} {self.email} {self.password}>"


class RegisterForm(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired()])
    email = EmailField(
        "Введите email",
        validators=[DataRequired(),
                    Email(message="Это не email")])
    password = PasswordField("Введите пароль",
                             validators=[DataRequired(),
                                         Length(min=6)])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    email = EmailField(
        "Введите email",
        validators=[DataRequired(),
                    Email(message="Это не email")])
    password = PasswordField("Введите пароль", validators=[DataRequired()])
    submit = SubmitField('Отправить')


@app.route('/')
def index():
    return render_template("index.html", username="Michael")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    with app.app_context():
        db.create_all()
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Users(username=form.name.data,
                         email=form.email.data,
                         password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('profile', code=307))
    return render_template("sign_up.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.form:
        name = request.form['name']
        email = request.form['email']
        return render_template("profile.html", name=name, email=email)
    else:
        return render_template("profile.html")


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    login = LoginForm()
    if login.validate_on_submit():
        user = Users.query.filter_by(email=login.email.data).first()
        if user and user.password:
            if user.password == login.password.data:
                return redirect(url_for('profile', code=307))
            else:
                return redirect(url_for('sign_up', code=307))
    return render_template("login.html", form=login)


@app.route("/test", methods=['GET', 'POST'])
def revie_case():
    case = Case("test_case", 100, 10)
    case_drop = None
    if request.method == 'POST':
        case_drop = case.open_case()
    return render_template("case.html", drop=case_drop)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
