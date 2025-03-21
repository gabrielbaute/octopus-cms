# Usar una imagen base de Python 3.13
FROM python:3.13-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Crear la carpeta instance para la base de datos SQLite
RUN mkdir -p instance

# Exponer el puerto en el que corre la aplicación
EXPOSE ${PORT:-5000}

# Comando para correr la aplicación usando waitress
CMD ["python", "run.py"]