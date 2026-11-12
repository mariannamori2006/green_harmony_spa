from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Cita(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Atendida', 'Atendida'),
        ('Cancelada', 'Cancelada'),
    ]

    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(
        'Cliente', on_delete=models.PROTECT, related_name='citas'
    )
    terapeuta = models.ForeignKey(
        'Terapeuta', on_delete=models.PROTECT, related_name='citas'
    )
    servicio = models.ForeignKey(
        'Servicio', on_delete=models.PROTECT, related_name='citas'
    )
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f'Cita {self.id} - {self.cliente} ({self.fecha} {self.hora})'

    def clean(self):
        super().clean()

        # 1. No permitir fechas pasadas al registrar una cita nueva
        if self.fecha and not self.pk and self.fecha < timezone.localdate():
            raise ValidationError({'fecha': 'La fecha no puede ser anterior a hoy.'})

        # Las citas canceladas no ocupan horario
        if self.estado == 'Cancelada':
            return

        if self.fecha and self.hora:
            otras = Cita.objects.filter(
                fecha=self.fecha, hora=self.hora
            ).exclude(estado='Cancelada').exclude(pk=self.pk)

            # 2. El terapeuta no puede tener dos citas a la misma hora
            if self.terapeuta_id and otras.filter(terapeuta_id=self.terapeuta_id).exists():
                raise ValidationError(
                    'El terapeuta ya tiene una cita en ese horario.'
                )

            # 3. El cliente no puede tener dos citas a la misma hora
            if self.cliente_id and otras.filter(cliente_id=self.cliente_id).exists():
                raise ValidationError(
                    'El cliente ya tiene una cita en ese horario.'
                )

        # 4. Solo terapeutas y servicios activos
        if self.terapeuta_id and self.terapeuta.estado != 'Activo':
            raise ValidationError({'terapeuta': 'El terapeuta está inactivo.'})
        if self.servicio_id and self.servicio.estado != 'Activo':
            raise ValidationError({'servicio': 'El servicio está inactivo.'})