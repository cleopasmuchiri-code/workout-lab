from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import *
from schemas import *
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()

# The workout routes


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(jsonify(workout_detail_schema.dump(workout)), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    json_data = request.get_json(silent=True)
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        data = workout_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 400)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "Could not save workout"}), 409)

    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted"}), 200)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    json_data = request.get_json(silent=True)
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 400)
    except IntegrityError:
        db.session.rollback()
        return make_response(
            jsonify({"error": "An exercise with that name already exists"}), 409
        )

    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted"}), 200)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    json_data = request.get_json(silent=True)
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        data = workout_exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        link = WorkoutExercise(workout=workout, exercise=exercise, **data)
        db.session.add(link)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 400)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "Could not save workout exercise"}), 409)

    return make_response(jsonify(workout_exercise_schema.dump(link)), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
