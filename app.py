import os, requests, json, random

from flask import Flask, request,  render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Exercise, User_Workout
from forms import MacrosForm, SignUpForm, LoginForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
os.environ.get('DATABASE_URL', 'postgresql:///fit_app')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
app.config['SQLALCHEMY_ECHO'] =  False
app.config['SECRET_KEY'] =  'helloworld123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

###############################################
# API Request URL

API_BASE_URL = "https://exercisedb.p.rapidapi.com"

headers = {
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
	"X-RapidAPI-Key": "7ddbb671c3msh5ac6eca10dce7d9p1c4f61jsna698597b6a3f"
}

###############################################
# Homepage route

@app.route('/')
def home():
    if g.user:
        
        return render_template('home.html')

    else:
        return render_template('index.html')
@app.route('/home/<int:user_id>')
def home_logged_in_user(user_id):
    if g.user:
        user = User.query.get(user_id)
        return render_template('home.html', user=user)

    else:
        return render_template('index.html')
@app.route('/home/<int:user_id>')
def homepage(user_id):
    if g.user:
        user = User.query.get(user_id)
        return render_template('home.html', user=user)

    else:
        return render_template('index.html')


###############################################
#Signup, Login, Logout routes

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        # try:
        user = User.signup(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
            )
        db.session.commit()

        # except IntegrityError:
        #     flash("Username already taken", 'danger')
        #     return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect(f"/home/{user.id}")

    else:
        return render_template('users/signup.html', form=form)

    
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/home/{user.id}")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle logout of user."""
    session.pop(CURR_USER_KEY)
    flash("You have logged out!", "success")
    return redirect('/login')


################################
# Macros Calculation

@app.route('/macros', methods=['GET', 'POST'])
def calculate_macros():
    """Renders calculate macros page and handles calculation of macros"""

    user_id = session[CURR_USER_KEY]
    user = User.query.get(user_id)

    form = MacrosForm()

    if form.validate_on_submit():
        if form.gender.data == 'male':
            weight_calc = form.weight.data*10
            height_calc = form.height.data*6.25
            age_calc = (form.age.data * 5) + 5
            print(age_calc)
            BMR = weight_calc + height_calc - age_calc
            print(BMR)
            macros_calculated = BMR * float(form.activity_level.data)
            print(macros_calculated)
            user.gender = form.gender.data
            user.age = form.age.data
            user.height = form.height.data
            user.weight = form.weight.data
            user.activity_level = form.activity_level.data
            user.calorie_maintenance = macros_calculated,
            user.protein = (macros_calculated * .4)/4,
            user.carbohydrate = (macros_calculated * .2)/4,
            user.fat = (macros_calculated * .4)/9    
            
            db.session.commit()
            
            return redirect(f"macros/{user_id}/next")
        
        else:
            weight_calc = form.weight.data*10
            height_calc = form.height.data*6.25
            age_calc = (form.age.data * 5) - 161
            print(age_calc)
            BMR = weight_calc + height_calc - age_calc
            print(BMR)
            macros_calculated = BMR * float(form.activity_level.data)
            print(macros_calculated)
            user.gender = form.gender.data
            user.age = form.age.data
            user.height = form.height.data
            user.weight = form.weight.data
            user.activity_level = form.activity_level.data
            user.calorie_maintenance = macros_calculated,
            user.protein = (macros_calculated * .4)/4,
            user.carbohydrate = (macros_calculated * .2)/4,
            user.fat = (macros_calculated * .4)/9    
            
            db.session.commit()
            
            return redirect(f"macros/{user_id}/next")

    return render_template('users/macros.html', user=user, form=form)

@app.route('/macros/<int:user_id>/next')
def next(user_id):
    user = User.query.get(user_id)

    return render_template('users/next.html', user = user)