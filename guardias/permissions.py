from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from bomberos.models import CategoriaBombero


class BomberoAdminAuthentication(TokenAuthentication):
    def authenticate(self, request):
        user, token = super().authenticate(request)

        if user.is_admin == False and user.is_super == False:
            raise AuthenticationFailed(
                "No tienes los permisos necesarios para acceder."
            )

        return user, token
    
class BomberoSuperAuthentication(TokenAuthentication):
    def authenticate(self, request):
        user, token = super().authenticate(request)

        if user.is_super == False:
            raise AuthenticationFailed(
                "No tienes los permisos necesarios para acceder."
            )
        
        return user, token
