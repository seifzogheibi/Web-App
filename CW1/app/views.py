from flask import render_template, flash, redirect, url_for
from .models import db, Assessment
from .forms import AssessmentForm
from datetime import datetime
from app import app, db, models


# The route for the home page,
# Ordering the assessments by closest deadline,
# Passing the data to the home template
@app.route('/')
def home():
    assessments = Assessment.query.order_by(Assessment.deadline.asc()).all()
    return render_template('home.html', assessments=assessments)


# Adding an assessment page
@app.route('/add_assessment', methods=['GET', 'POST'])
def add_assessment():
    form = AssessmentForm()
    today_date = datetime.now()

# Check that the submitted for is valid and is not a duplicate
    if form.validate_on_submit():
        duplicate_assessment = Assessment.query.filter_by(
            title=form.title.data,
            module_code=form.module_code.data
        ).first()

        if duplicate_assessment:
            flash('This assessment already exists')
        else:
            new_assessment = Assessment(
                title=form.title.data,
                module_code=form.module_code.data,
                deadline=form.deadline.data,
                description=form.description.data,
                completed=form.completed.data
            )
            try:
                # Adding the assessment to the database
                # then redirecting back to home
                db.session.add(new_assessment)
                db.session.commit()
                flash('Assessment added.')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding assessment: {e}')

    # Loop through form errors to check if validation fails
    for forms, errors in form.errors.items():
        for error in errors:
            flash(error)

    return render_template('add_assessment.html', form=form,
                           today_date=today_date)


# Edit button/page
@app.route('/edit_assessment/<int:id>', methods=['GET', 'POST'])
def edit_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    # Keeping the original data in the form when editing
    form = AssessmentForm(obj=assessment)

    # Making sure that duplicates cannot be entered through the edit page
    if form.validate_on_submit():
        duplicate_assessment = Assessment.query.filter(
            Assessment.title == form.title.data,
            Assessment.module_code == form.module_code.data,
            Assessment.id != id
        ).first()

        if duplicate_assessment:
            flash('This assessment already exists')

        else:
            # Update the data to the new one if successful
            form.populate_obj(assessment)
            try:
                db.session.commit()
                flash('Assessment updated.')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating assessment: {e}')

    for forms, errors in form.errors.items():
        for error in errors:
            flash(error)

    return render_template('edit.html', form=form)


# Complete button
@app.route('/complete/<int:id>', methods=['GET', 'POST'])
def complete_button(id):
    assessment = Assessment.query.get_or_404(id)
    # Using Boolean to set completed assessments to True
    # and incomplete to False
    assessment.completed = True
    try:
        db.session.commit()
        flash('Assessment completed!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking assessment as complete: {e}')

    return redirect(url_for('view_complete'))


# Incomplete button
@app.route('/incomplete/<int:id>', methods=['GET', 'POST'])
def incomplete_button(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.completed = False
    try:
        db.session.commit()
        flash('Assessment incomplete!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking assessment as incomplete: {e}')

    return redirect(url_for('view_incomplete'))


# Delete button
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    try:
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted.')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting assessment: {e}')

    return redirect(url_for('home'))


# Completed assessments page
@app.route('/view_complete')
def view_complete():
    # Filter to only display completed assessments
    complete_assessments = Assessment.query.filter_by(completed=True).all()
    return render_template('complete.html', assessments=complete_assessments)


# Incomplete assessments page
@app.route('/view_incomplete')
def view_incomplete():
    # Filter to only display incomplete assessments
    incomplete_assessments = Assessment.query.filter_by(completed=False).all()
    return render_template('incomplete.html',
                           assessments=incomplete_assessments)
