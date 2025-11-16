from django.shortcuts import render
from rest_framework import viewsets
from herramientas.models import Herramientas
from herramientas.serializers import Herramientas_Serializada
# Create your views here.

class Visualizador_Herramienta(viewsets.ModelViewSet):
    queryset = Herramientas.objects.all()
    serializer_class = Herramientas_Serializada