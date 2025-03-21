from database import db
from database.models import User, ContactMessage, Post
from server.forms import RegistrationForm, NewsletterForm
from server.roles import admin_required
from mail import send_newsletter_mail

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required
from flask import(
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    request,
    current_app
)

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegistrationForm()
    new_username = form.username.data
    new_email = form.email.data
    new_password = form.password.data
    role = form.role.data

    if form.validate_on_submit():
        user_by_username = User.query.filter_by(username=new_username).first()
        user_by_email = User.query.filter_by(email=new_email).first()
        
        if user_by_username:
            flash('Username already exists. Please choose a different one.', 'danger')
        
        elif user_by_email:
            flash('Email already exists. Please choose a different one.', 'danger')
        
        else:
            hashed_password = generate_password_hash(new_password)
            user = User(username=new_username, email=new_email, password=hashed_password, role=role)

            try:
                db.session.add(user)
                db.session.commit()
                current_app.logger.info(f"Nuevo usuario creado por {current_user.email}. Username: {new_username}, Email: {new_email}, Rol: {role}")
            
            except Exception as e:
                current_app.logger.error(f"Error al crear nuevo usuario: {e}")

            flash('The user account has been created!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@admin_bp.route('/send_newsletter', methods=['GET', 'POST'])
@login_required
@admin_required
def send_newsletter_route():
    form = NewsletterForm()
    if request.method == 'POST':
        subject = request.form['subject']
        html_template_path = 'templates/newsletter.html'
        #send_newsletter_mail(post)
        flash('Newsletter enviado exitosamente.', 'success')
        return redirect(url_for('index'))
    return render_template('send_newsletter.html', form=form)

@admin_bp.route('/contact-messages')
@login_required
@admin_required
def contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
    return render_template('contact_messages.html', messages=messages)