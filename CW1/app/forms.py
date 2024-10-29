from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, BooleanField
from wtforms import TextAreaField, ValidationError
from wtforms.validators import DataRequired
from datetime import date


# Creating the forms of where the data will be entered
# and making sure no field can be empty
class AssessmentForm(FlaskForm):
    title = StringField('Assessment Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    deadline = DateField('Deadline Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    completed = BooleanField('Completed')

    # Validation check to make sure the form doesnt accept past deadlines
    def validate_deadline(form, field):
        if field.data < date.today():
            raise ValidationError("Deadline cannot be in the past.")
