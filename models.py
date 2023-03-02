"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = "https://image.shutterstock.com/image-vector/default-avatar-profile-icon-social-260nw-1677509740.jpg"


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """USERS."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=False)
    last_name = db.Column(db.Text, nullable=False, unique=False)
    image_url = db.Column(db.Text, nullable=False, unique=False, default=DEFAULT_IMAGE)


@property
def full_name(self):
    """full name of user."""

    return f"{self.first_name} {self.last_name}"


def greet(self):
    """Welcome New User"""
    return f"Hello {self.first_name} {self.last_name}, nice to meet you!"


def __repr__(self):
    """show user information"""
    u = self
    return f"<User id={u.id} name={u.first_name}{u.last_name}>"
