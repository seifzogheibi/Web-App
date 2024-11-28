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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign Up successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')


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

    # Add a count of likes for each post and whether the user has liked the post
    for post in posts:
        post.like_count = post.likes.count()
        post.is_liked = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None

    return render_template('dashboard.html', user=current_user, posts=posts)



@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content')
    if content.strip():
        new_post = Post(content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully.")
    else:
        flash("Post content cannot be empty.")
    return redirect(url_for('dashboard'))


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    followers_count = user.followers.count()
    following_count = user.following.count()
    posts = Post.query.filter_by(author=user).all()

    # Calculate followers and following counts
    followers_count = user.followers.count()
    following_count = user.following.count()

    is_current_user = user.id == current_user.id

    # Add like count and check if the current user liked each post
    for post in posts:
        post.like_count = post.likes.count()
        post.is_liked = current_user in [like.user for like in post.likes]

    return render_template('profile.html', user=user, followers=followers_count, current_user=current_user, following=following_count, posts=posts, is_current_user=is_current_user)


@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_like:
        db.session.delete(existing_like)  # Unlike
        db.session.commit()
        return jsonify({"status": "unliked", "like_count": post.likes.count(), "post_id": post_id})
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"status": "liked", "like_count": post.likes.count(), "post_id": post_id})


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')

    if not content or not content.strip():
        app.logger.error(f"Failed to add comment: Empty content for post ID {post_id}")
        flash("Comment cannot be empty.")
        return redirect(request.referrer or url_for('dashboard'))

    new_comment = Comment(content=content.strip(), user_id=current_user.id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    app.logger.info(f"New comment added by {current_user.username} for post ID {post_id}")
    flash("Comment added successfully.")
    return redirect(request.referrer or url_for('dashboard'))




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


@app.route('/follow_toggle/<int:user_id>', methods=['POST'])
@login_required
def follow_toggle(user_id):
    user = User.query.get_or_404(user_id)

    # Check if the user is already followed
    if user in current_user.following:
        current_user.following.remove(user)
        db.session.commit()
        flash(f"You unfollowed {user.username}.")
    else:
        current_user.following.append(user)
        db.session.commit()
        flash(f"You are now following {user.username}.")

    # Redirect back to the profile page
    return redirect(url_for('profile', username=user.username))



@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        return jsonify({"status": "failure", "error": "Unauthorized"}), 403

    # Delete associated likes and comments
    Like.query.filter_by(post_id=post_id).delete()
    Comment.query.filter_by(post_id=post_id).delete()

    db.session.delete(post)
    db.session.commit()
    return jsonify({"status": "success", "post_id": post_id}), 200




@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash("You don't have permission to delete this comment.")
        return redirect(url_for('dashboard'))

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully.")
    return redirect(url_for('dashboard'))
