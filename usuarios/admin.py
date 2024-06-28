from django.contrib import admin
from .models import Bombero, Actividad, Categoria, BomberoCategoria, CategoriaActividad

@admin.register(Bombero)
class BomberoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'codigo', 'telefono', 'rol')

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(BomberoCategoria)
class BomberoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('bombero', 'categoria')

@admin.register(CategoriaActividad)
class CategoriaActividadAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'actividad')