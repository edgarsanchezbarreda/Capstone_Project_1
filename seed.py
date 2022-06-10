import requests
from app import db, response, exercise_data, API_BASE_URL, headers
from models import User, Equipment, Muscle_Group, Exercise, User_Workout, Macros

db.drop_all()
db.create_all()

def fetch_equipment():
    response = requests.request("GET", f"{API_BASE_URL}/exercises/equipmentList", headers=headers)
    data = response.json()

    for equipment in data:
        equipment_type = Equipment(name = equipment)

        db.session.add(equipment_type)
    db.session.commit()

fetch_equipment()

def fetch_muscle_group():
    response = requests.request("GET", f"{API_BASE_URL}/exercises/targetList", headers=headers)
    data = response.json()

    for muscle_group in data:
        target_muscle = Muscle_Group(name = muscle_group)

        db.session.add(target_muscle)
    db.session.commit()

fetch_muscle_group()

def fetch_exercises(type):
    response = requests.request("GET", f"{API_BASE_URL}/exercises", headers=headers)
    data = response.json()

    for equipment in data:
        e = Exercise(name = equipment['name'], equipment_type = {type})

        db.session.add(e)
    db.session.commit()

fetch_exercises('barbell')
fetch_exercises('bodyweight')
