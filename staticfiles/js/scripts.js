function soloLetras(e) {
    e.value = e.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ ]/g, '');
}

function soloNumeros(e) {
    e.value = e.value.replace(/[^0-9]/g, '');
}

function validarTecnica() {
    let grado = document.querySelector('[name="grado"]').value;
    let tecnica = document.querySelector('[name="tecnica"]');
    let paraleloTecnico = document.querySelector('[name="paralelo_tecnico"]');
    if (grado === "1ero Bach" || grado === "2do Bach" || grado === "3ro Bach") {
        tecnica.required = true;
        paraleloTecnico.required = true;
        tecnica.disabled = false;
        paraleloTecnico.disabled = false;
    } else {
        tecnica.required = false;
        paraleloTecnico.required = false;
        tecnica.value = "";
        paraleloTecnico.value = "";
        tecnica.disabled = true;
        paraleloTecnico.disabled = true;
    }
}

setTimeout(() => {
    const popup = document.getElementById("popup");
    if(popup){
        popup.style.display = "none";
    }
}, 3000);

function updateProgress() {
    const form = document.getElementById('requestForm');
    const inputs = form.querySelectorAll('input[required], select[required]:not(:disabled), textarea[required]');
    let filled = 0;
    inputs.forEach(input => {
        if (input.value.trim() !== "") filled++;
    });
    const percentage = (filled / inputs.length) * 100;
    document.getElementById('progressBar').style.width = percentage + "%";
}

// Función para filtrar solicitudes activas
function filtrarSolicitudes() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase().trim();
    const tablas = document.querySelectorAll('.tabla-box');
    const tbody = tablas[0].querySelector('tbody');
    const filas = tbody.querySelectorAll('tr');
    let filasVisibles = 0;

    filas.forEach(fila => {
        if (fila.id === 'sinResultadosActivas') {
            return;
        }
        
        const contenido = fila.textContent.toLowerCase();
        
        if (searchInput === '' || contenido.includes(searchInput)) {
            fila.style.display = '';
            filasVisibles++;
        } else {
            fila.style.display = 'none';
        }
    });

    const mensajeSinResultados = document.getElementById('sinResultadosActivas');
    if (searchInput !== '' && filasVisibles === 0) {
        mensajeSinResultados.style.display = '';
    } else {
        mensajeSinResultados.style.display = 'none';
    }
}

// Función para filtrar solicitudes finalizadas
function filtrarFinalizadas() {
    const searchInput = document.getElementById('searchFinalizadas').value.toLowerCase().trim();
    const tablas = document.querySelectorAll('.tabla-box');
    const tbody = tablas[1].querySelector('tbody');
    const filas = tbody.querySelectorAll('tr');
    let filasVisibles = 0;

    filas.forEach(fila => {
        if (fila.id === 'sinResultadosFinalizadas') {
            return;
        }
        
        const contenido = fila.textContent.toLowerCase();
        
        if (searchInput === '' || contenido.includes(searchInput)) {
            fila.style.display = '';
            filasVisibles++;
        } else {
            fila.style.display = 'none';
        }
    });

    const mensajeSinResultados = document.getElementById('sinResultadosFinalizadas');
    if (searchInput !== '' && filasVisibles === 0) {
        mensajeSinResultados.style.display = '';
    } else {
        mensajeSinResultados.style.display = 'none';
    }
}

// Función para limpiar búsqueda de solicitudes activas
function limpiarBusqueda() {
    document.getElementById('searchInput').value = '';
    filtrarSolicitudes();
}

// Función para limpiar búsqueda de solicitudes finalizadas
function limpiarBusquedaFinalizadas() {
    document.getElementById('searchFinalizadas').value = '';
    filtrarFinalizadas();
}

// Funciones para modal logout
function abrirModalLogout() {
    document.getElementById('modalLogout').classList.add('active');
}

function cerrarModales() {
    document.getElementById('modalLogout').classList.remove('active');
}

function ejecutarLogout() {
    window.location.href = '/logout';
}

// Cerrar modal al hacer clic fuera de él
window.onclick = function(event) {
    const modalLogout = document.getElementById('modalLogout');
    if (event.target === modalLogout) {
        cerrarModales();
    }
}