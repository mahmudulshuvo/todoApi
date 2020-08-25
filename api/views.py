from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer, TaskSerializer
from rest_framework.response import Response
from .models import Task
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

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


class TaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, )

    def get(self, request):
        if request.user.is_anonymous:
            return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_anonymous:
            return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)

        task = {
            'title': request.data.get('title'),
            'completed': request.data.get('completed'),
        }

        task_serializer = TaskSerializer(data=task)
        if task_serializer.is_valid(raise_exception=True):
            task_saved = task_serializer.create(task, request.user)
        return Response({"id": task_saved.id, "title": task_saved.title, "completed": task_saved.completed, "user_id": task_saved.user_id}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        if request.user.is_anonymous:
            return Response("Anonymous user", status=status.HTTP_400_BAD_REQUEST)

        saved_task = get_object_or_404(Task.objects.all(), pk=pk)
        if saved_task.user == request.user:
            data = request.data.get('task')
            serializer = TaskSerializer(instance=saved_task, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                task_saved = serializer.save()
            return Response({"id": task_saved.id, "title": task_saved.title, "completed": task_saved.completed}, status=status.HTTP_200_OK)
        else:
            return Response("User is not allowed to change the task ",status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        # Get object with this pk
        task = get_object_or_404(Task.objects.all(), pk=pk)
        if task.user == request.user:
            task.delete()
            return Response("Task deleted", status=204)
        else:
            return Response("User is not allowed to delete the task ", status=status.HTTP_403_FORBIDDEN)
