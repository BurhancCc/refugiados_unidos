from flask import Flask, Blueprint, redirect, render_template, request, url_for
from datetime import date
import re
import pyTigerGraph  as tg
from datetime import date, time, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError, Optional
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "x"

class RegistrationForm(FlaskForm):

  inputRequired = InputRequired(message="This box can't be empty!")
  emailValidation = Email(message="This is not a valid e-mail address!")
  nameLength = Length(min=2, max=50, message="A name has to be between 2 and 50 letters!")
  passwordLength = Length(min=8, max=50, message="A password has to be at least 8 characters, with a maximum of 50 characters!")
  email = EmailField('email', render_kw={"placeholder": "email"}, validators=[inputRequired, nameLength, emailValidation])
  password = PasswordField('password', render_kw={"placeholder": "password"}, validators=[inputRequired, passwordLength])
  repeatPassword = PasswordField('repeatPassword', render_kw={"placeholder": "repeat password"}, validators=[inputRequired, EqualTo("password", message="The passwords have to be the same!")])
  firstName = StringField('firstName', render_kw={"placeholder": "first name"}, validators=[inputRequired, nameLength])
  surname = StringField('surname', render_kw={"placeholder": "surname"}, validators=[inputRequired, nameLength])
  endDate = DateField('endDate', validators=[Optional()])
  countries = [("BY", "Belarus"), ("PL", "Poland"), ("UA", "Ukraine")]
  country = SelectField(label="country", choices=countries)

  def validate_first_name(form, firstName):
    firstName = firstName.data
    regex = "[a-zA-Z]"
    if len(re.findall(regex, firstName)) != len(firstName):
      raise ValidationError('Names must consist of only letters!')
  def validate_surname(form, surname):
    surname = surname.data
    regex = "[a-zA-Z]"
    if len(re.findall(regex, surname)) != len(surname):
      raise ValidationError('Names must consist of only letters!')
  def validate_end_date(form, endDate):
    endDate = endDate.data
    if endDate < date.today():
      raise ValidationError('The end date of your account must be after today!')
  def validate_password(form, password):
    password = password.data
    regexSmall = "[a-z]"
    regexCapital= "[A-Z]"
    regexDigits = "[0-9]"
    if (re.findall(regexSmall, password) == [] or re.findall(regexDigits, password) == []
            or re.findall(regexCapital, password) == []):
            raise ValidationError('A password must contain at least 1 small letter, 1 capital letter, and one number!')

class LoginForm(FlaskForm):
  inputRequired = InputRequired(message="This box can't be empty!")
  email = EmailField('email', render_kw={"placeholder": "email"}, validators=[inputRequired])
  password = PasswordField('password', render_kw={"placeholder": "password"}, validators=[inputRequired])

@app.route("/")
def index():
  title = "Refugiados Unidos"
  return render_template('index.html', title=title)

def runRegistrationQuery(formData):
  TG_HOST = "https://refugiados-unidos.i.tgcloud.io/"
  TG_USERNAME = "tigergraph"
  TG_PASSWORD = "Abcd1234!"
  TG_GRAPHNAME = "RefugiadosUnidos"
  latitude = 0
  longtitude = 0
  userRole = 1
  conn = tg.TigerGraphConnection(TG_HOST, TG_GRAPHNAME, TG_USERNAME, TG_PASSWORD)
  token = conn.getToken("i3u0jpebhih97seb3kgu1omg9dptcpvs")
  data = {"email": formData['email'],
  "password": formData['password'],
  "firstname": formData['firstname'],
  "surname": formData['surname'],
  "latitude": latitude,
  "longtitude": longtitude,
  "country": formData['country'],
  "userroleID": userRole,
  "registrationDate": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
  "endDate": str(formData['endDate'].strftime('%Y-%m-%d %H:%M:%S'))}
  ls = conn.gsql("ls", options=[])

  conn.runInstalledQuery("Registration", data)

@app.route("/register", methods=["POST", "GET"])
def register():
  title = "Registration"
  form = RegistrationForm()
  if form.validate_on_submit():
    formData = request.get_json()
    TG_HOST = "https://refugiados-unidos.i.tgcloud.io/"
    TG_USERNAME = "tigergraph"
    TG_PASSWORD = "Abcd1234!"
    TG_GRAPHNAME = "RefugiadosUnidos"
    latitude = 0
    longtitude = 0
    userRole = 1
    conn = tg.TigerGraphConnection(TG_HOST, TG_GRAPHNAME, TG_USERNAME, TG_PASSWORD)
    token = conn.getToken("i3u0jpebhih97seb3kgu1omg9dptcpvs")
    data = {"email": formData['email'],
    "password": formData['password'],
    "firstname": formData['firstname'],
    "surname": formData['surname'],
    "latitude": latitude,
    "longtitude": longtitude,
    "country": formData['country'],
    "userroleID": userRole,
    "registrationDate": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    "endDate": str(formData['endDate'].strftime('%Y-%m-%d %H:%M:%S'))}
    #runRegistrationQuery(formData)
    conn.runInstalledQuery("Registration", data)
    return redirect(url_for("registered"))
  title = "registered"
  return render_template('register.html', title=title, names="names", form=form, message="message")

@app.route("/login", methods=["POST", "GET"])
def login():
  title = "Login"
  form = LoginForm()
  if form.validate_on_submit():
    return redirect(url_for("services"))
  return render_template('login.html', form=form, title=title, message="message")

@app.route("/registered", methods=["POST", "GET"])
def registered():
  form = RegistrationForm()
  if form.validate_on_submit():
    return redirect(url_for('.index'))
  return redirect(url_for('register'))

@app.route("/services", methods=["POST", "GET"])
def services():
  title = "Services"
  return render_template('services.html', title=title)

if __name__ == "__main__":
  app.run(debug=True)