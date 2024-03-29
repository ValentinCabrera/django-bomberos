from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Guardia
from .serializers import GuardiaSerializer
from bomberos.models import BomberoUser
from datetime import date, datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import DetalleGuardia, EstadoGuardia
from bomberos.models import Actividad

from .permissions import BomberoAdminAuthentication


class UserAddDetalle(APIView):
    """
    post permite al usuario agregar un detalle a una guardia {"guardia":id, "actividad":id}
    retorna la guardia

    """

    def post(self, request):
        data = request.data

        guardia = Guardia.objects.get(id=data.get("guardia"))
        actividad = Actividad.objects.get(id=data.get("actividad"))

        detalle = DetalleGuardia(guardia=guardia, actividad=actividad)
        detalle.save()

        serializer = GuardiaSerializer(guardia)

        return Response(serializer.data)
    

class UserRemoveDetalle(APIView):
    """
    post permite al usuario eliminar un detalle a una guardia {"guardia":id, "actividad":id}
    retorna la guardia

    """

    def post(self, request):
        data = request.data

        guardia = Guardia.objects.get(id=data.get("guardia"))
        actividad = Actividad.objects.get(id=data.get("actividad"))

        detalle = DetalleGuardia.objects.get(guardia=guardia, actividad=actividad)
        detalle.delete()

        serializer = GuardiaSerializer(guardia)
        
        return Response(serializer.data)

class AdminGuardiasAbiertas(APIView):
    """
    get retorna las guardias abiertas para los admins
    post permite cerrar una guarda abierta {"guardia":id}

    falta verificar el sea admin
    """

    authentication_classes = [BomberoAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estadoAbierta = EstadoGuardia.objects.get(nombre="abierta")
        guardias = Guardia.objects.filter(estado=estadoAbierta)

        serializer = GuardiaSerializer(guardias, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.get("guardia")
        guardia = Guardia.objects.get(id=data)

        estadoAbierta = EstadoGuardia.objects.get(nombre="abierta")
        if guardia.estado == estadoAbierta:
            estadoCerrada = EstadoGuardia.objects.get(nombre="cerrada")
            guardia.estado = estadoCerrada
            guardia.fechaSalida = date.today()
            guardia.horaSalida = datetime.now().time()

            guardia.save()

        serializer = GuardiaSerializer(guardia)

        return Response(serializer.data)


class AdminGuardiasCerradas(APIView):
    """
    get retorna las guardias cerradas para los admins revisarlas
    post permite revisar una guarda cerrada {"guardia":id}

    falta verificar que sea admin

    """

    def get(self, request):
        estadoCerradas = EstadoGuardia.objects.get(nombre="cerrada")
        guardias = Guardia.objects.filter(estado=estadoCerradas)

        serializer = GuardiaSerializer(guardias, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.get("guardia")
        guardia = Guardia.objects.get(id=data)

        estadoCerrada = EstadoGuardia.objects.get(nombre="cerrada")
        if guardia.estado == estadoCerrada:
            estadoRevisada = EstadoGuardia.objects.get(nombre="revisada")
            guardia.estado = estadoRevisada
            guardia.save()

        serializer = GuardiaSerializer(guardia)

        return Response(serializer.data)


class UserListGuardias(APIView):
    """
    post retorna las guardias de un usuario en especifico {"bombero":codigo}
    retorna las horas totales del mes

    falta verificar que el usuario sea quien dice ser

    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        bombero = request.user

        month = request.data.get("month")
        year = request.data.get("year")

        if month:
            month = int(month)

        if year:
            year = int(year)

        estadoRevisada = EstadoGuardia.objects.get(nombre="revisada")

        guardias_revisadas = Guardia.objects.filter(
            bombero=bombero, estado=estadoRevisada
        )

        guardias = []

        horas_totales = 0

        for i in guardias_revisadas:
            if i.is_month(month, year):
                guardias.append(i)
                horas_totales += i.get_tiempo()

        horas_totales = round(horas_totales, 1)
        serializer = GuardiaSerializer(guardias, many=True)

        return Response({"guardias": serializer.data, "horasTotales": horas_totales})


class SuperListGuardias(APIView):
    """
    get retorna todas las guardias a un super
    post retorna las guardias filtradas a un super {**filtros}

    falta verificar que sea super

    """

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get(self, request):
        guardias = Guardia.objects.all()
        serializer = GuardiaSerializer(guardias, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        try:
            guardias = Guardia.objects.filter(**data)
            serializer = GuardiaSerializer(guardias, many=True)

            return Response(serializer.data)

        except:
            return Response("Alguno de los filtros ingresados es incorrecto")


class UserOpenGuardia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bombero = request.user

        estadoAbierto = EstadoGuardia.objects.get(nombre="abierta")
        try:
            guardia = Guardia.objects.get(bombero=bombero, estado=estadoAbierto)
            serializer = GuardiaSerializer(guardia)

            return Response(serializer.data)

        except:
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserUpdateGuardia(APIView):
    """

    post cierra la guarda abierta de un usario o
    abre una guardia si el usuario no tiene ninguna abierta {"bombero":codigo, "descripcion":None}

    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        bombero = request.user

        estadoAbierto = EstadoGuardia.objects.get(nombre="abierta")

        try:
            guardia = Guardia.objects.get(bombero=bombero, estado=estadoAbierto)

            if data.get("descripcion"):
                guardia.descripcion = data.get("descripcion")

            estadoCerrada = EstadoGuardia.objects.get(nombre="cerrada")

            guardia.estado = estadoCerrada
            guardia.fechaSalida = date.today()
            guardia.horaSalida = datetime.now().time()
            guardia.save()

            serializer = GuardiaSerializer(guardia)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except:
            guardia = Guardia(bombero=bombero, estado=estadoAbierto)
            guardia.save()

            serializer = GuardiaSerializer(guardia)
            return Response(serializer.data)
