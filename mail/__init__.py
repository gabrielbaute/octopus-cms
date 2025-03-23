from .newsletter_mail import send_newsletter_mail, newsletter_mail
from .config_mail import mail
from .tokens_mail_generator import(
    create_email_token,
    decode_email_token,
    create_reset_token,
    decode_reset_token)
from .auth_mail import send_confirmation_newsletter_email, send_reset_password_email
from .notifications_mail import send_welcome_email, send_password_change_notification