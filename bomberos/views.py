from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BomberoUser
from .serializers import BomberoSerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from guardias.permissions import BomberoAdminAuthentication, BomberoSuperAuthentication

from rest_framework import status

class TokenVerify(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bombero = request.user
        serializer = BomberoSerializer(bombero)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminVerify(APIView):
    authentication_classes = [BomberoAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    
class SuperVerify(APIView):
    authentication_classes = [BomberoSuperAuthentication]
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
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if bombero.check_password(password):
            serializer = BomberoSerializer(bombero)
            token, created = Token.objects.get_or_create(user=bombero)

            return Response(
                {"Mensaje": "Correcto", "Token": token.key, "Bombero": serializer.data}
            )

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class SuperListPersonal(APIView):
    authentication_classes = [BomberoSuperAuthentication]
    permission_classes = [IsAuthenticated]

    """
    get retorna el listado de bomberos en general
    
    """

    def get (self, request):
        bomberos = BomberoUser.objects.all()

        serializer = BomberoSerializer(bomberos, many=True)
        return Response(serializer.data)