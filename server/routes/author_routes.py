from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import current_user, login_required
from datetime import datetime

from server.forms import NewPostForm, EditPostForm, PostTagsForm, TagForm
from database import db
from database.models import Post, Tag
from mail import send_newsletter_mail
from server.permissions import permission_required


author_bp = Blueprint('author', __name__, template_folder='templates')

# Rutas de gestión de posts
@author_bp.route('/new-post', methods=['GET', 'POST'])
@login_required
@permission_required('author')
def new_post():
    post_form = NewPostForm()
    tags_form = PostTagsForm()
    
    if post_form.validate_on_submit():
        publish_date = post_form.publish_date.data if post_form.publish_date.data else datetime.utcnow()
        post = Post(
            title=post_form.title.data, 
            content=post_form.content.data, 
            user_id=current_user.id, 
            publish_date=publish_date
        )
        
        # Añadir tags seleccionados
        for tag_id in tags_form.tags.data:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()

        current_app.logger.info(f"Nueva entrada publicada por {current_user.email}")
        flash('Tu post ha sido creado!', 'success')
        send_newsletter_mail(post)
        
        return redirect(url_for('main.blog'))
    
    return render_template('main/new_post.html', 
                         title='Nuevo Post', 
                         post_form=post_form, 
                         tags_form=tags_form)

@author_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@permission_required('author')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Verificar permisos
    if post.user_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    post_form = EditPostForm()
    tags_form = PostTagsForm()
    
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data
        
        # Actualizar tags
        post.tags = []
        for tag_id in tags_form.tags.data:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        
        db.session.commit()
        current_app.logger.info(f"Post editado. Autor: {current_user.email}, Post: {post.title}")
        flash('Tu post ha sido actualizado!', 'success')
        return redirect(url_for('main.blog'))
    
    elif request.method == 'GET':
        post_form.title.data = post.title
        post_form.content.data = post.content
        tags_form.tags.data = [tag.id for tag in post.tags]
    
    return render_template('main/edit_post.html', 
                         title='Editar Post', 
                         post_form=post_form, 
                         tags_form=tags_form,
                         post=post)

# Nueva ruta para gestión de tags
@author_bp.route('/manage-tags', methods=['GET', 'POST'])
@login_required
@permission_required('editor')  # Solo editores y admins pueden gestionar tags
def manage_tags():
    form = TagForm()
    
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash(f'Tag "{tag.name}" creado exitosamente!', 'success')
        return redirect(url_for('author.manage_tags'))
    
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('main/manage_tags.html', 
                         title='Gestionar Tags', 
                         form=form, 
                         tags=tags)

@author_bp.route('/delete-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@permission_required('author')
def delete_post(post_id):
    # Obtener el post o devolver un error 404 si no existe
    post = Post.query.get_or_404(post_id)
     
    # Verificar si el usuario actual es el autor del post o un administrador
    if post.user_id != current_user.id and current_user.role != 'admin':
        abort(403)  # Forbidden
    
    # Guardar el título del post para el log
    post_name = post.title
    
    # Eliminar el post de la base de datos
    db.session.delete(post)
    db.session.commit()

    # Registrar la acción en el log
    current_app.logger.warning(f"Se ha borrado un post. Titulo: {post_name}, borrado por {current_user.email}")
    
    # Mostrar un mensaje flash al usuario
    flash('Your post has been deleted!', 'success')

    # Redirigir al blog
    return redirect(url_for('main.blog'))
