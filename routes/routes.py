from flask import Blueprints, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, NewPostForm, ContactForm, SubscriptionForm, NewsletterForm
from database import db
from database.models import Post
from roles import author_required
from datetime import datetime


def init_routes(app):
    # Rutas de gestión de posts
    @app.route('/new-post', methods=['GET', 'POST'])
    @login_required
    @author_required
    def new_post():
        form = NewPostForm()
        if form.validate_on_submit():
            publish_date = form.publish_date.data if form.publish_date.data else datetime.utcnow()
            post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, publish_date=publish_date)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('blog'))
        return render_template('new_post.html', title='Nuevo Post', form=form)

    @app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
    @login_required
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)  # Forbidden

        form = NewPostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('blog'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('new_post.html', title='Edit Post', form=form)

    @app.route('/delete-post/<int:post_id>', methods=['POST'])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)  # Forbidden

        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('blog'))
