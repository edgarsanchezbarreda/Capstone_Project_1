from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from forms import MacrosForm

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

    calorie_maintenance = db.Column(db.Float)

    protein = db.Column(db.Float)

    carbohydrate = db.Column(db.Float)

    fat = db.Column(db.Float)

    activity_level = db.Column(db.Float)

    goal = db.Column(db.Text)

    equipment_type = db.Column(db.Text)

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


class Exercise(db.Model):
    """An individual exercise/movement"""

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.Text, nullable = False)

    target_muscle = db.Column(db.Text, nullable = False)

    exercise_gif = db.Column(db.Text)

    sets_per_exercise = db.Column(db.Integer)

    reps_per_set = db.Column(db.Text)

    weight = db.Column(db.Text)

    equipment_type = db.Column(db.Text, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))


class User_Workout(db.Model):
    """A table that stores an individual user's exercises."""
    __tablename__ = 'user_workout'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete = 'cascade'))



def connect_db(app):
    db.app = app
    db.init_app(app)