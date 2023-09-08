from rest_framework import serializers
from .models import Guardia, EstadoGuardia, DetalleGuardia
from bomberos.serializers import BomberoSerializer, ActividadSerializer


class DetalleGuardiaSerializer(serializers.ModelSerializer):
    actividad = ActividadSerializer()

    class Meta:
        model = DetalleGuardia
        fields = ["actividad"]


class EstadoGuardiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoGuardia
        fields = "__all__"


class GuardiaSerializer(serializers.ModelSerializer):
    bombero = BomberoSerializer()
    estado = EstadoGuardiaSerializer()
    detalle = serializers.SerializerMethodField()
    tiempo = serializers.SerializerMethodField()
    horaEntrada = serializers.SerializerMethodField()
    horaSalida = serializers.SerializerMethodField()

    class Meta:
        model = Guardia
        fields = "__all__"

    def get_horaEntrada(self, obj):
        return obj.get_horaEntrada()

    def get_horaSalida(self, obj):
        return obj.get_horaSalida()

    def get_detalle(self, obj):    
        actividades = obj.get_actividades_posibles() 
        seleccionadas = obj.get_actividades()
        serializer = ActividadSerializer(actividades, many=True).data
        
        for i in serializer:
            i["check"] = i["id"] in seleccionadas

        return serializer

    def get_tiempo(self, obj):
        return obj.get_tiempo()


