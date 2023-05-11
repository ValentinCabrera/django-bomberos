from django.db import models
from bomberos.models import BomberoUser, Actividad
from django.db.models import UniqueConstraint
from datetime import datetime


class EstadoGuardia(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Guardia(models.Model):
    fechaEntrada = models.DateField(auto_now_add=True)
    horaEntrada = models.TimeField(auto_now_add=True)
    fechaSalida = models.DateField(null=True, blank=True)
    horaSalida = models.TimeField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.ForeignKey(
        EstadoGuardia, on_delete=models.RESTRICT, related_name="guardias"
    )

    bombero = models.ForeignKey(
        BomberoUser, on_delete=models.RESTRICT, related_name="guardias"
    )

    def __str__(self):
        return (
            str(self.fechaEntrada)
            + " / "
            + str(self.horaEntrada.hour)
            + ":"
            + str(self.horaEntrada.minute)
        )

    def get_tiempo(self):
        estadoCerrada = EstadoGuardia.objects.get(nombre="cerrada")

        if self.estado == estadoCerrada:
            tiempoEntrada = datetime.combine(self.fechaEntrada, self.horaEntrada)
            tiempoSalida = datetime.combine(self.fechaSalida, self.horaSalida)

            diferencia = tiempoSalida - tiempoEntrada
            tiempo = diferencia.total_seconds() / 3600

            return tiempo

        return 0

    def it_actual_month(self):
        actual_month = datetime.now().month

        if self.fechaEntrada.month == actual_month:
            return True

        return False


class DetalleGuardia(models.Model):
    actividad = models.ForeignKey(
        Actividad, on_delete=models.RESTRICT, related_name="guardias"
    )
    guardia = models.ForeignKey(
        Guardia, on_delete=models.CASCADE, related_name="detalles"
    )

    def __str__(self):
        return self.guardia.__str__() + " - " + self.actividad.__str__()

    def save(self, *args, **kwargs):
        estado = EstadoGuardia.objects.get(nombre="abierta")

        if self.guardia.estado == estado:
            super(DetalleGuardia, self).save(*args, **kwargs)

        else:
            raise ValueError("La guardia ya esta cerrada")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["actividad", "guardia"], name="actividad_guardia_unique"
            )
        ]
