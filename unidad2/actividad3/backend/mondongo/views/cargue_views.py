from rest_framework import viewsets
from mondongo.serializers.cargue_serializer import Serializador_Cargue
from Api.models.cargue import Cargue
from rest_framework.filters import SearchFilter, OrderingFilter

class CargueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo del modelo Cargue.
    Proporciona:
    - GET /cargues/ (lista todos los cargues)
    - POST /cargues/ (crea un nuevo cargue)
    - GET /cargues/{id}/ (obtiene un cargue específico)
    - PUT /cargues/{id}/ (actualiza un cargue)
    - DELETE /cargues/{id}/ (elimina un cargue)
    """
    queryset = Cargue.objects.all()
    serializer_class = Serializador_Cargue
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['Placa_del_vehiculo', 'Tipo_de_carga']
    ordering_fields = ['created_at', 'Valor_del_cargue']
    ordering = ['-created_at']