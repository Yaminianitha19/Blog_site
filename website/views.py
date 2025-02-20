from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db


views = Blueprint("views", __name__)



@views.route("/")
@views.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created Successfully!', category='success')
            return redirect(url_for('views.posts', username=current_user.username))

    return render_template("home.html", user=current_user)

@views.route("/create-post", methods=['GET','POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
    
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created Successfully!', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", category="success")
    
    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist.", category="error")
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).order_by(Post.date_created.desc()).all()
    return render_template("post.html", user=current_user, posts=posts, username=username)
