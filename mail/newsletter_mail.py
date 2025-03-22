from flask_mail import Message
from flask import render_template

from database.models import Post, Subscriber
from .config_mail import appname, mail


def newsletter_mail(subscriber, post):
    """
    Envía un email con el último post publicado.
    """

    content_summary = ' '.join(post.content.split()[:100]) + '...'
    
    try:
        msg = Message(f'[{appname}] Nuevo post!', recipients=[subscriber.email])
        msg.html = render_template(
            'email/newsletter',
            user=subscriber.name,
            post_title=post.title,
            post_author=post.author.username,
            post_date=post.publish_date.strftime('%d %b %Y'),
            post_content=content_summary
            )
        mail.send(msg)
    
    except Exception as e:
        print(f"Error al enviar el newsletter a {subscriber.email}: {e}")

    pass


def send_newsletter_mail(post):
    """
    Envía un email con el último post publicado de forma masiva a todos los usuarios suscritos
    """

    subscribers = Subscriber.query.get(is_active=True)
    try:
        for subscriber in subscribers:
            newsletter_mail(subscriber, post)
    except Exception as e:
        print(f"Error al enviar el newsletter a {subscriber.email}: {e}")