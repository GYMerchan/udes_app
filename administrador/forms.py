from django import forms
from.models import Sitio, Reserva
from django.contrib.auth.models import User, Group
from django.forms import ModelChoiceField

class SitioForm(forms.ModelForm):
    max_horas_diarias = forms.ChoiceField(choices=[('1:00','1:00'), ('2:00','2:00'), ('3:00','3:00'), ('4:00','4:00'), ('5:00','5:00'), ('6:00','6:00'), ('7:00','7:00'), ('8:00','8:00'), ('9:00','9:00'), ('10:00','10:00')], label='Maximo de Horas Diarias')
    
    class Meta:
        model = Sitio
        #fields = ['nombre', 'descripcion']
        fields = '__all__'

    def __init__(self, *args, **kwargs):# lo pongo bonito
        super().__init__(*args, **kwargs)
        self.fields['lugar_sitio'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_usuario'].widget.attrs.update({'class': 'form-control'})
        self.fields['aforo_maximo'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_horas_diarias'].widget.attrs.update({'class': 'form-control'})



''' #para futuras ocasiones tiene estilos
class ReservaForm(forms.Form):
    fecha = forms.DateField(label='Fecha', widget=forms.SelectDateWidget)
    hora_inicio = forms.ChoiceField(choices=[('8:00','8:00'), ('9:00','9:00'), ('10:00','10:00'), ('11:00','11:00'), ('12:00','12:00'), ('13:00','13:00'), ('14:00','14:00'), ('15:00','15:00'), ('16:00','16:00'), ('17:00','17:00'), ('18:00','18:00'), ('19:00','19:00'), ('20:00','20:00'), ('21:00','21:00')], label='Hora de inicio')
    hora_fin = forms.ChoiceField(choices=[('8:00','8:00'), ('9:00','9:00'), ('10:00','10:00'), ('11:00','11:00'), ('12:00','12:00'), ('13:00','13:00'), ('14:00','14:00'), ('15:00','15:00'), ('16:00','16:00'), ('17:00','17:00'), ('18:00','18:00'), ('19:00','19:00'), ('20:00','20:00'), ('21:00','21:00')], label='Hora de fin')
    usuario = ModelChoiceField(queryset=User.objects.filter(groups__name='Estudiante').order_by('first_name'), label='Usuario')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora_inicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora_fin'].widget.attrs.update({'class': 'form-control'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

'''
class ReservaForm(forms.ModelForm):

    hora_inicio = forms.ChoiceField(choices=[('8:00','8:00'), ('9:00','9:00'), ('10:00','10:00'), ('11:00','11:00'), ('12:00','12:00'), ('13:00','13:00'), ('14:00','14:00'), ('15:00','15:00'), ('16:00','16:00'), ('17:00','17:00'), ('18:00','18:00'), ('19:00','19:00'), ('20:00','20:00'), ('21:00','21:00')], label='Hora de inicio')
    hora_fin = forms.ChoiceField(choices=[('8:00','8:00'), ('9:00','9:00'), ('10:00','10:00'), ('11:00','11:00'), ('12:00','12:00'), ('13:00','13:00'), ('14:00','14:00'), ('15:00','15:00'), ('16:00','16:00'), ('17:00','17:00'), ('18:00','18:00'), ('19:00','19:00'), ('20:00','20:00'), ('21:00','21:00')], label='Hora de fin')
    usuario = ModelChoiceField(queryset=User.objects.filter(groups__name='Estudiante').order_by('first_name'), label='Usuario')
    

    class Meta:
        model = Reserva
        fields = '__all__'
    
        widgets = {
            "fecha_reserva": forms.SelectDateWidget()
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")