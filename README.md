# Workout Tracker Project Moringa

A simple backend built in Flask, Marshmallow, SQLAlchemy backend for a workout tracking app used by personal trainers.

## Set - Up

1. Clone the repo and move into it:
   ```bash
   git clone <your-repo-link>
   cd workout-app
   ```
2. Install dependencies and open the virtual environment:
   ```bash
   pipenv install 3.11
   pipenv shell
   ```
3. Create the database and load example data:
   ```bash
    cd server
    flask db init
    flask db migrate -m "create exercises table"
    flask db upgrade head
   ```

`python seed.py` - useful when stuck, resets the data

## Run

From the `server` folder:

```bash
flask run
```

The API is then available at `http://127.0.0.1:5555`.

## Endpoints

| Method | Path                                                               | Description                                                                           |
| ------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| GET    | `/workouts`                                                        | List all workouts                                                                     |
| GET    | `/workouts/<id>`                                                   | Show one workout with its exercises, including reps, sets and duration                |
| POST   | `/workouts`                                                        | Create a workout. Body: `date` (YYYY-MM-DD), `duration_minutes`, optional `notes`     |
| DELETE | `/workouts/<id>`                                                   | Delete a workout and its associated WorkoutExercises                                  |
| GET    | `/exercises`                                                       | List all exercises                                                                    |
| GET    | `/exercises/<id>`                                                  | Show one exercise and the workouts it appears in                                      |
| POST   | `/exercises`                                                       | Create an exercise. Body: `name`, `category`, optional `equipment_needed`             |
| DELETE | `/exercises/<id>`                                                  | Delete an exercise and its associated WorkoutExercises                                |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Body: `reps` and/or `duration_seconds`, optional `sets` |

Valid categories: strength, cardio, flexibility, balance, core.

Errors are returned as JSON: `400` for invalid data, `404` when a record isn't found, `409` when a database constraint is violated (for example a duplicate).

## Validations

- **Table constraints:** unique exercise names, non-blank name, valid category, positive duration, notes length limit, positive reps/sets/duration_seconds, and a unique (workout, exercise) pair.
- **Model validations:** `@validates` checks on names, categories, duration, notes, dates and reps/sets/duration_seconds.
- **Schema validations:** required fields, value ranges, allowed categories, no future dates, and a rule that reps or duration_seconds must be provided when adding an exercise to a workout.
