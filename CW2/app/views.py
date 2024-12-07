"""
    Views
    """
import os
import random
from flask import render_template, redirect, request, flash, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from app.models import User, Post, Like, Comment, followers


@app.route('/')
def home():
    return redirect(url_for('login'))


# creating the authentication system
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize an error variable
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        error = "Password and email do not match."  # Set the error message

    return render_template('login.html', error=error)


# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        # securing passwords by hashing them with scrypt methods before storing in the database
        hashed_password = generate_password_hash(password)

        # store the new user in the db
        new_user = User(username=username, email=email,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# logout button
@app.route('/logout')
# adding this to all other routes to ensure the user is logged in
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


# home page
@app.route('/dashboard')
@login_required
def dashboard():
    # only show posts from the users followed list + their own in the home dashboard
    followed_posts = Post.query.join(followers, followers.c.followed_id == Post.user_id) \
                               .filter(followers.c.follower_id == current_user.id)
    own_posts = Post.query.filter_by(user_id=current_user.id)
    posts = followed_posts.union(own_posts).order_by(
        Post.timestamp.desc()).all()

    # adding counts for likes and comments
    for post in posts:
        post.like_count = post.likes.count()
        post.comment_count = post.comments.count()
        post.is_liked = Like.query.filter_by(
            user_id=current_user.id, post_id=post.id).first() is not None

    return render_template('dashboard.html', user=current_user, posts=posts)


# setting specific file extensions to only allow images to be uploaded
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# create a post
@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    print("create_post route called")
    content = request.form.get('content').strip()
    image = request.files.get('image')

    image_url = None
    print("Image received:", image)
    print("Upload folder:", app.config['UPLOAD_FOLDER'])
    print("Files received:", request.files.keys())

    # saving the file as an image in a folder
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        print(f"Saving image to {image_path}")
        image.save(image_path)
        image_url = f"uploads/{filename}"

    # add the post to the dashboard and commit it to the db
    if content or image_url:
        new_post = Post(content=content, image_url=image_url,
                        user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully.")
    else:
        flash("Post content or image cannot be empty.")
    return redirect(url_for('dashboard'))


# profile page
@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    followers_count = user.followers.count()
    following_count = user.following.count()

    print(followers_count)
    print(following_count)

    # get the users' posts
    posts = Post.query.filter_by(author=user).all()
    for post in posts:
        post.like_count = post.likes.count()
        post.is_liked = Like.query.filter_by(
            user_id=current_user.id, post_id=post.id).first() is not None

    is_current_user = user.id == current_user.id

    return render_template('profile.html', user=user, followers=followers_count,
                           following=following_count, posts=posts, is_current_user=is_current_user)


# like a post
@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(
        user_id=current_user.id, post_id=post_id).first()
    # unlike button
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        # dynmically return like count
        return jsonify({"status": "unliked", "like_count": post.likes.count(), "post_id": post_id})
    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({"status": "liked", "like_count": post.likes.count(), "post_id": post_id})


# comment button
@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    if request.method == 'POST':
        print("Form submitted successfully")
    print(f"Received comment for post_id {post_id}")
    content = request.form.get('content')
    print(f"Comment content: {content}")

    # making sure blank comments cant be posted
    if not content or not content.strip():
        flash("Comment cannot be empty.")
        return redirect(request.referrer or url_for('dashboard'))

    new_comment = Comment(content=content.strip(),
                          user_id=current_user.id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    flash("Comment added successfully.")
    return redirect(request.referrer or url_for('dashboard'))


# search for a user
@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '').strip()
    if not query:
        flash('Please enter a valid search query.')
        return redirect(url_for('dashboard'))

    # search for usernames that match the entered query
    results = User.query.filter(User.username.ilike(f'%{query}%')).all()
    return render_template('search.html', query=query, results=results)


# users
@app.route('/user/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc()).all()

    followers_count = user.followers.count()
    following_count = user.following.count()

    print(followers_count)
    print(following_count)
    return render_template('profile.html', user=user, posts=user_posts,
                           followers=followers_count, following=following_count)


# follow button
@app.route('/follow_toggle/<int:user_id>', methods=['POST'])
@login_required
def follow_toggle(user_id):
    user = User.query.get_or_404(user_id)

    # check if the user is already followed and toggle between following and unfollowing
    if user in current_user.following:
        current_user.following.remove(user)
        db.session.commit()
        flash(f"You unfollowed {user.username}.")
    else:
        current_user.following.append(user)
        db.session.commit()
        flash(f"You are now following {user.username}.")

    return redirect(url_for('profile', username=user.username))


# delete a post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # only let the author delete the post
    if post.user_id != current_user.id:
        return jsonify({"status": "failure", "error": "Unauthorized"}), 403

    # delete the post's likes and comments as well
    Like.query.filter_by(post_id=post_id).delete()
    Comment.query.filter_by(post_id=post_id).delete()

    db.session.delete(post)
    db.session.commit()

    return jsonify({"status": "success", "post_id": post_id}), 200


# delete a comment
@app.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    coment = Comment.query.get_or_404(comment_id)
    if coment.author != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(coment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200


# edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        bio = request.form.get('bio').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # making sure emails can't be changed to existing ones
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != current_user.id:
            flash('Email is already taken.', 'danger')
            return redirect(url_for('edit_profile'))

        # updated the changes
        current_user.username = username
        current_user.bio = bio
        current_user.email = email

        # hash the new password as well before storing
        if password:
            current_user.password = generate_password_hash(password)

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    return render_template('edit_profile.html', user=current_user)


# display the post on a full page
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments.all()

    post.like_count = post.likes.count()
    post.is_liked = Like.query.filter_by(
        user_id=current_user.id, post_id=post.id).first() is not None

    return render_template('view_post.html', post=post, comments=comments)


# explore page
@app.route('/explore')
@login_required
def explore():
    posts = Post.query.all()

    random.shuffle(posts)

    return render_template('explore.html', posts=posts)


# viewing followers and following only accessed from the users profile
@app.route('/followers/<username>')
@login_required
def followers_page(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user.id != current_user.id:
        flash("You are not authorized to view this page.", "danger")
        return redirect(url_for('dashboard'))

    followers_list = user.followers
    return render_template('followers.html', user=user, followers=followers_list)


@app.route('/following/<username>')
@login_required
def following_page(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user.id != current_user.id:
        flash("You are not authorized to view this page.", "danger")
        return redirect(url_for('dashboard'))

    following_list = user.following
    return render_template('following.html', user=user, following=following_list)
