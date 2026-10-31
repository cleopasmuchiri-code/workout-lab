from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(validate=validate.Length(max=50))
    equipment_needed = fields.Bool()


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(validate=validate.Range(min=1))
    notes = fields.Str()


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1))
    sets = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int(validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def check_something_was_done(self, data, **kwargs):
        if not any(data.get(key) for key in ("reps", "sets", "duration_seconds")):
            raise ValidationError(
                "Provide reps, sets, or duration_seconds.", field_name="reps"
            )


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.Nested(WorkoutSchema, many=True, dump_only=True)
