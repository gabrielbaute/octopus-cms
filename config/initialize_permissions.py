from flask import current_app
from database.db_config import db
from database.models import Permission, RolePermission
from config.permissions_system import BASE_PERMISSIONS, ROLE_PERMISSIONS_MAP

def initialize_permissions_system():
    """Inicializa completamente el sistema de permisos"""
    try:
        if not is_system_initialized():
            _create_base_permissions()
            _assign_role_permissions()
            current_app.logger.info("Sistema de permisos inicializado correctamente")
            return True
        current_app.logger.info("El sistema de permisos ya estaba inicializado")
        return False
    except Exception as e:
        current_app.logger.error(f"Error inicializando permisos: {str(e)}")
        db.session.rollback()
        raise

def _create_base_permissions():
    """Crea los permisos base en la base de datos"""
    if Permission.query.count() == 0:
        permissions = [Permission(**p) for p in BASE_PERMISSIONS]
        db.session.bulk_save_objects(permissions)
        db.session.commit()

def _assign_role_permissions():
    """Asigna permisos a los roles según el mapeo definido"""
    # Verificar que todos los permisos referenciados existan
    existing_perms = {p.name for p in Permission.query.all()}
    for perm_name in set().union(*ROLE_PERMISSIONS_MAP.values()):
        if perm_name not in existing_perms:
            raise ValueError(f"Permiso {perm_name} no existe en la base de datos")
    
    # Procede a asignar los permisos
    if RolePermission.query.count() == 0:
        role_permissions = []
        for role, permissions in ROLE_PERMISSIONS_MAP.items():
            for perm_name in permissions:
                if perm := Permission.query.filter_by(name=perm_name).first():
                    role_permissions.append(
                        RolePermission(role=role, permission_id=perm.id))
        
        db.session.bulk_save_objects(role_permissions)
        db.session.commit()

def is_system_initialized():
    """Verifica si el sistema de permisos ya fue inicializado"""
    return Permission.query.count() > 0 and RolePermission.query.count() > 0