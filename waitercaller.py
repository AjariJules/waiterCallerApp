from flask import Flask,render_template, url_for, redirect,request
from flask.ext.login import LoginManager, login_required,login_user,logout_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User

app = Flask(__name__)
app.secret_key = 'TwxlMVrtoqiSd0MxGd5AVbqK2zmzMGEQX1kgRxZjEAHotLhkU0PJ0lgCHRKk63Fa6q1ZsDSIb6bZkhId7gAL8Sg2VOKH58MImR66'
login_manager = LoginManager(app)

DB = DBHelper()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account")
@login_required
def account():
    return "You are logged in"


@app.route("/login", methods=["Post"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user(email)
    if  user_password  == password:
        user = User(email)
        login_user(user,remember = True)
        return redirect(url_for('account'))
    return home()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
