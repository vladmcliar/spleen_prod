from rest_framework import serializers
from django.contrib.auth.models import User
from journal.models import Emotion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'user', 'emotion', 'description', 'timestamp']
        read_only_fields = ['user', 'timestamp']

    def create(self, validated_data):
        emotion = Emotion.objects.create(**validated_data)
        return emotion