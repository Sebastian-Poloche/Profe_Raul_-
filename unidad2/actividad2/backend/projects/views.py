from rest_framework import viewsets
from projects.models import Project_cargues
from projects.serializers import ProductoSerializer

# Create your views here.

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Project_cargues.objects.all()
    serializer_class = ProductoSerializer
