import os, requests, json, random
from flask import Flask, request,  render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Equipment, User_Equipment, Exercise, User_Workout, Macros

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
    response = requests.request("GET", f"{API_BASE_URL}/exercises/bodyPart/chest", headers=headers)
    data = response.json()
    rand = (random.sample(data, 3))
    return render_template('index.html', data=data, rand = rand)