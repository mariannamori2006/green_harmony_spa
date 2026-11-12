from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Pago(models.Model):
    METODOS = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Yape/Plin', 'Yape/Plin'),
        ('Transferencia', 'Transferencia'),
    ]
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Anulado', 'Anulado'),
    ]

    id = models.BigAutoField(primary_key=True)
    cita = models.ForeignKey(
        'Cita', on_delete=models.PROTECT, related_name='pagos'
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, 'El monto no puede ser negativo.')],
    )
    descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0, 'El descuento no puede ser negativo.')],
    )
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    fecha_pago = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f'Pago {self.id} - S/ {self.total}'

    @property
    def total(self):
        return (self.monto or 0) - (self.descuento or 0)

    def clean(self):
        super().clean()
        if self.monto is not None and self.descuento is not None:
            if self.descuento > self.monto:
                raise ValidationError(
                    {'descuento': 'El descuento no puede ser mayor al monto.'}
                )
        if self.cita_id and self.cita.estado == 'Cancelada':
            raise ValidationError(
                {'cita': 'No se puede registrar un pago para una cita cancelada.'}
            )