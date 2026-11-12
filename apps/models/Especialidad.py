from django.db import models

class Especialidad(models.Model):
    ESTADOS = [
        ('Activa', 'Activa'),('Inactiva', 'Inactiva')
    ]
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, error_messages={'unique':'Ya existe una especialidad con este nombre'})
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activa')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombre