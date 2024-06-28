from django.db import models
from usuarios.models import Bombero, Actividad
from django.utils import timezone

class Guardia(models.Model):
    fecha_hora_inicio = models.DateTimeField(auto_now_add=True)
    bombero = models.ForeignKey(Bombero, on_delete=models.CASCADE)
    fecha_hora_fin = models.DateTimeField(null=True, blank=True)
    bombero_cerro = models.ForeignKey(Bombero, on_delete=models.CASCADE, related_name='bombero_cerro', null=True, blank=True)

    def __str__(self):
        return self.bombero.nombre + ' ' + self.bombero.apellido + ' - ' + str(self.fecha_hora_inicio) + ' - ' + (str(self.fecha_hora_fin) if self.fecha_hora_fin else 'Abierta')
    
    def get_mes(self):       
        meses_espanol = {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre'
        }
        
        return meses_espanol[self.fecha_hora_inicio.month]
    
    def get_anio(self):
        return self.fecha_hora_inicio.strftime('%Y')
    
    def get_dia(self):
        return self.fecha_hora_inicio.strftime('%d')
    
    def get_hora_inicio(self):
        return self.fecha_hora_inicio.strftime('%H:%M')
    
    def get_actividades(self):
        guardia_actividad = self.guardia_actividad.all()
        actividades = list(map(lambda x: {"id" : x.actividad.id, "nombre" :x.actividad.nombre}, guardia_actividad))
        
        return actividades
    
    def get_duracion(self):
        duracion = None

        if self.fecha_hora_fin:
            duracion = self.fecha_hora_fin - self.fecha_hora_inicio
        
        else:
            fecha_hora_actual = timezone.now()
            duracion = fecha_hora_actual - self.fecha_hora_inicio

        # mostrar solo horas y minutos
        duracion = str(duracion).split(':')
        duracion = duracion[0] + 'hs y ' + duracion[1] + 'min'

        return str(duracion)
        
    def get_duracion_minutos(self):
        if self.fecha_hora_fin:
            duracion = self.fecha_hora_fin - self.fecha_hora_inicio
            return duracion.total_seconds() / 60
        
        else:
            fecha_hora_actual = timezone.now()
            duracion = fecha_hora_actual - self.fecha_hora_inicio
            return duracion.total_seconds() / 60

class GuardiaActividad(models.Model):
    guardia = models.ForeignKey(Guardia, on_delete=models.CASCADE, related_name="guardia_actividad")
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    def __str__(self):
        return self.guardia.bombero.nombre + ' ' + self.guardia.bombero.apellido + ' - ' + self.actividad.nombre