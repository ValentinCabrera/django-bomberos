from .models import Guardia, Actividad, GuardiaActividad
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class GuardiaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bombero = user.bombero.first()

        guardias = Guardia.objects.filter(bombero=bombero, fecha_hora_fin__isnull=True)
        
        actividades = []

        for i in Actividad.objects.filter(hecha=False):
            actividades.append({
                'id': i.id,
                'nombre': i.nombre
            })

        if guardias.exists():
            guardia = guardias.last()

            guardia_data = {
                'id': guardia.id,
                'hora_inicio': guardia.get_hora_inicio(),
                'duracion': guardia.get_duracion(),
                'actividades': guardia.get_actividades(),
            }

            return Response({'guardia': guardia_data, 'actividades': actividades}, status=200)
        
        else:
            return Response({'guardia': None, 'actividades': actividades}, status=200)
        
    def post(self, request):
        user = request.user
        bombero = user.bombero.first()

        guardia = Guardia.objects.create(bombero=bombero)
        guardia_data = {
            'id': guardia.id,
            'hora_inicio': guardia.get_hora_inicio(),
            'duracion': guardia.get_duracion(),
            'actividades': guardia.get_actividades(),
        }

        return Response({'guardia': guardia_data}, status=200)
    
    def put(self, request):
        guardia_id = request.data.get('guardia_id')
        guardia = Guardia.objects.get(id=guardia_id)

        guardia_actividades = request.data.get('actividades')

        for actividad_id in guardia_actividades:

            actividad = Actividad.objects.get(id=actividad_id)
            actividad.hecha = True
            actividad.save()

            GuardiaActividad.objects.create(guardia=guardia, actividad=actividad)

        return Response(GuardiaView.get(self, request).data, status=200)
        
    def delete(self, request):
        user = request.user
        bombero = user.bombero.first()

        guardia_id = request.data.get('guardia_id')
        guardia = Guardia.objects.get(id=guardia_id)

        guardia.fecha_hora_fin = timezone.now()
        guardia.bombero_cerro = bombero
        guardia.save()

        return Response(MisGuardiasView.get(self, request).data, status=200)

class MisGuardiasView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bombero = user.bombero.first()

        guardias = Guardia.objects.filter(bombero=bombero)
        guardias_values = []
        horas_del_mes_actual = 0

        for guardia in guardias:
            guardias_values.append({
                'id': guardia.id,
                'dia': guardia.get_dia(),
                'hora_inicio': guardia.get_hora_inicio(),
                'mes': guardia.get_mes(),
                'anio': guardia.get_anio(),
                'duracion': guardia.get_duracion(),
                'hora_fin': guardia.fecha_hora_fin,
                'actividades': guardia.get_actividades(),
            })

            if guardia.fecha_hora_fin:
                horas_del_mes_actual += guardia.fecha_hora_fin.hour - guardia.fecha_hora_inicio.hour



        return Response({'guardias': guardias_values}, status=200)
    
class HorasAcumuladasView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bombero = user.bombero.first()

        guardias = Guardia.objects.filter(bombero=bombero)

        horas_acumuladas_data = []
        
        mes_actual = guardias[0].get_mes()
        anio_actual = guardias[0].get_anio()
        horas_del_mes_acumuladas = 0

        for guardia in guardias:
            mes = guardia.get_mes()
            anio = guardia.get_anio()

            if mes_actual == mes and anio_actual == anio:
                horas_del_mes_acumuladas += guardia.get_duracion_minutos()

            else:
                horas = horas_del_mes_acumuladas / 60
                minutos = horas_del_mes_acumuladas % 60

                horas = int(horas)
                minutos = int(minutos)

                horas_acumuladas_data.append({
                    'id': len(horas_acumuladas_data),
                    'mes': mes_actual,
                    'anio': anio_actual,
                    'horas': horas,
                    'minutos': minutos
                })

                mes_actual = mes
                anio_actual = anio
                horas_del_mes_acumuladas = guardia.get_duracion_minutos()

        else:
            horas = horas_del_mes_acumuladas / 60
            minutos = horas_del_mes_acumuladas % 60

            horas = int(horas)
            minutos = int(minutos)

            horas_acumuladas_data.append({
                'id': len(horas_acumuladas_data),
                'mes': mes_actual,
                'anio': anio_actual,
                'horas': horas,
                'minutos': minutos
            })

        return Response({'horas_acumuladas': horas_acumuladas_data}, status=200)