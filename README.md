# Blog en Flask

## Descripción

Este proyecto de blog, desarrollado con **Flask** como backend en Python y **Bulma** como framework CSS, está diseñado para ofrecer una experiencia de usuario robusta y funcional. El proyecto incorpora una variedad de características avanzadas y se centra en la gestión eficiente de contenido y usuarios.

### Características Principales

- **Operaciones CRUD**: Capacidad completa para Crear, Leer, Actualizar y Eliminar posts del blog.
- **Gestión de Usuarios**: Dos niveles de usuario, `author` y `admin`, cada uno con permisos específicos.
- **Edición en Markdown**: Los posts pueden ser editados utilizando Markdown, mejorando la flexibilidad y control sobre el contenido.
- **Programación de Publicaciones**: Los posts pueden ser programados para publicarse en una fecha y hora futura.
- **Newsletter**: Envío de correos masivos a suscriptores utilizando servicios SMTP de Gmail, Outlook, o cualquier otro proveedor. La configuración del correo se maneja a través de variables de entorno.
- **Suscripción a Newsletter**: Los usuarios pueden suscribirse para recibir actualizaciones y newsletters.
- **Sistema de Roles**: Implementación de roles de usuario para autor y administrador, manejando permisos y acceso a funcionalidades.
- **Interfaz con Bulma**: Utilización de Bulma para un diseño limpio y responsivo, garantizando una buena experiencia de usuario.

### Enfoque en Python

El proyecto está completamente centrado en Python, utilizando Flask como framework para el backend. Esta elección permite una rápida y eficiente creación de aplicaciones web, aprovechando las capacidades y simplicidad de Python.

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/tu-usuario/blog-project.git
   cd blog-project
   ```

2. Crear un entorno virtual y activar:
    ```sh
    python -m venv env
    source env/bin/activate # En Windows usa `env\Scripts\activate`
    ```

3. Instalar las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configurar las variables de entorno: Crea un archivo `.env` en la raíz del proyecto y añade las siguientes configuraciones:
    ```plaintext
    SECRET_KEY='tu_secreto'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    SMTP_SERVER='smtp.gmail.com'
    SMTP_PORT=587
    EMAIL='tu_email@gmail.com'
    APP_PASS='tu_password_app'
    FROM='Blog <tu_email@gmail.com>'
    ```
    El proyecto también incluye un archivo example.env en donde encontrará otras variables de entorno para configurar.

5. Inicializar la base de datos:
    ```sh
    flask db init
    flask db migrate -m "Inicializar base de datos"
    flask db upgrade
    ```

## Uso
1. Ejecutar la aplicación:
    ```sh
    flask run
    ```

2. Abrir el navegador y navegar a `http://localhost:5000` para ver la aplicación en funcionamiento.

## Contribuciones
Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request. Este proyecto se encuentra en desarrollo activo, y se planea incorporar más funcionalidades en el futuro. ¡Todas las ideas y aportes son bienvenidos!

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
