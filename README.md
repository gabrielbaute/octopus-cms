# Octopus CMS v0.3.0 Beta
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)
![Docker](https://img.shields.io/badge/Container-Docker-blue.svg)
![Bulma](https://img.shields.io/badge/CSS%20Framework-Bulma-00D1B2.svg)
![Status](https://img.shields.io/badge/Status-En%20desarrollo-yellow.svg)
## Descripción

Este proyecto de CMS, desarrollado con **Flask** como backend en Python y **Bulma** como framework CSS, nuestro objetivo es ofrecer una experiencia de usuario robusta y funcional. El proyecto incorpora una variedad de características avanzadas y se centrará en ofrecer un CMS completo y funcional pero con un look & feel totalmente minimalista.

### Características Principales

- **Operaciones CRUD**: Capacidad completa para Crear, Leer, Actualizar y Eliminar posts del blog.
- **Gestión de Usuarios**: Sistema de usuarios y roles semejante a wordpress.
- **Edición en Markdown**: Los posts pueden ser editados utilizando Markdown, mejorando la flexibilidad y control sobre el contenido.
- **Programación de Publicaciones**: Los posts pueden ser programados para publicarse en una fecha y hora futura.
- **Newsletter**: Envío de correos masivos a suscriptores utilizando servicios SMTP de Gmail, Outlook, o cualquier otro proveedor. La configuración del correo se maneja a través de variables de entorno.
- **Suscripción a Newsletter**: Los usuarios pueden suscribirse para recibir actualizaciones y newsletters. Los correos sólo se envían a los usuarios que hayan confirmado su suscripción previamente, algo que se hace mediante un token enviado al correo del ususario y que expira a las 24 horas.
- **Sistema de Roles**: Implementación de roles de usuario para autor y administrador, manejando permisos y acceso a funcionalidades.
- **Interfaz con Bulma**: Utilización de Bulma para un diseño limpio y responsivo, garantizando una buena experiencia de usuario.
- **Dark y Light theme**: Los usuarios y lectores pueden seleccionar el theme para explorar o emplear el Site.
- **Deploy en docker**: De momento, el proyecto puede desplegarse usando contenedores docker y empleando Waitress como WSGI en producción.

### Enfoque en Python

El proyecto está completamente centrado en Python, utilizando Flask como framework para el backend. Esta elección permite una rápida y eficiente creación de aplicaciones web, aprovechando las capacidades y simplicidad de Python. El desarrollo sigue una lógica modular y el objetivo es permitir en un futuro la incorporación de más módulos sin afectar en gran medida el código principal.

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/gabrielbaute/octopus-cms.git
   cd octopus-cms
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
    SECRET_KEY='alguna_clave_muy_segura'
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
    python run.py
    ```
    Ten en cuenta que si vas a trabajar en producción, debes pasar `DEBUG=True` en las variables de entorno. Esto cambiará el servidor del servidor de pruebas de Flask al servidor WSGI de Waitress. No es recomendable emplear el servidor de Flask en producción ni el modo DEBUG.

2. Abrir el navegador y navegar a `http://localhost:5000` (o el puerto que hayas designado en las variables de entorno) para ver la aplicación en funcionamiento.

## Contribuciones
Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request. Este proyecto se encuentra en desarrollo activo, y se planea incorporar más funcionalidades en el futuro. ¡Todas las ideas y aportes son bienvenidos!

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
