from database import db
from database.models import Post, ContactMessage

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
    return redirect(url_for('blog'))

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/blog')
def blog():
    posts = Post.query.filter((Post.publish_date <= datetime.utcnow()) | (Post.publish_date == None)).order_by(Post.date_posted.desc()).all()
    for post in posts:
        post.content_summary = ' '.join(post.content.split()[:60]) + '...' # Mostrar las primeras 20 palabras
    return render_template('blog.html', posts=posts)

@main_bp.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    post.content = markdown.markdown(post.content)
    return render_template('post.html', post=post)

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
        return redirect(url_for('index'))
    return render_template('contact.html', title='Contacto', form=form)

@main_bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscriptionForm()
    if form.validate_on_submit():
        subscriber = Subscriber(name=form.name.data, email=form.email.data)
        db.session.add(subscriber)
        db.session.commit()
        flash('¡Gracias por suscribirte a nuestra newsletter!', 'success')
        return redirect(url_for('index'))
    return render_template('subscribe.html', form=form)