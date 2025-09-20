FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias primero (para optimizar cache)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación (.dockerignore se aplica aquí)
COPY . .

# Crear directorios necesarios para la aplicación
RUN mkdir -p uploads compressed && \
    chmod 755 uploads compressed

# Exponer puerto 5000 (Flask)
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando por defecto: aplicación Flask web (para Render)
CMD ["python", "app.py"]
