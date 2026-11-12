from django.core.exceptions import ValidationError
from django.db import models


class Valoracion(models.Model):
    id = models.BigAutoField(primary_key=True)
    cita = models.ForeignKey(
        'Cita', on_delete=models.CASCADE, related_name='valoraciones'
    )
    tipo_piel = models.CharField(max_length=100)
    descripcion = models.TextField()
    recomendaciones = models.TextField()
    fecha = models.DateField()

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'

    def __str__(self):
        return f'Valoración {self.id} - Cita {self.cita_id}'

    def clean(self):
        super().clean()
        if self.cita_id and self.cita.estado == 'Cancelada':
            raise ValidationError(
                {'cita': 'No se puede valorar una cita cancelada.'}
            )