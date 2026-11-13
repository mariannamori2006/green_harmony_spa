document.addEventListener('DOMContentLoaded', function () {
    // Menú lateral en pantallas pequeñas
    var lateral = document.getElementById('lateral');
    var abrir = document.getElementById('abrir-menu');
    if (lateral && abrir) {
        abrir.addEventListener('click', function () {
            var abierto = lateral.classList.toggle('abierto');
            abrir.setAttribute('aria-expanded', abierto);
        });
        document.addEventListener('click', function (e) {
            if (lateral.classList.contains('abierto') && !lateral.contains(e.target) && e.target !== abrir) {
                lateral.classList.remove('abierto');
            }
        });
    }

    // Confirmación antes de eliminar
    document.querySelectorAll('form[data-confirmar]').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (form.dataset.ok) return;
            e.preventDefault();
            var d = document.createElement('dialog');
            d.innerHTML = '<h3>Eliminar registro</h3><p>' + form.dataset.confirmar +
                '</p><div class="acciones-form"><button type="button" class="btn btn-suave" data-no>Cancelar</button>' +
                '<button type="button" class="btn btn-peligro" data-si>Sí, eliminar</button></div>';
            document.body.appendChild(d);
            d.showModal();
            d.querySelector('[data-no]').onclick = function () { d.close(); d.remove(); };
            d.querySelector('[data-si]').onclick = function () { form.dataset.ok = '1'; form.submit(); };
            d.addEventListener('cancel', function () { d.remove(); });
        });
    });

    // Imprimir / guardar como PDF desde el navegador
    document.querySelectorAll('[data-imprimir]').forEach(function (b) {
        b.addEventListener('click', function () { window.print(); });
    });

    // Mostrar u ocultar contraseña
    document.querySelectorAll('[data-ver-clave]').forEach(function (b) {
        b.addEventListener('click', function () {
            var campo = b.parentElement.querySelector('input');
            var oculto = campo.type === 'password';
            campo.type = oculto ? 'text' : 'password';
            b.textContent = oculto ? 'Ocultar' : 'Mostrar';
        });
    });

    // Los avisos desaparecen solos
    document.querySelectorAll('.mensaje').forEach(function (m) {
        setTimeout(function () { m.remove(); }, 6000);
    });

    // Selector de vista (Tarjetas vs Tabla) en listados
    var contenedorListado = document.getElementById('contenedor-listado');
    var botonesVista = document.querySelectorAll('[data-vista]');
    if (contenedorListado && botonesVista.length) {
        var vistaGuardada = localStorage.getItem('spa_vista_preferida') || 'tarjetas';
        aplicarVista(vistaGuardada);

        botonesVista.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var vista = btn.getAttribute('data-vista');
                localStorage.setItem('spa_vista_preferida', vista);
                aplicarVista(vista);
            });
        });

        function aplicarVista(vista) {
            if (vista === 'tabla') {
                contenedorListado.classList.add('vista-modo-tabla');
                contenedorListado.classList.remove('vista-modo-tarjetas');
            } else {
                contenedorListado.classList.add('vista-modo-tarjetas');
                contenedorListado.classList.remove('vista-modo-tabla');
            }
            botonesVista.forEach(function (b) {
                b.classList.toggle('activo', b.getAttribute('data-vista') === vista);
            });
        }
    }
});