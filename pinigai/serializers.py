from rest_framework import serializers
from .models import CustomUser

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'vardas', 'pareigos', 'email', 'username']

       