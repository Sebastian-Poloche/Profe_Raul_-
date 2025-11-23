from rest_framework import viewsets
from ch_sp.serializers.prestamos_serializer import Serializador_Prestamos
from api.models.prestamos import Prestamos
from rest_framework.filters import SearchFilter, OrderingFilter

class Prestamos_ViewSet(viewsets.ModelViewSet):
    queryset = Prestamos.objects.all()
    serializer_class = Serializador_Prestamos
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['numero']
    ordering_fields = ['created_at']
    ordering = ['-created_at']