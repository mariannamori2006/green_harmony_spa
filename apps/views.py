from datetime import date
 
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.db.models import F, Q, Sum
from django.db.models.deletion import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
 
from .forms import (ClienteForm, EspecialidadForm, TerapeutaForm, ServicioForm,
                    CitaForm, ValoracionForm, PagoForm, RegistroForm)
from .models import Cliente, Especialidad, Terapeuta, Servicio, Cita, Valoracion, Pago

# Create your views here.
SECCIONES = {
    'clientes': {'modelo': Cliente, 'formulario': ClienteForm, 'titulo': 'Clientes',
                 'campos': ['nombres', 'apellidos', 'dni', 'telefono', 'correo']},
    'especialidades': {'modelo': Especialidad, 'formulario': EspecialidadForm, 'titulo': 'Especialidades',
                       'campos': ['nombre', 'descripcion', 'estado']},
    'terapeutas': {'modelo': Terapeuta, 'formulario': TerapeutaForm, 'titulo': 'Terapeutas',
                   'campos': ['nombres', 'apellidos', 'dni', 'especialidad', 'estado']},
    'servicios': {'modelo': Servicio, 'formulario': ServicioForm, 'titulo': 'Servicios',
                  'campos': ['nombre', 'duracion_minutos', 'precio', 'estado']},
    'citas': {'modelo': Cita, 'formulario': CitaForm, 'titulo': 'Citas',
              'campos': ['cliente', 'terapeuta', 'servicio', 'fecha', 'hora', 'estado']},
    'valoraciones': {'modelo': Valoracion, 'formulario': ValoracionForm, 'titulo': 'Valoraciones',
                     'campos': ['cita', 'tipo_piel', 'fecha']},
    'pagos': {'modelo': Pago, 'formulario': PagoForm, 'titulo': 'Pagos',
              'campos': ['cita', 'monto', 'descuento', 'metodo_pago', 'fecha_pago', 'estado']},
}
 
# Búsqueda mediante campos válidos, sin consultas SQL manuales.
BUSQUEDAS = {
    'clientes': ['nombres', 'apellidos', 'dni'],
    'especialidades': ['nombre', 'descripcion'],
    'terapeutas': ['nombres', 'apellidos', 'dni'],
    'servicios': ['nombre', 'descripcion'],
    'citas': ['cliente__nombres', 'cliente__apellidos', 'terapeuta__apellidos', 'motivo'],
    'valoraciones': ['cita__cliente__apellidos', 'tipo_piel'],
    'pagos': ['cita__cliente__apellidos', 'metodo_pago'],
}

ETIQUETAS = {
    'duracion_minutos': 'Duración (min)', 'metodo_pago': 'Método de pago',
    'fecha_pago': 'Fecha de pago', 'tipo_piel': 'Tipo de piel',
    'descripcion': 'Descripción', 'especialidad': 'Especialidad',
}
 
