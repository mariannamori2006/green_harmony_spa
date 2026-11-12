from django.core.validators import RegexValidator
from .Especialidad import Especialidad
from django.db import models

class Terapeuta(models.Model):
    ESTADOS= [
        ('Activo', 'Activo'), ('Inactivo', 'Inactivo')
    ]
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True, validators=[RegexValidator(r'^\d{8}$','DNI debe tener 8 dígitos.')], error_messages={'unique':'Ya existe un terapeuta con este DNI.'})
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True, error_messages={'unique':'Ya existe un terapeuta con este correo.'})
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name='terapeutas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activo') 

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Terapeuta'
        verbose_name_plural = 'Terapeutas'

    def __str__(self):
        return f'{self.apellidos}, {self.nombres}'