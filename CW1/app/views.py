from flask import render_template, flash, redirect, url_for
from .models import db, Assessment
from .forms import AssessmentForm
from datetime import datetime
from . import create_app

app = create_app()

@app.route('/')
def home():
    assessments = Assessment.query.all()  # Get all assessments
    return render_template('home.html', assessments=assessments)  # Check if 'index.html' exists in templates

@app.route('/add_assessment', methods=['GET', 'POST'])  # Change route to /manage
def add_assessment():
    form = AssessmentForm()  # Create an instance of the form
    #assessment = None  # Initialize the assessment variable
    
    today_date = datetime.now().strftime('%Y-%m-%d')

    if form.validate_on_submit():  # Check if the form is submitted and valid
        new_assessment = Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            deadline=form.deadline.data,
            description=form.description.data,
            completed=form.completed.data
        )
        try:
            db.session.add(new_assessment)  # Add the new assessment to the session
            db.session.commit()  # Commit the session to save changes
            flash('Assessment added.')  # Show success message
            return redirect(url_for('views.home'))  # Redirect after successful submission
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error adding assessment: {e}')
    
    return render_template('add_assessment.html', form=form, today_date=today_date)  # Render the manage template with the form and assessment

@app.route('/edit_assessment', methods=['GET', 'POST'])  # Ensure this route exists
def edit_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)  # Pre-populate form with current data
    
    if form.validate_on_submit():
        form.populate_obj(assessment)  # Populate the assessment object with form data
        try:
            db.session.commit()
            flash('Assessment updated.')
            return redirect(url_for('views.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating assessment: {e}')
    
    return render_template('edit.html', form=form)  # Render the edit template with the form

@app.route('/complete', methods=['GET', 'POST'])
def complete_button(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.completed = True  # Mark as complete
    try:
        db.session.commit()
        flash('Assessment completed!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking assessment as complete: {e}')

    return redirect(url_for('views.view_complete'))  #

@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_button(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.completed = False  # Mark as incomplete
    try:
        db.session.commit()
        flash('Assessment incomplete!')  # Flash message for success
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking assessment as incomplete: {e}')  # Flash message for error

    return redirect(url_for('views.view_incomplete'))  # Redirect back to the index page

@app.route('/delete', methods=['GET', 'POST'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    try:
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted.')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting assessment: {e}')
    
    return redirect(url_for('views.home'))  # Redirect back to the index page

@app.route('/view_complete')
def view_complete():
    # Fetch assessments that are marked as complete
    complete_assessments = Assessment.query.filter_by(completed=True).all()
    return render_template('complete.html', assessments=complete_assessments)

@app.route('/view_incomplete')
def view_incomplete():
    # Fetch assessments that are not marked as complete
    incomplete_assessments = Assessment.query.filter_by(completed=False).all()
    return render_template('incomplete.html', assessments=incomplete_assessments)