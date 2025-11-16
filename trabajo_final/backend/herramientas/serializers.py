from rest_framework import serializers
from herramientas.models import Herramientas

class Herramientas_Serializada(serializers.ModelSerializer):
    class Meta:
        model = Herramientas
        fields = ['id', 'codigo', 'nombre', 'categoria', ' ubicacion', 'created_at', 'updated_at']