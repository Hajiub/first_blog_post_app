from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .validator import PostModel
from .models import Post, User, Comment, Like
from . import db
from sqlalchemy.orm import joinedload
from sqlalchemy import func

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    posts = Post.query.options(joinedload(Post.user)).order_by(Post.created_at).all()
    
    for post in posts:
        post.likes_count = db.session.query(func.count(Like.id)).filter_by(post_id=post.id).scalar()
        post.comments_count = db.session.query(func.count(Comment.id)).filter_by(post_id=post.id).scalar()

    return render_template('index.html',posts=posts)
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/create_post')
@login_required
def create_post():
    return render_template('create_post.html')


@main.route('/create_post', methods=['POST'])
@login_required
def post_it():
    try:
        post_data = PostModel(**request.form)
        post      = Post(**post_data.dict(),user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    except ValueError as e:
        errors = e.errors()
        flash(errors)        
        return redirect(url_for('main.create_post'))

@main.route('/like/<int:post_id>')
@login_required  # Assuming you have authentication set up
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the user has already liked the post
    if like := Like.query.filter_by(user_id=current_user.id, post_id=post.id).first():
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('main.index'))

    # Create a new like entry
    like = Like(user_id=current_user.id, post_id=post.id)
    db.session.add(like)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/detail/<int:post_id>')
@login_required
def detail(post_id):
   
   post     = Post.query.options(joinedload(Post.user)).filter_by(id=post_id).first()
   comments = Comment.query.filter_by(post_id=post.id).all()
   query = db.session.query(Comment.content, User.username, Post.content)\
        .join(User, User.id == Comment.user_id)\
        .join(Post, Post.id == Comment.post_id)\
        .filter(Comment.post_id == post_id)\
        .all()

   context = {
       'post': post,
       'comments': comments,
       'query':query,
   }

   return render_template('detail.html', context=context)


@main.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not post:
        abort(404)

    elif not content.strip():
        flash('Comment cannot be a white space!')
        return redirect(url_for('main.detail', post_id=post.id))
    
    comment = Comment(user_id=current_user.id, post_id=post.id, content=content)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('main.detail', post_id=post.id))
    