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

from usuarios.views import AuthView, ValidarTokenView, BomberoView
from guardias.views import MisGuardiasView, HorasAcumuladasView, GuardiaView, GuardiaActivaAdminView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", AuthView.as_view()),
    path("guardias/mis-guardias/", MisGuardiasView.as_view()),
    path("guardias/horas-acumuladas/", HorasAcumuladasView.as_view()),
    path("guardias/guardia-actual/", GuardiaView.as_view()),
    path("validar-token/", ValidarTokenView.as_view()),
    path("guardias/admin/guardias-activas/", GuardiaActivaAdminView.as_view()),
    path("usuarios/bomberos/", BomberoView.as_view()),
]
