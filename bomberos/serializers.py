from rest_framework import serializers
from .models import BomberoUser, CategoriaBombero, Actividad, DetalleCategoria

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class DetalleCategoriaSerializer(serializers.ModelSerializer):
    actividad = ActividadSerializer()

    class Meta:
        model = DetalleCategoria
        fields = ["actividad"]

class CategoriaBomberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaBombero
        fields = ["nombre"]


class BomberoSerializer(serializers.ModelSerializer):
    categoria = CategoriaBomberoSerializer()

    class Meta:
        model = BomberoUser
        fields = ["codigo", "categoria", "nombre", "apellido", "telefono"]