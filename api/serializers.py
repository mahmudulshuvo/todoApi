# Serializers define the API representation.
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User()
        user.username = validated_data.get('username')
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    completed = serializers.BooleanField()

    def create(self, validated_data, user):
        task = Task()
        task.user = user
        task.title = validated_data.get('title')
        task.completed = validated_data.get('completed')
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.user_id = validated_data.get('user_id', instance.user_id)

        instance.save()
        return instance

