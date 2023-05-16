from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BomberoUser
from .serializers import BomberoSerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from guardias.permissions import BomberoAdminAuthentication

from rest_framework import status

class TokenVerify(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class AdminVerify(APIView):
    authentication_classes = [BomberoAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    def post(self, request):
        codigo = request.data.get("codigo")
        password = request.data.get("password")

        try:
            bombero = BomberoUser.objects.get(codigo=codigo)

        except:
            return Response({"Mensaje": "El bombero no se encontro"})

        if bombero.check_password(password):
            serializer = BomberoSerializer(bombero)
            token, created = Token.objects.get_or_create(user=bombero)

            return Response(
                {"Mensaje": "Correcto", "Token": token.key, "Bombero": serializer.data}
            )

        else:
            return Response({"Mensaje": "Incorrecto"})
