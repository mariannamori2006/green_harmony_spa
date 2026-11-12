from enum import unique
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True, validators=[RegexValidator(r'^\d{8}$', 'DNI debe tener 8 digitos.')], error_messages={'unique': 'Ya existe un cliente con este DNI.'})
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField(unique=True, error_messages={'unique':'Ya existe un cliente con este correo.'})
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['apellidos','nombres']
        verbose_name = "Cliente"
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'