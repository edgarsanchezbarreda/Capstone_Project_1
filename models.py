from enum import unique
from re import L
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

bcrypt = Bcrypt()
db = SQLAlchemy()



class User(db.Model):
    """A registered user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.Text, nullable = False)

    last_name = db.Column(db.Text, nullable = False)

    age = db.Column(db.Integer, nullable = False)

    height = db.Column(db.Integer, nullable = False)

    weight = db.Column(db.Integer, nullable = False)

    email = db.Column(db.Text, nullable = False, unique = True)

    acitivity_level = db.Column(db.Text)

    goal = db.Column(db.Text, nullable = False)

    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id', ondelete='cascade'))

    user_workout_id = db.Column(db.Integer, db.ForeignKey('user_workout.id', ondelete='cascade'))

    macros_id = db.Column(db.Integer, db.ForeignKey('macros.id', ondelete='cascade'))



class Equipment(db.Model):
    """The type of equipment that is available to a user."""

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False, unique = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))



class Muscle_Group(db.Model):
    """An individual muscle group."""

    __tablename__ = 'muscle_group'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False, unique = True)



class Exercise(db.Model):
    """An individual exercise/movement"""

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False)

    equipment_type = db.Column(db.Text, nullable = False)



class User_Workout(db.Model):
    """"A workout that is generated for a user based off their user information and responses to the questionnaire"""

    __tablename__ = 'user_workout'

    id = db.Column(db.Integer, primary_key = True)

    sets_per_exercise = db.Column(db.Integer, nullable = False)

    reps_per_set = db.Column(db.Integer, nullable = False)

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete='cascade'))



class Macros(db.Model):
    """The recommended daily macronutrient and calorie intake based off user's goal, age, height, weight, and activity level """

    __tablename__ = 'macros'

    id = db.Column(db.Integer, primary_key = True)

    calorie_maintenance = db.Column(db.Integer, nullable = False)

    protein = db.Column(db.Integer, nullable = False)

    carbohydrate = db.Column(db.Integer, nullable = False)

    fat = db.Column(db.Integer, nullable = False)



def connect_db(app):
    db.app = app
    db.init_app(app)