from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    """A form for users to create an account."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class MacrosForm(FlaskForm):
    """Form used to calculate macros."""

    gender = SelectField('Gender', choices = [('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])

    age = IntegerField('Age', validators=[DataRequired()])

    height = FloatField('Height in cm', validators=[DataRequired()])

    weight = FloatField('Weight in kg', validators=[DataRequired()])

    activity_level = SelectField('Activity Level', choices = [(1.2, 'Sedentary (office job)'), (1.375, 'Light Exercise (1-2 days/week)'), (1.55, 'Moderate Exercise (3-5 days/week)'), (1.725, 'Heavy Exercise (6-7 days/week)'), (1.9, 'Athlete (2x per day)')
    ], validators=[DataRequired()])
