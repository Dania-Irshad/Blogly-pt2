from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "sec_ret$0987"
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    return redirect("/users")

@app.route("/users")
def list_users():
    """Display all users"""
    users = User.query.all()
    return render_template("users/users.html", users=users)

@app.route("/users/new")
def new_user():
    """Display new user form."""
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def get_user():
    """Add new user and redirect to users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Display details of the user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    """Display edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def get_updated_user(user_id):
    """Edit user and redirect to detail page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to homepage"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Display details of the user's post"""
    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def get_post(user_id):
    """Add post and redirect to user detail page"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user.id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """Display details of the post"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/detail.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    """Display edit post form."""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def get_updated_post(post_id):
    """Edit post and redirect to post detail page"""
    title = request.form['title']
    content = request.form['content']
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post and redirect to user detail page"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")