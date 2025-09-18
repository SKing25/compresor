// JavaScript para la aplicación de Compresor de Audio

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Mejorar la experiencia de subida de archivos
    setupFileUpload();
    
    // Auto-ocultar alertas después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

function setupFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        // Validar tamaño de archivo
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const maxSize = 100 * 1024 * 1024; // 100MB
            
            for (let i = 0; i < files.length; i++) {
                if (files[i].size > maxSize) {
                    alert(`El archivo ${files[i].name} es demasiado grande. Máximo permitido: 100MB`);
                    e.target.value = '';
                    return;
                }
                
                if (!files[i].name.toLowerCase().endsWith('.wav')) {
                    alert(`El archivo ${files[i].name} no es un archivo WAV válido.`);
                    e.target.value = '';
                    return;
                }
            }
            
            // Mostrar información del archivo seleccionado
            if (files.length === 1) {
                showFileInfo(files[0], input);
            }
        });
        
        // Drag and drop functionality
        const formGroup = input.closest('.mb-3');
        if (formGroup) {
            setupDragAndDrop(formGroup, input);
        }
    });
}

function showFileInfo(file, input) {
    const sizeKB = (file.size / 1024).toFixed(1);
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    
    // Crear o actualizar elemento de información
    let infoDiv = input.parentNode.querySelector('.file-info');
    if (!infoDiv) {
        infoDiv = document.createElement('div');
        infoDiv.className = 'file-info mt-2 p-2 bg-light rounded';
        input.parentNode.appendChild(infoDiv);
    }
    
    infoDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-file-audio text-primary me-2"></i>
            <div>
                <strong>${file.name}</strong><br>
                <small class="text-muted">Tamaño: ${sizeMB} MB</small>
            </div>
        </div>
    `;
}

function setupDragAndDrop(container, input) {
    container.addEventListener('dragover', function(e) {
        e.preventDefault();
        container.classList.add('dragover');
    });
    
    container.addEventListener('dragleave', function(e) {
        e.preventDefault();
        if (!container.contains(e.relatedTarget)) {
            container.classList.remove('dragover');
        }
    });
    
    container.addEventListener('drop', function(e) {
        e.preventDefault();
        container.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            // Validar archivos
            const validFiles = [];
            for (let i = 0; i < files.length; i++) {
                if (files[i].name.toLowerCase().endsWith('.wav')) {
                    validFiles.push(files[i]);
                }
            }
            
            if (validFiles.length > 0) {
                // Crear un nuevo FileList
                const dt = new DataTransfer();
                validFiles.forEach(file => dt.items.add(file));
                input.files = dt.files;
                
                // Disparar evento change
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            } else {
                alert('Solo se permiten archivos WAV');
            }
        }
    });
}

// Función para mostrar notificaciones toast
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remover el toast del DOM después de que se oculte
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Función para formatear bytes
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Función para descargar múltiples archivos
function downloadAll(urls, filenames) {
    if (!urls || urls.length === 0) return;
    
    urls.forEach((url, index) => {
        setTimeout(() => {
            const link = document.createElement('a');
            link.href = url;
            link.download = filenames ? filenames[index] : '';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }, index * 1000); // Retraso de 1 segundo entre descargas
    });
}

// Función para limpiar archivos temporales
function cleanupFiles() {
    fetch('/cleanup')
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                showToast(data.message, 'success');
            } else {
                showToast(data.error, 'danger');
            }
        })
        .catch(error => {
            showToast('Error al limpiar archivos', 'danger');
        });
}

// Función para copiar al portapapeles
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Enlace copiado al portapapeles', 'success');
        });
    } else {
        // Fallback para navegadores más antiguos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Enlace copiado al portapapeles', 'success');
    }
}
