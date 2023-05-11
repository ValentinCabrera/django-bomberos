from rest_framework import serializers
from .models import Guardia, EstadoGuardia, DetalleGuardia
from bomberos.serializers import BomberoSerializer, ActividadSerializer

class DetalleGuardiaSerializer(serializers.ModelSerializer):
    actividad = ActividadSerializer()
    
    class Meta:
        model = DetalleGuardia
        fields = ['actividad']

class EstadoGuardiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoGuardia
        fields = '__all__'

class GuardiaSerializer(serializers.ModelSerializer):
    bombero = BomberoSerializer()
    estado = EstadoGuardiaSerializer()
    detalle = serializers.SerializerMethodField()
    tiempo = serializers.SerializerMethodField()

    class Meta:
        model = Guardia
        fields = '__all__'

    def get_detalle(self, obj):
        detalles = DetalleGuardia.objects.filter(guardia=obj)
        serializer = DetalleGuardiaSerializer(detalles, many=True)
        return serializer.data
    
    def get_tiempo(self, obj):
        return obj.get_tiempo()