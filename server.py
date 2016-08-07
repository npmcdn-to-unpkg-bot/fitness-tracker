
import sqlalchemy
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, Response
from flask_debugtoolbar import DebugToolbarExtension

from model import Exercise, User, MuscleGroup, Workout, Equipment, MuscleGroupExerciseLink, WorkoutExerciseLink, EquipmentExerciseLink, ExerciseImage, UserSaved, connect_to_db, db

import os
import json
import bcrypt
import requests

import smtplib
from email.mime.text import MIMEText

from datetime import date


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["FLASK_SECRET_KEY"]







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
    # app.run(host='0.0.0.0')