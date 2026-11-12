from django.contrib import admin
from .models import Cliente, Especialidad, Terapeuta, Servicio, Cita, Valoracion, Pago

# Register your models here.
for modelo in (Cliente, Especialidad, Terapeuta, Servicio, Cita, Valoracion, Pago):
    admin.site.register(modelo)

admin.site.site_header = 'Salón Spa - Administración'