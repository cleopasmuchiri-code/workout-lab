#!/usr/bin/env python3

from datetime import date

from app import app
from models import *

with app.app_context():

    # 1. Clear old data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # 2. Create exercises
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    bench = Exercise(name="Bench press", category="strength", equipment_needed=True)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)
    db.session.add_all([pushup, squat, bench, plank])

    # 3. Create workouts
    monday = Workout(date=date(2026, 11, 2), duration_minutes=45, notes="Upper body")
    friday = Workout(date=date(2026, 11, 6), duration_minutes=30, notes="Full body")
    db.session.add_all([monday, friday])

    # 4. Link them (the join table rows)
    links = [
        WorkoutExercise(workout=monday, exercise=pushup, sets=3, reps=10),
        WorkoutExercise(workout=monday, exercise=bench, sets=4, reps=8),
        WorkoutExercise(workout=friday, exercise=pushup, sets=4, reps=12),
        WorkoutExercise(workout=friday, exercise=squat, sets=3, reps=15),
        WorkoutExercise(workout=friday, exercise=plank, duration_seconds=60),
    ]
    db.session.add_all(links)

    db.session.commit()
    print("Database seeded!")
