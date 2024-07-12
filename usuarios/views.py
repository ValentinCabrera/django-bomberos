from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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