from rest_framework import serializers
from .models import BomberoUser, CategoriaBombero, Actividad

class CategoriaBomberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaBombero
        fields = ["nombre", "descripcion"]

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class BomberoSerializer(serializers.ModelSerializer):
    categoria = CategoriaBomberoSerializer()

    class Meta:
        model = BomberoUser
        fields = ["codigo", "categoria", "nombre", "apellido", "telefono"]