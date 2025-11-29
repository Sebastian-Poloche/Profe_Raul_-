"""
URL configuration for ch_sp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.herramientas_views import Herramientas_ViewSet
from .views.prestamos_views import Prestamos_ViewSet


router = DefaultRouter()
router.register(r'herramientas', Herramientas_ViewSet, basename='herramientas')
router.register(r'prestamos', Prestamos_ViewSet, basename='prestamos')

app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]