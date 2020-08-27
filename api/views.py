from django.shortcuts import render
import uuid
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer, TaskSerializer
from rest_framework.response import Response
from .models import Task
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, logout


# Create your views here.


# ViewSets define the view behavior.
class UserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        try:
            user = user_serializer.create(user_serializer.initial_data)
            return Response({"id": user.id, "username": user.username}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Request failed because "+str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            if self.request.user.is_anonymous:
                return Response("Annonymous user", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"id": self.request.user.id, "username": self.request.user.username},
                                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return


# ViewSets define the view behavior.
class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def jwt(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response("Username or password required", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=user.username, password=password)

            if not user:
                return Response("Unable to login, invalid password", status=status.HTTP_400_BAD_REQUEST)

            return Response({"id": user.id, "username": user.username, "jwt": self.jwt(user)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Request failed because "+str(e), status=status.HTTP_400_BAD_REQUEST)


# ViewSets define the view behavior.
class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            # Anonymous is not allowed
            if self.request.user.is_anonymous:
                return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)

            # change the user's jwt_secret
            user = self.request.user
            user.jwtsecret.jwt_secret = uuid.uuid4()
            user.save()

            # Removes the authenticated user's ID from the request, if available
            logout(self.request)
            return Response("Logged out", status=status.HTTP_200_OK)

        except Exception as e:
            return Response("Request failed because "+str(e), status=status.HTTP_400_BAD_REQUEST)



class TaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, )

    def get(self, request):
        try:
            if request.user.is_anonymous:
                return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)

            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response({"tasks": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response("Failed "+str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if request.user.is_anonymous:
                return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)
            task = request.data.get('task')
            task_serializer = TaskSerializer(data=task)
            if task_serializer.is_valid(raise_exception=True):
                task_saved = task_serializer.create(task, request.user)
            return Response({"id": task_saved.id, "title": task_saved.title, "completed": task_saved.completed, "user_id": task_saved.user_id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response("Failed " + str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            if request.user.is_anonymous:
                return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)

            saved_task = get_object_or_404(Task.objects.all(), pk=pk)
            if saved_task.user == request.user:
                serializer = TaskSerializer(instance=saved_task, data=request.data.get('task'), partial=True)
                if serializer.is_valid(raise_exception=True):
                    task_saved = serializer.save()
                return Response({"id": task_saved.id, "title": task_saved.title, "completed": task_saved.completed}, status=status.HTTP_200_OK)
            else:
                return Response("User is not allowed to change the task ",status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response("Failed " + str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = get_object_or_404(Task.objects.all(), pk=pk)
            if task.user == request.user:
                task.delete()
                return Response("Task deleted", status=204)
            else:
                return Response("User is not allowed to delete the task ", status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response("Failed " + str(e), status=status.HTTP_400_BAD_REQUEST)
