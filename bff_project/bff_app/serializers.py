from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'sub', 'username', 'first_name', 'last_name', 'email', 'user_id')
