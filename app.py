"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts, Tag, PostTag

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_user_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "bloglyusers123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Homepage redirects to list of users."""
    posts = Posts.query.order_by(Posts.created_at.desc()).limit(5).all()
    print("LOADING HOMEPAGE")
    tags = Tag.query.order_by(Tag.id.desc()).limit(5).all()

    return render_template("posts/homepage.html", posts=posts, tags=tags)


@app.errorhandler(404)
def page_not_found(e):
    """SHOW 404 NOT FOUND page."""

    return render_template("404.html"), 404


# user routes


@app.route("/users")
def list_users():
    """show list of users"""
    users = Users.query.order_by(Users.last_name, Users.first_name).all()
    print(users[0].first_name)
    return render_template("list.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_user_form():
    """create new user from form"""
    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = Users(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = Users.query.get_or_404(user_id)
    print(f"You picked {user.full_name}")
    return render_template("users/show.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """show details of new user"""
    user = Users.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_update(user_id):
    """Handle form submission for updating user"""

    user = Users.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    flash(f"This user: {user.full_name} was added.")

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} is no more.")

    return redirect("/users")


# post routes
@app.route("/users/<int:user_id>/posts/new")
def new_posts_form(user_id):
    """show form to create a new post from a specific user"""
    user = Users.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """handle the submission for a new post"""
    user = Users.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Posts(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
        tags=tags,
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """show info on post"""
    post = Posts.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Posts.query.get_or_404(post_id)
    tags = Tag.query.all()
    print("edit post")
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_posts(post_id):
    """edit an existing post"""
    post = Posts.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    print("edit form ")
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f" Post '{post.title}' editted ")
    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete an exisiting post"""
    post = Posts.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted")

    return redirect(f"/users/{post.user_id}")


# tag routes


@app.route("/tag")
def display_tags():
    """show all tags"""

    tags = Tag.query.all()
    return render_template("tag/details.html", tags=tags)


@app.route("/tag/new")
def new_tag_form():
    """display new tag form"""
    posts = Posts.query.all()

    return render_template("tag/new.html", posts=posts)


@app.route("/tag/new", methods=["POST"])
def new_tags():
    """handle new tag form"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Posts.query.filter(Posts.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"new tag: `{new_tag.name}` added")

    return redirect("/tag")


@app.route("/tag/<int:tag_id>")
def show_tags(tag_id):
    """show a page with info on a tag"""
    tag = Tag.query.get_or_404(tag_id)
    print(f"You picked {tag.id}")
    return render_template("tag/show.html", tag=tag)


@app.route("/tag/<int:tag_id>/edit")
def edit_tag(tag_id):
    """edit a tags info"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Posts.query.all()

    return render_template("tag/edit.html", tag=tag, posts=posts)


@app.route("/tag/<int:tag_id>/edit", methods=["POST"])
def edit_tag_form(tag_id):
    """handle editted tag form"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Posts.query.filter(Posts.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"user tag: '{tag.name}'was updated.")

    return redirect("/tag")


@app.route("/tag/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"your tag:'{tag.name}' is deleted.")

    return redirect("/tag")
