from django.contrib import admin
from .models import Guardia, GuardiaActividad

@admin.register(Guardia)
class GuardiaAdmin(admin.ModelAdmin):
    list_display = ('bombero', 'fecha_hora_inicio', 'fecha_hora_fin', 'bombero_cerro')

@admin.register(GuardiaActividad)
class GuardiaActividadAdmin(admin.ModelAdmin):
    list_display = ('guardia', 'actividad')