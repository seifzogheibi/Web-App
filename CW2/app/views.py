# from app import app, db, admin
# from flask_admin.contrib.sqla import ModelView
# from .models import Property, Landlord

# admin.add_view(ModelView(Property, db.session))
# admin.add_view(ModelView(Landlord, db.session))

# @app.route('/')
# def index():
#     return "Hello World!!!"

# from flask import Flask, request
# from flask_restful import Resource, Api

# app = Flask(__name__)
# api = Api(app)

# tasks = {}

# class TaskResource(Resource):
#     def get(self, task_id):
#         return {task_id: tasks[task_id]}

#     def put(self, task_id):
#         tasks[task_id] = request.form['data']
#         return {task_id: tasks[task_id]}

# api.add_resource(TaskResource, '/<string:task_id>')

# if __name__ == '__main__':
#     app.run(debug=True)


# Add Login/Registration Views:
from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))
