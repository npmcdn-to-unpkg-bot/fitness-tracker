
from flask import Flask, render_template, redirect

import os

from model import connect_to_db, db, Exercise, MuscleGroup, MuscleGroupExerciseLink, Equipment, EquipmentExerciseLink, Workout, WorkoutExerciseLink, ExerciseImage, User, UserSaved

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["FLASK_SECRET_KEY"]

if __name__ == "__main__":

    connect_to_db(app)
    app.run()