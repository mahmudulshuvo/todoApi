from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer
from rest_framework.response import Response

# Create your views here.


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        try:
            user = user_serializer.create(user_serializer.initial_data)
            return Response({"id": user.id, "username": user.username}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Request failed because "+str(e), status=status.HTTP_400_BAD_REQUEST)
