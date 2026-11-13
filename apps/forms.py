from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Cliente, Especialidad, Terapeuta, Servicio, Cita, Valoracion, Pago


class FormularioBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.DateInput): campo.widget.input_type = 'date'
            if isinstance(campo.widget, forms.TimeInput): campo.widget.input_type = 'time'
            campo.widget.attrs.setdefault('class', 'campo')


class ClienteForm(FormularioBase):
    class Meta:
        model = Cliente
        fields = ['nombres', 'apellidos', 'dni', 'fecha_nacimiento', 'telefono', 'direccion', 'correo']
        widgets = {'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d')}


class EspecialidadForm(FormularioBase):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}


class TerapeutaForm(FormularioBase):
    class Meta:
        model = Terapeuta
        fields = ['nombres', 'apellidos', 'dni', 'telefono', 'correo', 'especialidad', 'estado']


class ServicioForm(FormularioBase):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'duracion_minutos', 'precio', 'estado', 'imagen']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}


class CitaForm(FormularioBase):
    class Meta:
        model = Cita
        fields = ['cliente', 'terapeuta', 'servicio', 'fecha', 'hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d'),
            'hora': forms.TimeInput(format='%H:%M'),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo terapeutas y servicios activos (más el ya asignado si se edita).
        t_actual = self.instance.terapeuta_id
        s_actual = self.instance.servicio_id
        self.fields['terapeuta'].queryset = Terapeuta.objects.filter(
            Q(estado='Activo') | Q(pk=t_actual))
        self.fields['servicio'].queryset = Servicio.objects.filter(
            Q(estado='Activo') | Q(pk=s_actual))


class ValoracionForm(FormularioBase):
    class Meta:
        model = Valoracion
        fields = ['cita', 'tipo_piel', 'descripcion', 'recomendaciones', 'fecha']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'recomendaciones': forms.Textarea(attrs={'rows': 3}),
        }


class PagoForm(FormularioBase):
    class Meta:
        model = Pago
        fields = ['cita', 'monto', 'descuento', 'metodo_pago', 'fecha_pago', 'estado']
        widgets = {'fecha_pago': forms.DateInput(format='%Y-%m-%d')}


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    codigo = forms.CharField(
        label='Código de invitación (solo en producción)', required=False,
        widget=forms.PasswordInput,
        help_text='En desarrollo se puede dejar vacío; en producción es obligatorio.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_codigo(self):
        from django.utils.crypto import constant_time_compare
        codigo = self.cleaned_data.get('codigo', '')
        if not settings.DEBUG and not constant_time_compare(codigo, settings.REGISTRATION_CODE):
            raise forms.ValidationError('Código de invitación no válido.')
        return codigo