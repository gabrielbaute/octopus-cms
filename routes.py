from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, NewPostForm, ContactForm, SubscriptionForm, NewsletterForm
from database import db
from database.models import User, Post, ContactMessage, Subscriber
from roles import admin_required, author_required
from mail import send_newsletter
from datetime import datetime
from flask_bcrypt import Bcrypt 
import markdown


def init_routes(app):
    # Rutas de Autenticación y Gestión de Usuarios:
    @app.route('/subscribe', methods=['GET', 'POST'])
    def subscribe():
        form = SubscriptionForm()
        if form.validate_on_submit():
            subscriber = Subscriber(name=form.name.data, email=form.email.data)
            db.session.add(subscriber)
            db.session.commit()
            flash('¡Gracias por suscribirte a nuestra newsletter!', 'success')
            return redirect(url_for('index'))
        return render_template('subscribe.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register():
        bcrypt = Bcrypt(app)
        form = RegistrationForm()
        if form.validate_on_submit():
            user_by_username = User.query.filter_by(username=form.username.data).first()
            user_by_email = User.query.filter_by(email=form.email.data).first()
            if user_by_username:
                flash('Username already exists. Please choose a different one.', 'danger')
            elif user_by_email:
                flash('Email already exists. Please choose a different one.', 'danger')
            else:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
                db.session.add(user)
                db.session.commit()
                flash('The user account has been created!', 'success')
                return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route('/send_newsletter', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def send_newsletter_route():
        form = NewsletterForm()
        if request.method == 'POST':
            subject = request.form['subject']
            html_template_path = 'templates/newsletter.html'
            send_newsletter(subject, html_template_path, app.app_context())
            flash('Newsletter enviado exitosamente.', 'success')
            return redirect(url_for('index'))
        return render_template('send_newsletter.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            bcrypt = Bcrypt(app)
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login successful', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

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

    # Rutas de la navegación de la app
    @app.route('/')
    def index():
        return redirect(url_for('blog'))

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/blog')
    def blog():
        posts = Post.query.filter((Post.publish_date <= datetime.utcnow()) | (Post.publish_date == None)).order_by(Post.date_posted.desc()).all()
        for post in posts:
            post.content_summary = ' '.join(post.content.split()[:60]) + '...' # Mostrar las primeras 20 palabras
        return render_template('blog.html', posts=posts)

    @app.route('/post/<slug>')
    def post(slug):
        post = Post.query.filter_by(slug=slug).first_or_404()
        post.content = markdown.markdown(post.content)
        return render_template('post.html', post=post)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            contact_message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(contact_message)
            db.session.commit()
            flash('Tu mensaje ha sido enviado. ¡Gracias por contactarnos!', 'success')
            return redirect(url_for('index'))
        return render_template('contact.html', title='Contacto', form=form)

    @app.route('/contact-messages')
    @login_required
    @admin_required
    def contact_messages():
        messages = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
        return render_template('contact_messages.html', messages=messages)
