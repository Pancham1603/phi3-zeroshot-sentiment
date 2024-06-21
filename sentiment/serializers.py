from rest_framework import serializers
from .models import Chat, ChatInstance
from django.contrib.auth.models import User

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class ChatInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInstance
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'