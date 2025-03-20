from flask import Flask
from dotenv import load_dotenv
from os import getenv
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_migrate import Migrate
from database import db
from database.models import User
from loadadmin import create_admin_user
import markdown
import routes

# Cargando variables de entorno:
load_dotenv()
appport = getenv('PORT', 5000)
dburi = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
secret_key = getenv('SECRET_KEY')
setdebug = getenv('DEBUG', False)

# Inicializando la app de Flask:
app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = dburi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando las extensiones:
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importar las rutas desde routes.py
routes.init_routes(app)

# Ejecutar la Aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=setdebug, port=appport)
