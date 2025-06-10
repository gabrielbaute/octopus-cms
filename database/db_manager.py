from werkzeug.security import generate_password_hash
from typing import List, Union
from datetime import datetime

from database.db_config import db
from database.models import User, Post, Tag



class DatabaseManager:
    """Gestor de la base de datos para el blog"""
    def __init__(self):
        self.session = db.session

    @staticmethod
    def _commit_or_rollback():
        """Helper para manejar commit/rollback."""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return str(e)

    @classmethod
    def create_user(cls, username: str, email: str, password: str, role: str) -> Union[bool, str]:
        """Método para crear un nuevo usuario"""
        user = User(username, email, password, role)
        db.session.add(user)

        return cls._commit_or_rollback()

    @classmethod
    def set_new_password(cls, password: str, user_id: int) -> Union[bool, str]:
        """Método para cambiar contraseña de un usuario"""
        user = User.query.get(user_id)
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.commit()

        return cls._commit_or_rollback()

    @classmethod
    def get_post_for_edit(cls, post_id: int, user: User) -> Union[Post, str]:
        """Trae un post solo si el usuario tiene permisos."""
        post = Post.query.get_or_404(post_id)
        if post.user_id == user.id or user.role == "admin":
            return post
        return "Acceso denegado"

    @classmethod
    def get_user_posts(cls, user_id: int, include_deleted=False) -> List[Post]:
        """Obtiene todos los posts de un usuario."""
        query = Post.query.filter_by(user_id=user_id)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.all()

    @classmethod
    def save_new_post(
        cls, 
        title: str, 
        content: str, 
        user_id: int, 
        tag_ids: List[int],
        publish_date=datetime.utcnow()
    ) -> Union[bool, str]:
        """Método para guardar nuevos posts en la base de datos"""
        post = Post(title, content, user_id, publish_date)

        for tag_id in tag_ids.tags.data:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        
        db.session.add(post)
        return cls._commit_or_rollback()

    @classmethod
    def update_post(
        cls,
        post_id: int,
        title: str,
        content: str,
        tag_ids: List[int],
        user: User,  # Para verificar permisos
    ) -> Union[bool, str]:
        """Actualiza un post existente."""
        post = Post.query.get_or_404(post_id)
        
        # Verificación de permisos (podría estar en otro método)
        if post.user_id != user.id and user.role != "admin":
            return "No tienes permisos para editar este post"
        
        post.title = title
        post.content = content
        
        # Actualizar tags (forma eficiente)
        new_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.tags = new_tags  # Reemplaza todos los tags
        
        return cls._commit_or_rollback()
    
    @classmethod
    def delete_post(cls, post_id: int, user: User) -> Union[bool, str]:
        post = Post.query.get(post_id)
        if not post:
            return "Post no encontrado"
            
        if post.user_id != user.id and user.role != "admin":
            return "No tienes permisos"
            
        db.session.delete(post)
        return cls._commit_or_rollback()

    @classmethod
    def delete_posts(cls, post_ids: List[int], user: User):
        """Elimina permanentemente un post de la base de datos.

        Args:
            post_id: ID del post a eliminar
            user: Instancia del usuario que realiza la acción

        Returns:
            bool: True si la eliminación fue exitosa
            str: Mensaje de error en caso de fallo
        """
        if user.role != "admin":
            return "Se requiere rol de admin"
            
        Post.query.filter(Post.id.in_(post_ids)).delete()
        return cls._commit_or_rollback()

    @classmethod
    def soft_delete_post(cls, post_id: int, user: User) -> Union[bool, str]:
        post = Post.query.get(post_id)
        if not post:
            return "Post no encontrado"
            
        post.is_deleted = True
        post.deleted_at = datetime.utcnow()
        db.session.add(post)

        return cls._commit_or_rollback()