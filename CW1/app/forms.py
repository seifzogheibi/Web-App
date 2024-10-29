from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, DateField, TextAreaField, BooleanField, ValidationError
from wtforms.validators import DataRequired
from datetime import date

class AssessmentForm(FlaskForm):
    title = StringField('Assessment Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    deadline = DateField('Deadline Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    completed = BooleanField('Completed')
    # submit = SubmitField('Add Assessment')

    def validate_deadline(form, field):
        if field.data < date.today():
            raise ValidationError("Deadline cannot be in the past.")