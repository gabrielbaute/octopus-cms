import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from database.models import Subscriber, Post
from database import db

# Cargar variables de entorno
load_dotenv()

# Variables de entorno
smtpserver = os.getenv("SMTP_SERVER")
smtpport = os.getenv("SMTP_PORT")
sender = os.getenv("EMAIL")
password = os.getenv("APP_PASS")
fromfield = os.getenv("FROM")

# Función para enviar newsletter
def send_newsletter(subject, html_template_path, app_context):
    with app_context:
        # Iniciar sesión en el servidor SMTP de Google
        try:
            server = smtplib.SMTP(smtpserver, smtpport)
            server.ehlo()
            server.starttls()
            server.login(sender, password)
            print('Inicio de sesión en SMTP exitoso')
        except smtplib.SMTPException as e:
            print(f'Error: No se pudo conectar: {e}')
            server.quit()
            return

        # Leer la plantilla HTML
        with open(html_template_path, 'r', encoding='utf-8') as file:
            html_template = file.read()

        # Recuperar el último post publicado
        last_post = Post.query.order_by(Post.publish_date.desc()).first()
        if not last_post:
            print('No hay posts para enviar en el newsletter.')
            return

        # Crear un resumen del contenido del post (primeras 100 palabras)
        content_summary = ' '.join(last_post.content.split()[:100]) + '...'

        # Enviar correo a cada suscriptor
        subscribers = Subscriber.query.all()
        for subscriber in subscribers:
            username = subscriber.name
            usermail = subscriber.email

            # Reemplazar variables en la plantilla
            html_content = html_template.format(
                user=username,
                post_title=last_post.title,
                post_author=last_post.author.username,
                post_date=last_post.date_posted.strftime('%d %b %Y'),
                post_content=content_summary
            )
            
            # Componer cabeceras del correo
            msg = MIMEMultipart()
            msg['From'] = fromfield
            msg['To'] = usermail
            msg['Subject'] = subject
            
            # Adjuntar el contenido HTML al mensaje
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            # Enviar el correo
            try:
                text = msg.as_string()
                server.sendmail(sender, usermail, text)
                print(f'Correo enviado exitosamente a {usermail}')
            except smtplib.SMTPException as e:
                print(f'Error: No se pudo enviar el correo a {usermail}: {e}')

        # Cerrar la conexión SMTP
        server.quit()
        print('Conexión SMTP cerrada')
