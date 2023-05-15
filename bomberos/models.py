from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.hashers import make_password


class CodigoArea(models.Model):
    prefijo = models.CharField(max_length=1, default="+")
    codigo = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.prefijo + " " + str(self.codigo)


class Telefono(models.Model):
    numero = models.PositiveBigIntegerField()

    codigoArea = models.ForeignKey(
        CodigoArea, on_delete=models.RESTRICT, related_name="telefonos"
    )

    def __str__(self):
        return self.codigoArea.__str__() + " " + str(self.numero)


class CategoriaBombero(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Actividad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class DetalleCategoria(models.Model):
    categoria = models.ForeignKey(
        CategoriaBombero, on_delete=models.RESTRICT, related_name="detallesCategoria"
    )
    actividad = models.ForeignKey(
        Actividad, on_delete=models.RESTRICT, related_name="detalleCategoria"
    )

    def __str__(self):
        return self.categoria.__str__() + " - " + self.actividad.__str__()


class BomberoUserManager(BaseUserManager):
    def create_superuser(self, codigo, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.model(codigo=codigo, password=password, **extra_fields)
        user.save(using=self._db)
        return user


class BomberoUser(AbstractBaseUser, PermissionsMixin):
    codigo = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.ForeignKey(
        Telefono,
        on_delete=models.RESTRICT,
        related_name="bombero",
        null=True,
        blank=True,
    )
    categoria = models.ForeignKey(
        CategoriaBombero,
        on_delete=models.RESTRICT,
        related_name="bomberos",
        null=True,
        blank=True,
    )

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "codigo"

    objects = BomberoUserManager()

    def __str__(self):
        return str(self.codigo)

    def save(self, *args, **kwargs):
        try:
            old_password = BomberoUser.objects.get(codigo=self.codigo).password

            if old_password != self.password:
                self.password = make_password(self.password)

        except:
            self.password = make_password(self.password)

        super(BomberoUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Bomberos"
