from django.core.validators import MinValueValidator
from django.forms.models import modelform_defines_fields
from django.db import models

class Servicio(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'), ('Inactivo', 'Inactivo')
    ]
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True, error_messages={'unique':'Ya existe un servicio con este nombre.'})
    descripcion = models.TextField()
    duracion_minutos = models.PositiveIntegerField(validators=[MinValueValidator(1, 'La duración debe ser mayor a 0.')])
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0, 'El precio no puede ser negativo.')])
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activo')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre