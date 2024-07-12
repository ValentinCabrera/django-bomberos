from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Bombero(models.Model):
    ROLES = (
        ('1', 'Jefe de Cuerpo'),
        ('2', 'Administrador'),
        ('3', 'Bombero'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bombero')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=10)
    rol = models.CharField(max_length=1, choices=ROLES)

    def __str__(self):
        return self.nombre + ' ' + self.apellido

class BomberoCategoria(models.Model):
    bombero = models.ForeignKey(Bombero, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.bombero.nombre + ' ' + self.bombero.apellido + ' - ' + self.categoria.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=50)
    hecha = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
class CategoriaActividad(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    def __str__(self):
        return self.categoria.nombre + ' - ' + self.actividad.nombre