RELACIONES = {
    'terapeutas': ['especialidad'],
    'citas': ['cliente', 'terapeuta', 'servicio'],
    'valoraciones': ['cita__cliente'],
    'pagos': ['cita__cliente'],
}
 
 
def ingresar(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    formulario = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        login(request, formulario.get_user())
        if not request.POST.get('recordarme'):
            request.session.set_expiry(0)  # Cierra al terminar la sesión del navegador.
        else:
            request.session.set_expiry(60 * 60 * 24 * 14)
        return redirect('inicio')
    return render(request, 'control/login.html',
                  {'formulario': formulario, 'registro_abierto': settings.REGISTRATION_OPEN})
 
 
def registro(request):
    if not settings.REGISTRATION_OPEN:
        raise Http404('Registro deshabilitado. Contacta al administrador.')
    if request.user.is_authenticated:
        return redirect('inicio')
    formulario = RegistroForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save(commit=False)
        usuario.email = formulario.cleaned_data['email']
        usuario.save()  # Usuario común: sin is_staff ni is_superuser.
        login(request, usuario)
        request.session.set_expiry(0)
        messages.success(request, 'Cuenta creada correctamente.')
        return redirect('inicio')
    return render(request, 'control/registro.html', {'formulario': formulario})
 
 
@login_required
@require_POST
def salir(request):
    logout(request)
    return redirect('login')
 
 
@login_required
def inicio(request):
    resumen = [(item['titulo'], item['modelo'].objects.count(), nombre)
               for nombre, item in SECCIONES.items()]
    ingresos = Pago.objects.filter(estado='Pagado').aggregate(
        total=Sum(F('monto') - F('descuento')))['total'] or 0
    pendientes = Cita.objects.filter(estado__in=['Pendiente', 'Confirmada']).count()
    proximas = (Cita.objects.select_related('cliente', 'terapeuta', 'servicio')
                .filter(fecha__gte=date.today())
                .exclude(estado='Cancelada')
                .order_by('fecha', 'hora')[:8])
    return render(request, 'control/inicio.html', {
        'resumen': resumen, 'proximas': proximas,
        'ingresos': ingresos, 'pendientes': pendientes})
 
 
@login_required
def listado(request, seccion):
    info = SECCIONES.get(seccion)
    if info is None: raise Http404('Sección no disponible')
    objetos = info['modelo'].objects.all()
    if seccion in RELACIONES:
        objetos = objetos.select_related(*RELACIONES[seccion])
    q = request.GET.get('q', '').strip()[:100]
    if q:
        filtro = Q()
        for campo in BUSQUEDAS[seccion]:
            filtro |= Q(**{campo + '__icontains': q})
        objetos = objetos.filter(filtro)
    objetos = list(objetos[:300])
    filas = [[getattr(obj, campo) for campo in info['campos']] for obj in objetos]
    datos = list(zip(objetos, filas))
    cabeceras = [ETIQUETAS.get(c, info['modelo']._meta.get_field(c).verbose_name.capitalize())
                 for c in info['campos']]
    return render(request, 'control/listado.html',
                  {'info': info, 'seccion': seccion, 'datos': datos, 'q': q,
                   'cabeceras': cabeceras})

@login_required
def guardar(request, seccion, pk=None):
    info = SECCIONES.get(seccion)
    if info is None: raise Http404('Sección no disponible')
    objeto = get_object_or_404(info['modelo'], pk=pk) if pk else None
    formulario = info['formulario'](request.POST or None, request.FILES or None, instance=objeto)
    if request.method == 'POST' and formulario.is_valid():
        try:
            formulario.save()
            messages.success(request, 'Registro guardado correctamente.')
            return redirect('listado', seccion=seccion)
        except IntegrityError:
            formulario.add_error(None, 'No se pudo guardar: dato duplicado o relación inválida.')
    return render(request, 'control/formulario.html',
                  {'formulario': formulario, 'info': info, 'seccion': seccion, 'objeto': objeto})
 
 
@login_required
@require_POST
def eliminar(request, seccion, pk):
    info = SECCIONES.get(seccion)
    if info is None: raise Http404('Sección no disponible')
    objeto = get_object_or_404(info['modelo'], pk=pk)
    try:
        objeto.delete()
        messages.success(request, 'Registro eliminado.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar: tiene registros relacionados. '
                                'Elimina primero los dependientes.')
    return redirect('listado', seccion=seccion)
 
 
@login_required
def imprimir(request, seccion, pk):
    if seccion not in ('citas', 'valoraciones', 'pagos'):
        raise Http404('Documento no disponible')
    objeto = get_object_or_404(SECCIONES[seccion]['modelo'], pk=pk)
    return render(request, 'control/impresion.html', {'objeto': objeto, 'seccion': seccion})
 
 
@login_required
def reporte(request, tipo):
    """Reportes filtrables: citas, valoraciones y pagos."""
    if tipo not in ('citas', 'valoraciones', 'pagos'):
        raise Http404('Reporte no disponible')
 
    campo_fecha = {'citas': 'fecha', 'valoraciones': 'fecha', 'pagos': 'fecha_pago'}[tipo]
    modelo = SECCIONES[tipo]['modelo']
    objetos = modelo.objects.all()
    if tipo in RELACIONES:
        objetos = objetos.select_related(*RELACIONES[tipo])
 
    desde = request.GET.get('desde', '')
    hasta = request.GET.get('hasta', '')
    estado = request.GET.get('estado', '')
    try:
        if desde: objetos = objetos.filter(**{campo_fecha + '__gte': date.fromisoformat(desde)})
        if hasta: objetos = objetos.filter(**{campo_fecha + '__lte': date.fromisoformat(hasta)})
    except ValueError:
        messages.error(request, 'Las fechas deben tener formato AAAA-MM-DD.')
        return redirect('reporte', tipo=tipo)
 
    estados = getattr(modelo, 'ESTADOS', [])
    if estado in dict(estados):
        objetos = objetos.filter(estado=estado)
 
    objetos = list(objetos[:500])
    total_pagado = sum(p.total for p in objetos if p.estado == 'Pagado') if tipo == 'pagos' else 0

    return render(request, 'control/reporte.html', {
        'tipo': tipo, 'titulo': SECCIONES[tipo]['titulo'],
        'objetos': objetos, 'desde': desde, 'hasta': hasta,
        'estado': estado, 'estados': estados, 'total_pagado': total_pagado})