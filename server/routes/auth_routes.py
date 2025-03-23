from database import db
from database.models import User
from server.forms import LoginForm, ForgotPasswordForm, ResetPasswordForm
from mail import send_reset_password_email, decode_reset_token

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import(
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    request,
    current_app
)

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    remember=form.remember.data
    
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first()
            
            if check_password_hash(user.password, password):
                login_user(user, remember)
                flash('Login successful', 'success')
                
                next_page = request.args.get('next')
                current_app.logger.info(f"Sesión iniciada por {email}")
                
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
                #return redirect(url_for('main.index')                

            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        except Exception as e:
            current_app.logger.error(f"Error al iniciar sesion: {e}")

    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    user = current_user
    current_app.logger.info(f"Sesión cerrada por {user.email}")
    logout_user()
    return redirect(url_for('main.index'))



@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        
        if user:
            send_reset_password_email(user)
        
        flash('Si existe una cuenta con ese correo electrónico, se ha enviado un enlace de restablecimiento de contraseña.', 'success')
        
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        user_id = decode_reset_token(token)
    except:
        flash('El enlace de restablecimiento no es válido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.get(user_id)

        # Verificar que la contraseña no haya sido utilizada antes
        for old_password in user.password_history:
            if check_password_hash(old_password.password_hash, password):
                flash('No es posible reutilizar una contraseña anterior. Elija una diferente.', 'danger')
                return redirect(url_for('auth.reset_password', token=token))

        # Actualizar la contraseña del usuario
        user.password = generate_password_hash(password, method='pbkdf2:sha256')

        db.session.commit()
        #send_password_change_notification(user, request.remote_addr)
        flash('Su contraseña ha sido restablecida. Ya puede iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)