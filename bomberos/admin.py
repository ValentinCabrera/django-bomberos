from django.contrib import admin
from .models import BomberoUser, CategoriaBombero, CodigoArea, Telefono, Actividad, DetalleCategoria

admin.site.register(BomberoUser)
admin.site.register(CategoriaBombero)
admin.site.register(DetalleCategoria)
admin.site.register(CodigoArea)
admin.site.register(Telefono)
admin.site.register(Actividad)