from flask_mail import Message
from flask import render_template, current_app

from server.server_extensions import mail
from mail.tokens_mail_generator import create_email_token, create_reset_token
from database import db
from config import Config

appname = Config.APP_NAME.upper()

def send_confirmation_newsletter_email(suscriber):
    """
    Envía un email de confirmación al suscriptor del newsletter.
    """
    try:
        token = create_email_token(suscriber.id)
        msg = Message(f'[{appname}] Confirme su suscripción', recipients=[suscriber.email])
        msg.html = render_template('email/confirm_newsletter_email.html', username=suscriber.name, token=token)
        mail.send(msg)
        
        current_app.logger.info(f"Confirmation email sent to {suscriber.email}.")
    
    except Exception as e:
        current_app.logger.error(f"Failed to send confirmation email to {suscriber.email}: {e}")

def send_reset_password_email(user):
    """
    Envía un email al usuario con un enlace para restablecer su contraseña.
    """
    try:

        token = create_reset_token(user.id)
        msg = Message(f'[{appname}] Restablecer su contraseña', recipients=[user.email])
        msg.html = render_template('email/reset_password.html', username=user.username, token=token)
        mail.send(msg)
        
        current_app.logger.info(f"Reset password email sent to {user.email}.")

    except Exception as e:
        current_app.logger.error(f"Failed to send reset password email to {user.email}: {e}")