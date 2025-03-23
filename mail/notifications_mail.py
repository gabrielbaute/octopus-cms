from flask_mail import Message
from flask import render_template, current_app, request

from mail.config_mail import mail
from database import db
from config import Config

appname = Config.APP_NAME.upper()

def send_welcome_email(user):
    try:
        """
        Envía un correo de bienvenida al usuario después de crear su cuenta.
        """
        # Configurar el mensaje
        msg = Message(
            subject=f"¡Bienvenido a {appname}!",
            recipients=[user.email]
        )
        msg.html = render_template(
            "mail/welcome_email.html",
            username=user.username
        )
        mail.send(msg)

        current_app.logger.info(f"Welcome email sent to {user.email}.")

    except Exception as e:
        current_app.logger.error(f"Failed to welcome email to {user.email}: {e}")

def send_password_change_notification(user, ip_address):
    try:
        """
        Envía una notificación por email al usuario cuando se detecta que la contraseña ha sido cambiada.
        """
        device = request.user_agent.platform
        browser = request.user_agent.browser

        # Renderizar la plantilla con los datos
        msg = Message(f'[{appname}] Su contraseña ha sido cambiada!', recipients=[user.email])
        msg.html = render_template(
            'mail/password_changed_notification.html',
            username=user.username,
            ip_address=ip_address,
            device=device,
            browser=browser
        )
        mail.send(msg)

        current_app.logger.info(f"Password change notification email sent to {user.email} from IP {ip_address} via {device}/{browser}.")
    
    except Exception as e:
        current_app.logger.error(f"Failed to send password change notification email to {user.email} from IP {ip_address} via {device}.: {e}")