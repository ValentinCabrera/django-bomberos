"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bomberos.views import LoginAPIView, TokenVerify, AdminVerify, SuperVerify, SuperListPersonal
from guardias.views import (
    UserUpdateGuardia,
    UserOpenGuardia,
    UserListGuardias,
    AdminGuardiasAbiertas,
    AdminGuardiasCerradas,
    UserAddDetalle,
    UserRemoveDetalle,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginAPIView.as_view()),
    path("guardia/update/", UserUpdateGuardia.as_view()),
    path("guardia/open/", UserOpenGuardia.as_view()),
    path("guardia/listar/", UserListGuardias.as_view()),
    path("guardias/admin/abiertas/", AdminGuardiasAbiertas.as_view()),
    path("guardias/admin/revisar/", AdminGuardiasCerradas.as_view()),
    path("auth/", TokenVerify.as_view()),
    path("auth/admin", AdminVerify.as_view()),
    path("auth/super", SuperVerify.as_view()),
    path("guardia/detalle/add/", UserAddDetalle.as_view()),
    path("guardia/detalle/rm/", UserRemoveDetalle.as_view()),
    path("super/list/bomberos/", SuperListPersonal.as_view()),
]
