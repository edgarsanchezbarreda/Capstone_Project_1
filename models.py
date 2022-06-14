from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

bcrypt = Bcrypt()
db = SQLAlchemy()



class User(db.Model):
    """A registered user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text, nullable = False, unique = True)

    email = db.Column(db.Text, nullable = False, unique = True)

    password = db.Column(db.Text, nullable = False)

    age = db.Column(db.Integer)

    height = db.Column(db.Integer)

    weight = db.Column(db.Integer)

    gender = db.Column(db.Text)

    activity_level = db.Column(db.Text)

    body_fat = db.Column(db.Integer)

    goal = db.Column(db.Text)

    macros = db.relationship('Macros')

    exercises = db.relationship('Exercise')


    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


    @classmethod
    def calculate_macros(cls, self, gender, age, height, weight, activity_level, body_fat):
        """Calculate macros if body fat is included"""

        # sedentary = 1.2
        # light_exercise = 1.375
        # moderate_exercise = 1.55
        # heavy_exercise = 1.725
        # athlete = 1.9
        user = User.query.filter_by(self.id).first()

        if gender == 'Male':

            weight_calc = weight*10
            height_calc = height*10
            age_calc = (age*5) + 5

            BMR = weight_calc + height_calc - age_calc
            macros_calculated = BMR * activity_level

            macros = Macros(
                calorie_maintenance=macros_calculated,
                protein = weight,
                carbohydrate = 100,
                fat = 100,
                user_id = user.id      
                )
            db.session.add(macros)
            db.session.commit()
            print(macros_calculated)
            return macros_calculated
        else:
            weight_calc = weight*10
            height_calc = height*10
            age_calc = (age*5) - 161

            BMR = weight_calc + height_calc - age_calc
            macros_calculated = BMR * activity_level

            macros = Macros(
                calorie_maintenance=macros_calculated,
                protein = weight,
                carbohydrate = 100,
                fat = 100,
                user_id = user.id      
                )
            db.session.add(macros)
            db.session.commit()
            print(macros_calculated)
            return macros_calculated  

class Exercise(db.Model):
    """An individual exercise/movement"""

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False)

    target_muscle = db.Column(db.Text, nullable = False)

    exercise_gif = db.Column(db.Text)

    sets_per_exercise = db.Column(db.Integer, nullable = False)

    reps_per_set = db.Column(db.Integer, nullable = False)

    equipment_type = db.Column(db.Text, nullable = False, unique = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))


class User_Workout(db.Model):
    """A table that stores an individual user's exercises."""
    __tablename__ = 'user_workout'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete = 'cascade'))



class Macros(db.Model):
    """The recommended daily macronutrient and calorie intake based off user's goal, age, height, weight, and activity level """

    __tablename__ = 'macros'

    id = db.Column(db.Integer, primary_key = True)

    calorie_maintenance = db.Column(db.Integer, nullable = False)

    protein = db.Column(db.Integer, nullable = False)

    carbohydrate = db.Column(db.Integer, nullable = False)

    fat = db.Column(db.Integer, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), nullable = False)


def connect_db(app):
    db.app = app
    db.init_app(app)