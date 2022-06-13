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



class Equipment(db.Model):
    """The type of equipment that is available to a user."""

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False, unique = True)


class User_Equipment(db.Model):
    """The equipment type that user will use."""

    __tablename__ = 'user_equipment'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))

    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id', ondelete = 'cascade'))


class Exercise(db.Model):
    """An individual exercise/movement"""

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False)

    target_muscle = db.Column(db.Text, nullable = False)

    exercise_gif = db.Column(db.Text)

    sets_per_exercise = db.Column(db.Integer, nullable = False)

    reps_per_set = db.Column(db.Integer, nullable = False)

    equipment_type = db.Column(db.Integer, db.ForeignKey('equipment.id', ondelete='cascade'))


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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))


def connect_db(app):
    db.app = app
    db.init_app(app)