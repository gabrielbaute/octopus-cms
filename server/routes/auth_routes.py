from database import db
from database.models import User
from server.forms import LoginForm

from flask_bcrypt import Bcrypt 
from werkzeug.security import generate_password_hash, check_password_hash
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