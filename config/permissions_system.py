"""
Sistema de permisos para los roles de usuario.
"""

BASE_PERMISSIONS = [
    # ======================
    # CONTENIDO (POSTS}
    # ======================
    {'name':'create_posts', 'description':'Crear nuevos artículos', 'category':'content'},
    {'name':'edit_own_posts', 'description':'Editar sus propios artículos', 'category':'content'},
    {'name':'edit_others_posts', 'description':'Editar artículos de otros usuarios', 'category':'content'},
    {'name':'publish_posts', 'description':'Publicar artículos', 'category':'content'},
    {'name':'delete_own_posts', 'description':'Eliminar sus propios artículos', 'category':'content'},
    {'name':'delete_others_posts', 'description':'Eliminar artículos de otros usuarios', 'category':'content'},
    {'name':'read_private_posts', 'description':'Leer artículos privados', 'category':'content'},
    
    # ======================
    # PÁGINAS
    # ======================
    {'name':'create_pages', 'description':'Crear nuevas páginas', 'category':'pages'},
    {'name':'edit_pages', 'description':'Editar páginas', 'category':'pages'},
    {'name':'publish_pages', 'description':'Publicar páginas', 'category':'pages'},
    {'name':'delete_pages', 'description':'Eliminar páginas', 'category':'pages'},
    {'name':'read_private_pages', 'description':'Leer páginas privadas', 'category':'pages'},
    
    # ======================
    # MEDIA
    # ======================
    {'name':'upload_files', 'description':'Subir archivos al media library', 'category':'media'},
    {'name':'edit_media', 'description':'Editar archivos multimedia', 'category':'media'},
    {'name':'delete_media', 'description':'Eliminar archivos multimedia', 'category':'media'},
    
    # ======================
    # COMENTARIOS
    # ======================
    {'name':'moderate_comments', 'description':'Moderar comentarios', 'category':'comments'},
    {'name':'edit_comments', 'description':'Editar comentarios', 'category':'comments'},
    {'name':'delete_comments', 'description':'Eliminar comentarios', 'category':'comments'},
    
    # ======================
    # USUARIOS
    # ======================
    {'name':'list_users', 'description':'Ver lista de usuarios', 'category':'users'},
    {'name':'create_users', 'description':'Crear nuevos usuarios', 'category':'users'},
    {'name':'edit_users', 'description':'Editar usuarios existentes', 'category':'users'},
    {'name':'delete_users', 'description':'Eliminar usuarios', 'category':'users'},
    {'name':'promote_users', 'description':'Cambiar roles de usuarios', 'category':'users'},
    
    # ======================
    # AJUSTES
    # ======================
    {'name':'manage_options', 'description':'Gestionar ajustes generales', 'category':'settings'},
    {'name':'edit_theme_options', 'description':'Modificar opciones del tema', 'category':'settings'},
    {'name':'manage_categories', 'description':'Gestionar categorías', 'category':'settings'},
    {'name':'manage_tags', 'description':'Gestionar etiquetas', 'category':'settings'},
    
    # ======================
    # APARIENCIA
    # ======================
    {'name':'switch_themes', 'description':'Cambiar tema activo', 'category':'appearance'},
    {'name':'edit_theme', 'description':'Editar código del tema', 'category':'appearance'},
    {'name':'edit_widgets', 'description':'Gestionar widgets', 'category':'appearance'},
    {'name':'edit_menus', 'description':'Gestionar menús de navegación', 'category':'appearance'},
    
    # ======================
    # PLUGINS
    # ======================
    {'name':'install_plugins', 'description':'Instalar nuevos plugins', 'category':'plugins'},
    {'name':'activate_plugins', 'description':'Activar/desactivar plugins', 'category':'plugins'},
    {'name':'edit_plugins', 'description':'Editar código de plugins', 'category':'plugins'},
    {'name':'delete_plugins', 'description':'Eliminar plugins', 'category':'plugins'},
    
    # ======================
    # HERRAMIENTAS
    # ======================
    {'name':'import_content', 'description':'Importar contenido', 'category':'tools'},
    {'name':'export_content', 'description':'Exportar contenido', 'category':'tools'},
    {'name':'manage_backups', 'description':'Gestionar copias de seguridad', 'category':'tools'},
    
    # ======================
    # COMERCE (si aplica}
    # ======================
    {'name':'manage_products', 'description':'Gestionar productos', 'category':'commerce'},
    {'name':'manage_orders', 'description':'Gestionar pedidos', 'category':'commerce'},
    {'name':'view_reports', 'description':'Ver reportes de ventas', 'category':'commerce'},
]

ALL_PERMISSION_NAMES = [p['name'] for p in BASE_PERMISSIONS]

ROLE_PERMISSIONS_MAP = {
        'super_admin': ALL_PERMISSION_NAMES,
        'admin': [
            'create_posts', 'edit_own_posts', 'edit_others_posts', 'publish_posts',
            'delete_own_posts', 'delete_others_posts', 'read_private_posts',
            'create_pages', 'edit_pages', 'publish_pages', 'delete_pages',
            'upload_files', 'edit_media', 'delete_media',
            'moderate_comments', 'edit_comments', 'delete_comments',
            'list_users', 'create_users', 'edit_users', 'delete_users', 'promote_users',
            'manage_categories', 'manage_tags'
        ],
        'editor': [
            'create_posts', 'edit_own_posts', 'edit_others_posts', 'publish_posts',
            'delete_own_posts', 'delete_others_posts', 'read_private_posts',
            'edit_pages', 'upload_files',
            'moderate_comments', 'edit_comments', 'delete_comments'
        ],
        'author': [
            'create_posts', 'edit_own_posts', 'publish_posts', 'delete_own_posts',
            'upload_files'
        ],
        'contributor': [
            'create_posts', 'edit_own_posts'
        ],
        'subscriber': []
    }

# Jerarquía de permisos por rol
class PermissionHierarchy:
    """Clase que define la jerarquía de permisos por rol."""
    
    SUPER_ADMIN_PERMISSIONS = ROLE_PERMISSIONS_MAP['super_admin']
    ADMIN_PERMISSIONS = ROLE_PERMISSIONS_MAP['admin']
    EDITOR_PERMISSIONS = ROLE_PERMISSIONS_MAP['editor']
    AUTHOR_PERMISSIONS = ROLE_PERMISSIONS_MAP['author']
    CONTRIBUTOR_PERMISSIONS = ROLE_PERMISSIONS_MAP['contributor']
    SUBSCRIBER_PERMISSIONS = ROLE_PERMISSIONS_MAP['subscriber']



