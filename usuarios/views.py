from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Bombero
from django.contrib.auth.models import User

class BomberoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bomberos = Bombero.objects.all()

        bomberos_data = []

        for bombero in bomberos:
            bomberos_data.append({
                'codigo': bombero.user.username,
                'nombre': bombero.nombre,
                'apellido': bombero.apellido,
                'telefono': bombero.telefono,
            })

        return Response({'bomberos': bomberos_data}, status=200)
    
    def post(self, request):
        codigo = request.data.get('codigo')
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido')
        telefono = request.data.get('telefono')

        user = User.objects.create_user(username=codigo, password=nombre+apellido)
        user.save()

        bombero = Bombero(user=user, nombre=nombre, apellido=apellido, telefono=telefono)
        bombero.save()

        data = {
            'codigo': bombero.user.username,
            'nombre': bombero.nombre,
            'apellido': bombero.apellido,
            'telefono': bombero.telefono,
        }

        return Response(data, status=200)

class ValidarTokenView(APIView):
    def post(self, request):
        token_data = request.data.get('token')
        token = Token.objects.filter(key=token_data).first()

        if token:
            user = token.user
            bombero = user.bombero.first()
            rol = bombero.get_rol_display()

            return Response({'user': user.username, 
                             'token': token.key, 
                            'rol': rol,
                             }, status=200)

        return Response({'error': 'Token invalido'}, status=400)

class AuthView(APIView):
    def post(self, request):
        user_data = request.data.get('user')
        password_data = request.data.get('password')

        user = authenticate(username=user_data, password=password_data)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            bombero = user.bombero.first()
            rol = bombero.get_rol_display()

            return Response({'user': user.username, 
                             'token': token.key, 
                            'rol': rol,
                             }, status=200)

        return Response({'error': 'Usuario o contraseña incorrectos'}, status=400)