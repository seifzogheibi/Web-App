from flask import render_template, flash, redirect, url_for
from flask import Blueprint
from models import db, Assessment
from forms import AssessmentForm
from datetime import datetime

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    assessments = Assessment.query.all()  # Get all assessments
    return render_template('index.html', assessments=assessments)  # Check if 'index.html' exists in templates

@views_bp.route('/manage', methods=['GET', 'POST'])  # Change route to /manage
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
            flash('New assessment added successfully!')  # Show success message
            return redirect(url_for('views.add_assessment'))  # Redirect after successful submission
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error adding assessment: {e}')
    
    return render_template('add_assessment.html', form=form, today_date=today_date)  # Render the manage template with the form and assessment

@views_bp.route('/edit/<int:id>', methods=['GET', 'POST'])  # Ensure this route exists
def edit_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)  # Pre-populate form with current data
    
    if form.validate_on_submit():
        form.populate_obj(assessment)  # Populate the assessment object with form data
        try:
            db.session.commit()
            flash('Assessment updated successfully!')
            return redirect(url_for('views.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating assessment: {e}')
    
    return render_template('edit.html', form=form)  # Render the edit template with the form

@views_bp.route('/complete/<int:id>')
def complete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.completed = True  # Mark as complete
    try:
        db.session.commit()
        flash('Assessment marked as complete!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking assessment as complete: {e}')
    
    return redirect(url_for('views.index'))  # Redirect back to the index page

@views_bp.route('/delete/<int:id>')
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    try:
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted.')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting assessment: {e}')
    
    return redirect(url_for('views.index'))  # Redirect back to the index page

@views_bp.route('/view_complete')
def view_complete():
    # Fetch assessments that are marked as complete
    complete_assessments = Assessment.query.filter_by(completed=True).all()
    return render_template('view_assessments.html', assessments=complete_assessments, title="Complete Assessments", page_type='complete')

@views_bp.route('/view_incomplete')
def view_incomplete():
    # Fetch assessments that are not marked as complete
    incomplete_assessments = Assessment.query.filter_by(completed=False).all()
    return render_template('view_assessments.html', assessments=incomplete_assessments, title="Incomplete Assessments", page_type='incomplete')