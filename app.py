from flask import Flask, render_template, request, flash, redirect, session


from models import db, connect_db, User
from forms import UserAddForm, LoginForm



app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///nobpa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
CURR_USER_KEY = "curr_user"

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """User login handling"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session[CURR_USER_KEY] = user.id
            return redirect("/")
        else:
            form.username.errors = ["Invalid Username/Passwords"]

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """User register handling"""
    form = UserAddForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session[CURR_USER_KEY] = user.id
        flash("User Created", "success")
        return redirect("/")
    else:
        return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    session.pop(CURR_USER_KEY)
    flash("You have logged out successfully", "success")
    return redirect("/")
