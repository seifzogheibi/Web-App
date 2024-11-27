# from app import db

# class Property(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(500), index=True, unique=True)
#     start_date = db.Column(db.DateTime)
#     duration = db.Column(db.Integer)
#     rent = db.Column(db.Float)
#     landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))

#     def __repr__(self):
#             return '{}{}{}{}{}'.format(self.id, self.address, self.start_date, self.duration, self.rent)

# class Landlord(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     name = db.Column(db.String(500), index=True)
#     contact_number = db.Column(db.String(20))
#     address = db.Column(db.String(500), index=True, unique=True)
#     properties = db.relationship('Property', backref='landlord', lazy='dynamic')

#     def __repr__(self):
#             return '{}{}{}'.format(self.id, self.name, self.contact_number)


from app import db
from flask_login import UserMixin
from datetime import datetime, timezone



followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # date_joined = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='post', cascade="all, delete-orphan", lazy='dynamic')
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan", lazy='dynamic')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref='likes', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    # Add relationship to User model
    author = db.relationship('User', backref='comments', lazy=True)