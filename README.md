# Compresor de Audio WAV a MP3

Una aplicación Flask para comprimir archivos de audio WAV a MP3 con diferentes niveles de calidad. También incluye una herramienta de línea de comandos para uso directo.

## 🚀 Características

- **Aplicación Web**: Interfaz web intuitiva para subir y comprimir archivos
- **Línea de Comandos**: Herramienta CLI para compresión por lotes
- **Múltiples Calidades**: Diferentes bitrates (64k, 128k, 192k, 256k, 320k)
- **Niveles de Calidad**: Presets de calidad (baja, media, alta)
- **Docker Support**: Contenedor Docker para despliegue fácil

## 📋 Requisitos del Sistema

### Dependencias Principales
- Python 3.12 (recomendado) o 3.11
- FFmpeg (para conversión de audio)

### Sistemas Operativos Soportados
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu, Debian, CentOS, etc.)

## 🛠️ Instalación

### Opción 1: Instalación Local

#### Windows

1. **Instalar Python 3.12**:
   - Descarga desde [python.org](https://www.python.org/downloads/)
   - Durante la instalación, marca "Add Python to PATH"

2. **Instalar FFmpeg**:
   ```cmd
   # Usando chocolatey (recomendado)
   choco install ffmpeg
   
   # O descarga manual desde https://ffmpeg.org/download.html
   ```

3. **Clonar el repositorio**:
   ```cmd
   git clone https://github.com/SKing25/compresor.git
   cd compresor
   ```

4. **Crear entorno virtual**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Instalar dependencias**:
   ```cmd
   pip install -r requirements.txt
   ```

#### macOS

1. **Instalar Python 3.12**:
   ```bash
   # Usando Homebrew (recomendado)
   brew install python@3.12
   
   # O descarga desde python.org
   ```

2. **Instalar FFmpeg**:
   ```bash
   brew install ffmpeg
   ```

3. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/SKing25/compresor.git
   cd compresor
   ```

4. **Crear entorno virtual**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

5. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

#### Linux (Ubuntu/Debian)

1. **Instalar Python 3.12 y FFmpeg**:
   ```bash
   sudo apt update
   sudo apt install python3.12 python3.12-venv python3-pip ffmpeg
   ```

2. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/SKing25/compresor.git
   cd compresor
   ```

3. **Crear entorno virtual**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

#### Linux (CentOS/RHEL)

1. **Instalar Python 3.12 y FFmpeg**:
   ```bash
   sudo dnf install python3.12 python3-pip
   sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
   sudo dnf install ffmpeg
   ```

2. **Seguir pasos 2-4 como en Ubuntu**

### Opción 2: Docker (Recomendado para Producción)

#### Requisitos
- Docker instalado en tu sistema

#### Todos los Sistemas Operativos

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/SKing25/compresor.git
   cd compresor
   ```

2. **Construir la imagen Docker**:
   ```bash
   docker build -t compresor-audio .
   ```

3. **Ejecutar el contenedor**:
   ```bash
   docker run -p 5000:5000 compresor-audio
   ```

## 🎯 Uso

### Aplicación Web Flask

#### Desarrollo Local
```bash
# Activar entorno virtual (si no está activado)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

#### Producción
```bash
# Usando Gunicorn (incluido en requirements.txt)
gunicorn --bind 0.0.0.0:5000 app:app
```

### Herramienta de Línea de Comandos

#### Comprimir un archivo individual
```bash
# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Comprimir archivo con calidad media (192k)
python compresor.py archivo.wav

# Comprimir con bitrate específico
python compresor.py archivo.wav -b 320k

# Comprimir con preset de calidad
python compresor.py archivo.wav -q high

# Especificar archivo de salida
python compresor.py archivo.wav -o compressed_file.mp3
```

#### Comprimir múltiples archivos
```bash
# Comprimir todos los WAV de una carpeta
python compresor.py -f /path/to/folder

# Comprimir a carpeta específica
python compresor.py -f /path/to/folder -o /path/to/output
```

#### Opciones Disponibles
```bash
python compresor.py -h
```

**Parámetros:**
- `-i, --input`: Archivo WAV de entrada
- `-f, --folder`: Carpeta con archivos WAV
- `-o, --output`: Archivo o carpeta de salida
- `-b, --bitrate`: Bitrate (64k, 128k, 192k, 256k, 320k)
- `-q, --quality`: Calidad (low, medium, high)

## 📁 Estructura del Proyecto

```
compresor-audio/
├── app.py                 # Aplicación Flask principal
├── compresor.py          # Herramienta CLI de compresión
├── requirements.txt      # Dependencias Python
├── Dockerfile           # Configuración Docker
├── .dockerignore       # Archivos excluidos de Docker
├── static/             # Archivos estáticos (CSS, JS)
│   ├── css/
│   └── js/
├── templates/          # Plantillas HTML
├── uploads/           # Archivos subidos (temporal)
└── compressed/       # Archivos comprimidos (temporal)
```

## 🐳 Despliegue

### Render.com
1. Conecta tu repositorio de GitHub
2. Render detectará automáticamente el `Dockerfile`
3. La aplicación se desplegará usando Python 3.12 y FFmpeg

### Heroku
```bash
# Instalar Heroku CLI y hacer login
heroku create tu-app-name
git push heroku main
```

### Docker Compose (Opcional)
```yaml
version: '3.8'
services:
  compresor:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./compressed:/app/compressed
```

## 🔧 Solución de Problemas

### Error: "FFmpeg not found"
- **Windows**: Instala FFmpeg usando Chocolatey o descarga manual
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)

### Error: "Module 'audioop' not found"
- Usa Python 3.12 o inferior (Python 3.13 eliminó audioop)
- Con Docker esto se resuelve automáticamente

### Error: "Permission denied"
- **Linux/macOS**: Asegúrate de tener permisos de escritura en las carpetas
- Ejecuta: `chmod 755 uploads compressed`

### Problemas de Memoria
- Para archivos grandes (>100MB), aumenta la memoria disponible
- Considera procesar archivos en lotes más pequeños

## 📝 Ejemplos de Uso

### Ejemplo 1: Comprimir para Podcast
```bash
python compresor.py mi_podcast.wav -b 128k -o podcast_compressed.mp3
```

### Ejemplo 2: Comprimir Música de Alta Calidad
```bash
python compresor.py mi_cancion.wav -q high -o musica/
```

### Ejemplo 3: Procesar Carpeta Completa
```bash
python compresor.py -f ./audio_raw -o ./audio_compressed -b 192k
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras problemas:

1. Revisa la sección de "Solución de Problemas"
2. Busca en los [Issues existentes](https://github.com/SKing25/compresor/issues)
3. Crea un nuevo Issue con detalles del problema

## 🔄 Changelog

### v1.0.0
- Aplicación Flask con interfaz web
- Herramienta CLI para compresión
- Soporte Docker
- Múltiples formatos de calidad
- Documentación completa
