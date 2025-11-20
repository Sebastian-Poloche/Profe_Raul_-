from rest_framework import viewsets
from ch_sp.serializers.herramientas_serializer import Serializador_Herramientas
from api.models.herramientas import Herramientas
from rest_framework.filters import SearchFilter, OrderingFilter

class Herramientas_ViewSet(viewsets.ModelViewSet):
    queryset = Herramientas.objects.all()
    serializer_class = Serializador_Herramientas
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['codigo', 'nombre']
    ordering_fields = ['created_at', 'categoria']
    ordering = ['-created_at']