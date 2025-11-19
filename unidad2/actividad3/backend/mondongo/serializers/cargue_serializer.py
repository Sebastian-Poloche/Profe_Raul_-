from rest_framework import serializers
from Api.models.cargue import Cargue

class Serializador_Cargue(serializers.ModelSerializer):
    class Meta:
        model = Cargue
        exclude = ['created_at']