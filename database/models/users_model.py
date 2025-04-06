from datetime import datetime
from flask_login import UserMixin
from database.db_config import db
from config.permissions_system import PermissionHierarchy

role = PermissionHierarchy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    # Roles disponibles (constantes)
    ROLES = {
        'super_admin': 'Super Admin',
        'admin': 'Administrator',
        'editor': 'Editor',
        'author': 'Author',
        'contributor': 'Contributor',
        'subscriber': 'Subscriber'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='subscriber')
    is_active = db.Column(db.Boolean, default=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Validación de roles
    
    def has_role(self, role_name):
        """Verifica si el usuario tiene un rol específico"""
        return self.role == role_name
    
    def is_super_admin(self):
        return self.has_role('super_admin')
    
    def is_admin(self):
        return self.is_super_admin() or self.has_role('admin')
    
    def is_editor(self):
        return self.is_admin() or self.has_role('editor')
    
    def is_author(self):
        return self.is_editor() or self.has_role('author')
    
    def is_contributor(self):
        return self.is_author() or self.has_role('contributor')
    
    def is_subscriber(self):
        return True  # Todos los usuarios son al menos subscribers
    
    # Proteger súper admin de eliminación y cambio de rol
    @staticmethod
    def prevent_super_admin_deletion(mapper, connection, target):
        if target.role == 'super_admin':
            raise ValueError("No se puede eliminar un Super Admin")

    @staticmethod
    def prevent_super_admin_role_change(mapper, connection, target):
        original = db.session.get(User, target.id)
        if original and original.role == 'super_admin' and target.role != 'super_admin':
            raise ValueError("No se puede cambiar el rol de Super Admin")

    
    def has_permission(self, permission_name):
        """Verifica si el usuario tiene un permiso directo o por jerarquía"""
        # Super Admin tiene todos los permisos
        if self.role == 'super_admin':
            return True
            
        # Administradores heredan permisos de editores
        if self.role == 'admin' and permission_name in role.EDITOR_PERMISSIONS:
            return True
            
        # Editores heredan permisos de autores
        if self.role == 'editor' and permission_name in role.AUTHOR_PERMISSIONS:
            return True
        
        # Autores heredan permisos de contribuyentes
        if self.role == 'author' and permission_name in role.CONTRIBUTOR_PERMISSIONS:
            return True
        # Contribuyentes heredan permisos de suscriptores
        if self.role == 'contributor' and permission_name in role.SUBSCRIBER_PERMISSIONS:
            return True
        
        # Verificar permiso directo
        permission = Permission.query.filter_by(name=permission_name).first()
        if not permission:
            return False
            
        return RolePermission.query.filter_by(
            role=self.role,
            permission_id=permission.id
        ).first() is not None
        
class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    category = db.Column(db.String(50))

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False) 
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    
    # Relación
    permission = db.relationship('Permission', backref='role_assignments')