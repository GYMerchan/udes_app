from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from datetime import timedelta, datetime 
from django import forms
from django.core.exceptions import ValidationError

# Modelo para el sitio
class Sitio(models.Model):

    OPCIONES_LUGAR_SITIO = [
        ('biblioteca', 'Biblioteca'),
        ('informatica 1', 'Informatica 1'),
        ('informatica 2', 'Informatica 2'),
        ('informatica 3', 'Informatica 3'),
        ('aula 1', 'Aula 1'),
        ('aula 2', 'Aula 2'),
        ('aula 3', 'Aula 3'),
        ('aula 4', 'Aula 4'),
        ('aula 5', 'Aula 5'),
        ('laboratorio 1', 'Laboratorio 1'),
        ('laboratorio 2', 'Laboratorio 2'),
        ('laboratorio 3', 'Laboratorio 3'),
    ]
    OPCIONES_TIPO_USUARIO = [
        ('biblioteca', 'Biblioteca'),
        ('informatica ', 'Informatica '),
        ('aula ', 'Aula '),
        ('laboratorio ', 'Laboratorio '),
    ]

    lugar_sitio = models.CharField(max_length=50, choices=OPCIONES_LUGAR_SITIO, default=False) # Tipo de sitio a reservar
    tipo_usuario = models.CharField(max_length=50, choices=OPCIONES_TIPO_USUARIO, default=False)
    aforo_maximo = models.PositiveIntegerField() # Aforo máximo del sitio
    max_horas_diarias = models.TimeField() # Máximo de horas diarias que se puede reservar el sitio

    def __str__(self):
        return self.lugar_sitio

# Modelo para el registro de las reservas
class Reserva(models.Model):
    
    OPCIONES_ESTADO_RESERVA = (
        ('realizada', 'Realizada'),
        ('por hacer', 'Por hacer'),
    )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None)
    sitio = models.ForeignKey(Sitio,on_delete=models.CASCADE,verbose_name="Sitio a reservar",related_name="reservas")
    fecha_reserva = models.DateField(null=True, blank=True, verbose_name="Fecha de la reserva")
    hora_inicio = models.TimeField(null=True, blank=True,verbose_name="Hora inicio")
    hora_fin = models.TimeField(null=True, blank=True,verbose_name="Hora Fin")
    estado_reserva = models.CharField(max_length=20, choices=OPCIONES_ESTADO_RESERVA, default=False)
    reservado = models.BooleanField(default=False, verbose_name="Asistió")
    def __str__(self):
        return self.estado_reserva
    
    def clean(self):
        # aca me traigo las reservas realizadas por el mismo estudiante para el mismo sitio en la misma fecha
        reservas_mismo_dia = Reserva.objects.filter(
            sitio=self.sitio,
            fecha_reserva=self.fecha_reserva,
            usuario=self.usuario
        ).exclude(id=self.id)

        
        # Sumar las horas de reservazzione, tocó comvertir los datos a datetime porque timefield no dejaba restar
        horas_reservadas = sum(
            (datetime.combine(datetime.min, reserva.hora_fin) - datetime.combine(datetime.min, reserva.hora_inicio)).total_seconds() / 3600
            for reserva in reservas_mismo_dia
        )

        # acá le estoy asignando las nuevas horas a las anteriores +=
        horas_reservadas += (datetime.combine(datetime.min, self.hora_fin) - datetime.combine(datetime.min, self.hora_inicio)).total_seconds() / 3600

        # Si se superan las 3 horas, lanzar una excepción
        if horas_reservadas > 3:
            raise ValidationError('No se pueden reservar más de 3 horas al día para el mismo sitio')

    
    # si se puede cancelar una reserva si ya pasaron 15 minutos de la hora de inicio, filtrando el usuario de control
    def puede_cancelar_reserva(self, user):
        #  si es usuario  del grupo Usuario_Control
        if not user.groups.filter(name='Usuario_Control').exists():
            return False
        #  si ya se ha marcado la reserva como "reservado"
        if self.reservado:
            return False
        hora_actual = timezone.localtime(timezone.now()).time()
        minutos_transcurridos = (hora_actual.hour - self.hora_inicio.hour) * 60 + hora_actual.minute - self.hora_inicio.minute
        # calculo si ya van más de 15 minutos desde la hora de inicio de la reserva
        if minutos_transcurridos >= 15:
            return True
        return False

    #el estudiante puede modificar o cancelar la reserva
    def puede_modificar_cancelar_reserva(reserva):#estudiante puede hacerlo si la hora de inicio de la reserva es mayor a la hora actual más 30 minutos.
        if reserva.hora_inicio > timezone.now() + timedelta(minutes=30):
            return True
        else:
            return False


