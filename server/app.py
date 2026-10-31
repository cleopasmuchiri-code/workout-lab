from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

# The workout routes


@app.route("/workouts", methods=["GET"])
def get_workouts():
    return make_response({"message": "list all workouts"}, 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    return make_response({"message": f"show workout {id}"}, 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    return make_response({"message": "create a workout"}, 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    return make_response({"message": f"delete workout {id}"}, 200)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    return make_response({"message": "list all exercises"}, 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    return make_response({"message": f"show exercise {id}"}, 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    return make_response({"message": "create an exercise"}, 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    return make_response({"message": f"delete exercise {id}"}, 200)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    return make_response(
        {"message": f"add exercise {exercise_id} to workout {workout_id}"}, 201
    )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
