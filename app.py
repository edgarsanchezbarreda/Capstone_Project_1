import os, requests, json, random, math

from flask import Flask, request,  render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Exercise, User_Workout
from forms import EditAccountForm, MacrosForm, SignUpForm, LoginForm, GoalForm, EquipmentTypeForm

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

def random_exercise_selection(list, n):
    return random.sample(list, n)

target_muscles = ['abs', 'biceps', 'delts', 'hamstrings', 'lats', 'pectorals', 'quads', 'triceps']

###############################################
# API Request URL

API_BASE_URL = "https://exercisedb.p.rapidapi.com"

headers = {
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
	"X-RapidAPI-Key": "223bb7db04mshd8ae1af744fb12ep12e2b5jsn8b10ff422736"
}


###############################################
# Homepage route

@app.route('/')
def home():
    """Checks if user is logged in, and displays the appropriate page."""
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
    """Allows user to sign up."""
    form = SignUpForm()

    if form.validate_on_submit():
        user = User.signup(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
            )
        db.session.commit()

        do_login(user)

        return redirect(f"/home/{user.id}")

    else:
        return render_template('users/signup.html', form=form)

    
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login."""

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



@app.route('/user/account', methods = ['GET', 'POST'])
def user_account():
    """Dislays user account and handles editing username and email."""
    
    user_id = session[CURR_USER_KEY]
    user = User.query.get(user_id)

    form = EditAccountForm(obj=user)

    if form.validate_on_submit():
        """Check if password input is valid."""

        user = User.authenticate(form.username.data, 
                                form.password.data)

        if user:
            """If password was valid, update user profile and redirect to user home page."""
            user.email = form.email.data
            user.username = form.username.data    
            
            db.session.commit()                        
            return redirect(f"/home/{user_id}")
        else:
            flash("Invalid password.", 'danger')
            return redirect(f"/home/{user_id}")
    return render_template('/users/user_account.html', user = user, form = form)



################################
# Questionnaire 

@app.route('/questionnaire/<int:user_id>', methods = ['GET', 'POST'])
def questionnaire_start(user_id):
    """Asks user's goal."""
    user = User.query.get(user_id)

    form = GoalForm()

    if form.validate_on_submit():
        user.goal = form.goal.data
        db.session.commit()
        return redirect(f"/questionnaire/{user.id}/macros")

    return render_template('/users/questionnaire_start.html', user = user, form = form)


@app.route('/questionnaire/<int:user_id>/macros')
def questionnaire_macros(user_id):
    """Asks user if they want to calculate macros."""
    
    user = User.query.get(user_id)

    return render_template('/users/questionnaire_macros.html', user = user)




################################
# Macros Calculation

@app.route('/macros/<int:user_id>', methods=['GET', 'POST'])
def calculate_macros(user_id):
    """Renders calculate macros page and handles calculation of macros"""

    user = User.query.get(user_id)

    form = MacrosForm()

    if form.validate_on_submit():
        if form.gender.data == 'male':
            weight_calc = form.weight.data*10
            height_calc = form.height.data*6.25
            age_calc = (form.age.data * 5)

            BMR = (weight_calc + height_calc) - age_calc + 5
            
            macros_calculated = math.ceil(BMR * float(form.activity_level.data))
            
            user.gender = form.gender.data
            user.age = form.age.data
            user.height = form.height.data
            user.weight = form.weight.data
            user.activity_level = form.activity_level.data
            user.calorie_maintenance = macros_calculated,
            user.protein = math.ceil(form.weight.data * 2.2),
            user.carbohydrate = math.ceil((macros_calculated * .2)/4),
            user.fat = math.ceil((macros_calculated * .4)/9)    
            
            db.session.commit()
            
            return redirect(f"/macros/{user.id}/detail")
        
        else:
            weight_calc = form.weight.data*10
            height_calc = form.height.data*6.25
            age_calc = (form.age.data * 5)

            BMR = (weight_calc + height_calc) - age_calc - 161
            
            macros_calculated = math.ceil(BMR * float(form.activity_level.data))
            
            user.gender = form.gender.data
            user.age = form.age.data
            user.height = form.height.data
            user.weight = form.weight.data
            user.activity_level = form.activity_level.data
            user.calorie_maintenance = macros_calculated,
            user.protein = math.ceil((form.weight.data * 2.2)),
            user.carbohydrate = math.ceil((macros_calculated * .2)/4),
            user.fat = math.ceil((macros_calculated * .4)/9)    
            
            db.session.commit()
            
            return redirect(f"/macros/{user.id}/detail")

    return render_template('users/macros.html', user=user, form=form)

@app.route('/macros/<int:user_id>/detail')
def next(user_id):
    """Displays user's macronutrient and calorie intake breakdown."""
    user = User.query.get(user_id)

    return render_template('users/macros_detail.html', user = user)


@app.route(f"/macros/<int:user_id>/view")
def view_calories(user_id):
    user = User.query.get(user_id)

    return render_template('/users/view_calories.html', user = user)



###############################
# Program Details and Questionnaire

@app.route('/program/<int:user_id>', methods = ['GET', 'POST'])
def program_choice(user_id):
    """This route allows a user to select the equipment that is available to them, and generates a random workout program based off their goal and equipment type."""
    user = User.query.get(user_id)

    form = EquipmentTypeForm()
    
    if form.validate_on_submit():
        user.equipment_type = form.equipment_type.data
        db.session.commit()
        if not user.exercises:
            for muscle in target_muscles:
                response = requests.request("GET", f"{API_BASE_URL}/exercises/target/{muscle}", headers = headers)
                
                data = response.json()
                exercises = [e for e in data if e['equipment'] == user.equipment_type]
                
                random_exercise = random_exercise_selection(exercises, 1)
                
                user_exercise = Exercise(
                    name = random_exercise[0]['name'],
                    target_muscle = random_exercise[0]['target'],
                    exercise_gif = random_exercise[0]['gifUrl'],
                    equipment_type = random_exercise[0]['equipment'],
                    user_id = user.id
                )

                db.session.add(user_exercise)
                db.session.commit()

                for exercise in user.exercises:
                    if user.goal == 'gain strength':
                        exercise.sets_per_exercise = 5,
                        exercise.reps_per_set = '4-6',
                        exercise.weight = '80% of 1 rep max'
                        db.session.commit()
                    else:
                        exercise.sets_per_exercise = 4,
                        exercise.reps_per_set = '10-12',
                        exercise.weight = '60% of 1 rep max'
                        db.session.commit()

                user_workout = User_Workout(
                    user_id = user.id,
                    exercise_id = user_exercise.id
                )
                db.session.add(user_workout)
                db.session.commit()

        return redirect(f"/program/{user.id}/template")
    return render_template('program/program_choice.html', user = user, form = form)


@app.route('/program/<int:user_id>/template')
def generate_program(user_id):
    """This form will display their generated program."""
    user = User.query.get(user_id)
    ids = range(1,9)
    user_ids = zip(user.exercises, ids)
    return render_template('/program/program_template.html', user = user, target_muscles = target_muscles, ids = ids, user_ids = user_ids)

@app.route('/program/<int:user_id>/template/delete', methods = ['POST'])
def delete_program(user_id):
    """Deletes workoute program."""
    user = User.query.get(user_id)
    
    for exercises in user.exercises:
        db.session.delete(exercises)
    db.session.commit()

    return redirect(f"/program/{user.id}")
