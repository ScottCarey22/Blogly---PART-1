"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE = "https://image.shutterstock.com/image-vector/default-avatar-profile-icon-social-260nw-1677509740.jpg"


class Users(db.Model):
    """USERS."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=False)
    last_name = db.Column(db.Text, nullable=False, unique=False)
    image_url = db.Column(db.Text, nullable=False, unique=False, default=DEFAULT_IMAGE)

    posts = db.relationship("Posts", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """full name of user."""
        print("I am inside the full name")
        print(f"{self.first_name} {self.last_name}")
        return f"{self.first_name} {self.last_name}"

    def greet(self):
        """Welcome New User"""
        return f"Hello {self.first_name} {self.last_name}, nice to meet you!"

    def __repr__(self):
        """show user information"""
        u = self
        return f"<Users id={u.id} name={u.first_name}{u.last_name}>"


class Posts(db.Model):
    """Posts db"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def show_date(self):
        """return date"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)
