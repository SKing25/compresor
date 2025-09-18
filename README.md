# Compresor de Audio WAV a MP3

Una aplicación Flask para comprimir archivos de audio WAV a MP3 con diferentes niveles de calidad. También incluye una herramienta de línea de comandos para uso directo.

## Características

- **Aplicación Web**: Interfaz web intuitiva para subir y comprimir archivos
- **Múltiples Calidades**: Diferentes bitrates (64k, 128k, 192k, 256k, 320k)
- **Niveles de Calidad**: Presets de calidad (baja, media, alta)
- **Docker Support**: Contenedor Docker para despliegue fácil

## Acceso Rápido

Si no quieres instalar la aplicación localmente, puedes acceder directamente a la versión desplegada:

**[https://compresor-alfy.onrender.com/](https://compresor-alfy.onrender.com/)**

> **Nota**: A veces cuando accedas al enlace puede tardar unos minutos en cargar mientras Render reactiva la aplicación. Esto es normal en el plan gratuito de Render.

---

## Requisitos del Sistema

### Dependencias Principales
- Python 3.12 (recomendado) o 3.11
- FFmpeg (para conversión de audio)

### Sistemas Operativos Soportados
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu, Debian, CentOS, etc.)

## Instalación

En caso de no tener python 3.12 o anterior, usar la [Opcion 2](#opción-2-docker) (por medio de Docker), de lo contrario usa la [Opcion 1](#opción-1-instalación-local)

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

#### Ejecución Local

```bash
# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Opción 2: Docker

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

La aplicación estará disponible en: `http://localhost:5000`