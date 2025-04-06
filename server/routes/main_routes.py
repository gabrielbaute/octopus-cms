from database import db
from database.models import Post, ContactMessage, Subscriber
from server.forms import ContactForm, SubscriptionForm
from mail import send_confirmation_newsletter_email, decode_email_token

import markdown
from datetime import datetime
from flask import(
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
)

main_bp = Blueprint('main', __name__, template_folder='templates')

# Rutas de la navegación de la app
@main_bp.route('/')
def index():
    return redirect(url_for('main.blog'))

@main_bp.route('/about')
def about():
    return render_template('public/about.html')

@main_bp.route('/blog')
def blog():
    posts = Post.query.filter((Post.publish_date <= datetime.utcnow()) | (Post.publish_date == None)).order_by(Post.date_posted.desc()).all()
    for post in posts:
        post.content_summary = ' '.join(post.content.split()[:60]) + '...' # Mostrar las primeras 20 palabras
    return render_template('public/blog.html', posts=posts)

@main_bp.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    post.content = markdown.markdown(post.content)
    return render_template('public/post.html', post=post)

@main_bp.route('/contact', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('public/contact.html', title='Contacto', form=form)

@main_bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscriptionForm()

    if form.validate_on_submit():
        subscriber = Subscriber(name=form.name.data, email=form.email.data)
    
        db.session.add(subscriber)
        db.session.commit()

        send_confirmation_newsletter_email(subscriber)
    
        flash('¡Gracias por suscribirte a nuestra newsletter!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('public/subscribe.html', form=form)

@main_bp.route('/confirm_subscription/<token>')
def confirm_subscription(token):
    subscriber_id = decode_email_token(token)

    if subscriber_id is None:
        flash('El enlace de confirmación no es válido o ha expirado. Debe volver a suscribirse.', 'danger')
        return redirect(url_for('main.subscribe'))
    
    subscriber = Subscriber.query.get(subscriber_id)

    if subscriber.is_active:
        flash('Ya te has suscrito, puedes seguir navegando!', 'success')
        return redirect(url_for('main.index'))
    
    # Activar la suscripción del usuario
    subscriber.is_active = True
    db.session.commit()

    flash('¡Felicidades! Gracias por suscribirte a nuestro newsletter y mantenerte atento a nuestras publicaciones.', 'success')
    return redirect(url_for('main.index'))
    