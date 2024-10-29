from flask import render_template, flash, redirect, url_for
from .models import db, Assessment
from .forms import AssessmentForm
from datetime import datetime
from app import app, db, models

@app.route('/')
def home():
    assessments = Assessment.query.order_by(Assessment.deadline.asc()).all()
    return render_template('home.html', assessments=assessments)

@app.route('/add_assessment', methods=['GET', 'POST'])
def add_assessment():
    form = AssessmentForm()
    today_date = datetime.now()#.strftime('%d-%m-%Y')

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
            db.session.add(new_assessment)
            db.session.commit()
            flash('Assessment added.')
            return redirect(url_for('home'))  # Use direct function name
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding assessment: {e}')
    
    return render_template('add_assessment.html', form=form, today_date=today_date)

@app.route('/edit_assessment/<int:id>', methods=['GET', 'POST'])
def edit_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)
    
    if form.validate_on_submit():
        duplicate_assessment = Assessment.query.filter(
            Assessment.title == form.title.data,
            Assessment.module_code == form.module_code.data,
            Assessment.id != id  # Exclude the current assessment from the check
        ).first()

        if duplicate_assessment:
            flash('An assessment with this title and module code already exists.', 'error')
        
        
        else:
            form.populate_obj(assessment)
            try:
                db.session.commit()
                flash('Assessment updated.')
                return redirect(url_for('home'))  # Use direct function name
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating assessment: {e}')
    
    return render_template('edit.html', form=form)

@app.route('/complete/<int:id>', methods=['GET', 'POST'])
def complete_button(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.completed = True
    try:
        db.session.commit()
        flash('Assessment completed!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking assessment as complete: {e}')

    return redirect(url_for('view_complete'))  # Use direct function name

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

    return redirect(url_for('view_incomplete'))  # Use direct function name

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
    
    return redirect(url_for('home'))  # Use direct function name

@app.route('/view_complete')
def view_complete():
    complete_assessments = Assessment.query.filter_by(completed=True).all()
    return render_template('complete.html', assessments=complete_assessments)

@app.route('/view_incomplete')
def view_incomplete():
    incomplete_assessments = Assessment.query.filter_by(completed=False).all()
    return render_template('incomplete.html', assessments=incomplete_assessments)