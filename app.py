#!/usr/bin/env python3
"""
Aplicación Web Flask para Compresor de Audio WAV a MP3
"""

import os
import shutil
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from compresor import AudioCompressor
import tempfile
import uuid

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar en producción

# Configuración
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
ALLOWED_EXTENSIONS = {'wav'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB máximo

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Crear carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Maneja la subida y compresión de archivos"""
    try:
        # Verificar si se envió un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Solo se permiten archivos WAV'}), 400
        
        # Obtener parámetros de compresión
        bitrate = request.form.get('bitrate', '128k')
        quality = request.form.get('quality', 'medium')
        
        # Generar nombres únicos para los archivos
        unique_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        input_filename = f"{unique_id}_{original_filename}"
        output_filename = f"{unique_id}_{os.path.splitext(original_filename)[0]}.mp3"
        
        # Rutas completas
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)
        
        # Guardar archivo subido
        file.save(input_path)
        
        # Comprimir archivo
        compressor = AudioCompressor()
        success = compressor.compress_to_mp3(input_path, output_path, bitrate, quality)
        
        if success:
            # Obtener información de los archivos
            original_size = os.path.getsize(input_path) / (1024 * 1024)
            compressed_size = os.path.getsize(output_path) / (1024 * 1024)
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
            
            # Limpiar archivo original
            os.remove(input_path)
            
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', filename=output_filename),
                'original_size': round(original_size, 2),
                'compressed_size': round(compressed_size, 2),
                'compression_ratio': round(compression_ratio, 1),
                'filename': output_filename
            })
        else:
            # Limpiar archivos en caso de error
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({'error': 'Error durante la compresión'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Descarga el archivo comprimido"""
    try:
        file_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('Archivo no encontrado', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error al descargar: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/batch')
def batch_upload():
    """Página para subida múltiple"""
    return render_template('batch.html')

@app.route('/batch_upload', methods=['POST'])
def batch_upload_files():
    """Maneja la subida y compresión de múltiples archivos"""
    try:
        files = request.files.getlist('files')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No se seleccionaron archivos'}), 400
        
        # Obtener parámetros de compresión
        bitrate = request.form.get('bitrate', '128k')
        quality = request.form.get('quality', 'medium')
        
        results = []
        compressor = AudioCompressor()
        
        for file in files:
            if file.filename == '' or not allowed_file(file.filename):
                continue
                
            try:
                # Generar nombres únicos
                unique_id = str(uuid.uuid4())
                original_filename = secure_filename(file.filename)
                input_filename = f"{unique_id}_{original_filename}"
                output_filename = f"{unique_id}_{os.path.splitext(original_filename)[0]}.mp3"
                
                # Rutas completas
                input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
                output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)
                
                # Guardar y comprimir
                file.save(input_path)
                success = compressor.compress_to_mp3(input_path, output_path, bitrate, quality)
                
                if success:
                    original_size = os.path.getsize(input_path) / (1024 * 1024)
                    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                    compression_ratio = ((original_size - compressed_size) / original_size) * 100
                    
                    results.append({
                        'filename': original_filename,
                        'success': True,
                        'download_url': url_for('download_file', filename=output_filename),
                        'original_size': round(original_size, 2),
                        'compressed_size': round(compressed_size, 2),
                        'compression_ratio': round(compression_ratio, 1)
                    })
                else:
                    results.append({
                        'filename': original_filename,
                        'success': False,
                        'error': 'Error durante la compresión'
                    })
                
                # Limpiar archivo original
                if os.path.exists(input_path):
                    os.remove(input_path)
                    
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@app.route('/cleanup')
def cleanup_files():
    """Limpia archivos temporales antiguos"""
    try:
        # Limpiar archivos de más de 1 hora
        import time
        current_time = time.time()
        
        for folder in [app.config['UPLOAD_FOLDER'], app.config['COMPRESSED_FOLDER']]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > 3600:  # 1 hora
                        os.remove(file_path)
        
        return jsonify({'message': 'Archivos limpiados correctamente'})
    except Exception as e:
        return jsonify({'error': f'Error al limpiar archivos: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
