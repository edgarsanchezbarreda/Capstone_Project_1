import requests
from flask import session
from app import db
from models import User, Exercise, User_Workout

db.drop_all()
db.create_all()

# edgar = User(
#     username = 'EdgarS',
#     email = 'edgars@gmail.com',
#     password = 'EdgarS',
#     age = 27,
#     height = 175,
#     weight = 100,
#     gender = 'Male',
#     activity_level = 'Sedentary',
#     goal = 'Lose Weight'
# )

# hilda = User(
#     username = 'HildaA',
#     email = 'hildaa@gmail.com',
#     password = 'HildaA',
#     age = 26,
#     height = 150,
#     weight = 73,
#     gender = 'Female',
#     activity_level = 'Sedentary',
#     goal = 'Gain Muscle'
# )

# db.session.add(edgar)
# db.session.add(hilda)
# db.session.commit()