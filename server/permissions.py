from functools import wraps
from flask import abort
from flask_login import current_user
from database.models import Permission, RolePermission

def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(permission_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Decoradores específicos para roles
def admin_required(f):
    return permission_required('admin_access')(f)

def editor_required(f):
    return permission_required('editor_access')(f)