# Capstone 1 Project

My Capstone Project is called [FitGen](https://edgar-fit-app.herokuapp.com/).
I chose this title because the function of this app is to generate a fitness program for people who are looking for a quick exercise program.

Users start at the home page, where they are asked to create an account in order to be able to use the app. A user will then enter their username, email, and a password to register their accoubnt. My app uses the tool bcrypt to hash the user's password and safely store their information in my database.

The registered user is then directed to the start of the questionnaire, where they are asked what their primary fitness goal is, and then whether they would like to calculate the macronutrients and calories needed to best accomplish their goal. If the user elects to calculate their mactronutients and caloric intake, they are directed to a route where they input their sex, age, height, weight, and activity level. Based off their answers the app implements the Mifflin-St Jeor basal metabolic rate formula to calculate the total daily energy expenditure(TDEE), or the daily caloric intake needed to maintain the user's current weight.

The user also receives a recommendation for their daily protein, carbohydrate, and fat intake that would best fit their goal.

Next, the user can select whether they would like a program that includes barbell exercises, or only body weight exercises. This is where the app fetches exercises from the [ExerciseDB](https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb) API and randomly selects one exercise per major body part. 

Lastly, a program is generated containing one exercise per major body part consisting of exercises that fit the exercise equipment type the user previously selected, along with the exercise name, the body part assigned to it, the sets and reps for that exercise, the recommended weight to be used, and a gif showing how to exercise is performed.

A user has the ability to delete their current program and generate a new one, log in and out of their account, and edit their username and email.

The tech stack used for this is Python with Flask and SQLAlchemy, Postgres, HTML, and CSS.