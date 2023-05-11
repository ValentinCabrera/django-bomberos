from django.contrib import admin

from .models import Guardia, EstadoGuardia, DetalleGuardia

admin.site.register(Guardia)
admin.site.register(EstadoGuardia)
admin.site.register(DetalleGuardia)