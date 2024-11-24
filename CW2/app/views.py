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
from flask import render_template, redirect, request, flash, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Post, Like, Comment, followers


@app.route('/')
def home():
    return redirect(url_for('login'))

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    followed_posts = Post.query.join(followers, followers.c.followed_id == Post.user_id) \
                               .filter(followers.c.follower_id == current_user.id)
    own_posts = Post.query.filter_by(user_id=current_user.id)
    posts = followed_posts.union(own_posts).order_by(Post.timestamp.desc()).all()

    # Add a count of likes for each post
    for post in posts:
        post.like_count = post.likes.count()
    return render_template('dashboard.html', user=current_user, posts=posts)


@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    content = data.get('content')
    if content:
        new_post = Post(content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({
            "status": "success",
            "content": content,
            "author": current_user.username,
            "timestamp": new_post.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({"status": "failure"})

@app.route('/profile')
@login_required
def profile():
    # Query the user's posts
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
    
    return render_template('profile.html', user=current_user, posts=user_posts)


@app.route('/like', methods=['POST'])
@login_required
def like():
    data = request.get_json()
    post_id = data.get('post_id')

    # Check if the user already liked the post
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_like:
        db.session.delete(existing_like)  # Unlike if already liked
        db.session.commit()
        return jsonify({"status": "unliked", "post_id": post_id})

    # Add new like
    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({"status": "liked", "post_id": post_id})


@app.route('/comment', methods=['POST'])
@login_required
def comment():
    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content')

    if not content.strip():
        return jsonify({"status": "failure", "error": "Comment cannot be empty."})

    # Add new comment
    new_comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "status": "success",
        "post_id": post_id,
        "comment": {
            "author": current_user.username,
            "content": content,
            "timestamp": new_comment.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '').strip()
    if not query:
        flash('Please enter a valid search query.')
        return redirect(url_for('dashboard'))

    # Search for users whose username matches the query
    results = User.query.filter(User.username.ilike(f'%{query}%')).all()
    return render_template('search.html', query=query, results=results)


@app.route('/user/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()

    return render_template('profile.html', user=user, posts=user_posts)


@app.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user_to_follow = User.query.get_or_404(user_id)
    if user_to_follow != current_user and user_to_follow not in current_user.following:
        current_user.following.append(user_to_follow)
        db.session.commit()
    return redirect(url_for('view_profile', user_id=user_id))


@app.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get_or_404(user_id)
    if user_to_unfollow in current_user.following:
        current_user.following.remove(user_to_unfollow)
        db.session.commit()
    return redirect(url_for('view_profile', user_id=user_id))
