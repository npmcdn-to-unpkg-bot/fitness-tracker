"""Models and database functions for Fitness project."""

from flask_sqlalchemy import SQLAlchemy
import bcrypt
# import correlation

# Connection to the PostgreSQL database through the Flask-SQLAlchemy library.
# On this, we can find the `session` object, where we do most of our interactions.

db = SQLAlchemy()

##############################################################################
# Model definitions

class Exercise(db.Model):
    """Exercise that will be performed by users."""

    __tablename__ = "exercises"

    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable=True)
    exercise_description = db.Column(db.String(500), nullable=True)
    exercise_category = db.Column(db.String(300), nullable=True)
    exercise_muscle_group = db.Column(db.String(300), nullable=True)
    exercise_alias = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Exercise exercise_id=%s exercise_name=%s exercise_description=%s>" % (self.exercise_id, 
            self.exercise_name, self.exercise_description)


class MuscleGroup(db.Model):
    """Muscle groups targeted by exercises."""

    __tablename__ = "muscleGroups"

    muscleGroup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'))
    muscleGroup_name = db.Column(db.String(100), nullable=True)
    muscleGroup_description = db.Column(db.String(500), nullable=True)
    muscleGroup_alias = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<MuscleGroup muscleGroup_id=%s exercise_id=%s muscleGroup_name=%s>" % (self.muscleGroup_id, 
            self.exercise_id, self.muscleGroup_name)

class MuscleGroupExerciseLink(db.Model):
    """Association table connecting exercises to muscle groups that the exercise targets."""

    __tablename__ = "muscleGroup_exercise_link"

    muscleGroup_id = db.Column(db.Integer, db.ForeignKey('muscleGroups.muscleGroup_id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), primary_key=True)
    # UniqueConstraint('muscleGroup_id', 'exercise_id')

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<MuscleGroupExerciseLink muscleGroup_id=%s exercise_id=%s>" % (self.muscleGroup_id, self.exercise_id)


class Equipment(db.Model):
    """Equipment used during exercises."""

    __tablename__ = "equipments"

    equipment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'))
    equipment_name = db.Column(db.String(100), nullable=True)
    equipment_description = db.Column(db.String(500), nullable=True)
    equipment_alias = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Equipment equipment_id=%s exercise_id=%s equipment_name=%s>" % (self.equipment_id, 
            self.exercise_id, self.equipment_name)

class EquipmentExerciseLink(db.Model):
    """Association table connecting exercises to equipment that exercises require to be performed."""

    __tablename__ = "equipment_exercise_link"

    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.equipment_id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), primary_key=True)
    # UniqueConstraint('muscleGroup_id', 'exercise_id')

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<EquipmentExerciseLink equipment_id=%s exercise_id=%s>" % (self.equipment_id, self.exercise_id)


class Workout(db.Model):
    """Workouts that will be created by users."""

    __tablename__ = "workouts"

    workout_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    workout_name = db.Column(db.String(100), nullable=True)
    workout_description = db.Column(db.String(500), nullable=True)

    #Define relationship to user
    user = db.relationship("User", backref=db.backref("walks", order_by=workout_id))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Workout workout_id=%s user_id=%s workout_name=%s>" % (self.workoutout_id, 
            self.user_id, self.workout_name)

class WorkoutExerciseLink(db.Model):
    """Association table connecting workouts to exercises with unique constraint."""

    __tablename__ = "workout_exercise_link"

    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), primary_key=True)
    # UniqueConstraint('workout_id', 'exercise_id')

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<WorkoutExerciseLink workout_id=%s exercise_id=%s>" % (self.workout_id, self.exercise_id)


class ExerciseImage(db.Model):
    """Exercise images uploaded by admin to demonstrate exercises and workouts."""

    __tablename__ = "exercise_images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('landmarks.landmark_id'))
    imageurl = db.Column(db.String(255), nullable=False)

    # Define relationship to exercise
    exercise = db.relationship("Exercise", backref=db.backref('images'))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<ExerciseImage image_id=%s exercise_id=%s imageurl=%s>" % (self.image_id, self.exercise_id, self.imageurl)


class User(db.Model):
    """User of fitness website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(70), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    salt = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)
           
    def __init__(self, email, password):
        """Instantiate a user object within the User class with salted passwords."""

        self.email = email
        self.salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf8'), self.salt.encode('utf8'))

    def verify_password(self, password):
        """Verify user's password, a method that can be called on a user."""

        password_hash = bcrypt.hashpw(password.encode('utf8'), self.salt.encode('utf8'))

        if self.password_hash == password_hash:
            return True
        else:
            return False

    def similarity(self, other):
        """Return Pearson rating for user compared to other user."""

        u_ratings = {}
        paired_ratings = []

        for r in self.ratings:
            u_ratings[r.landmark_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.landmark_id)
            if u_r:
                paired_ratings.append( (u_r.user_score, r.user_score) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)

        else:
            return 0.0

    def predict_rating(self, landmark):
        """Predict a user's rating of a landmark."""

        other_ratings = landmark.ratings
        other_users = [ r.user for r in other_ratings ]

        similarities = [
            (self.similarity(other_user), other_user)
            for other_user in other_users
        ]

        similarities.sort(reverse=True)
        sim, best_match_user = similarities[0]

        matched_rating = None
        for rating in other_ratings:
            if rating.user_id == best_match_user.user_id:
                return rating.user_score * sim

class UserSaved(db.Model):
    """Saved exercises as favorited by users."""
    # 'Save' in lieu of 'Favorite', pinterest saw a bump in activity, less commitment.  users who SAVE similar exercises,
    # may also be interested in similar exericses
    # FIXME: save workouts too???

    __tablename__ = "user_saved"

    saved_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # Define relationship to exercise
    exercise = db.relationship("Exercise", backref=db.backref('saved'))
    # Define relationship to user
    user = db.relationship("User", backref=db.backref('saved'))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<UserSaved saved_id=%s exercise_id=%s user_id=%s>" % (self.saved_id, self.exercise_id, self.user_id)

    def __init__(self, landmark_id, user_id):
        """Instantiate a user object within the User class with salted passwords."""

        self.exercise_id = exercise_id
        self.user_id = user_id
        self.saved = []

# class Rating(db.Model):
#     """Ratings score of exercise given by users."""

#     __tablename__ = "ratings"

#     rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     exercise_id = db.Column(db.Integer, db.ForeignKey('landmarks.landmark_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     user_score = db.Column(db.Integer, nullable=False)

#     # Define relationship to user
#     user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

#     # Define relationship to landmark
#     exercise = db.relationship("Exercise", backref=db.backref("ratings", order_by=rating_id))

#     def __repr__(self):
#         """Provide helpful representation when printed, for human readability."""

#         return "<Rating rating_id=%s exercise_id=%s user_id=%s user_score=%s>" % (self.rating_id, 
#             self.exercise_id, self.user_id, self.user_score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///exercises'
    db.app = app
    db.init_app(app)



if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
