from database import db
from database.models import User, ContactMessage
from forms import RegistrationForm, NewsletterForm
from roles import admin_required
from mail import send_newsletter

import markdown
from flask_bcrypt import Bcrypt 
from flask_login import current_user, logout_user, login_required, a
from flask import(
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    request
)

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    bcrypt = Bcrypt(admin_bp)
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

@admin_bp.route('/send_newsletter', methods=['GET', 'POST'])
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

@admin_bp.route('/contact-messages')
@login_required
@admin_required
def contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
    return render_template('contact_messages.html', messages=messages)