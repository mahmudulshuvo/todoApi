# from django.contrib.auth.models import User
# from .serializers import UserSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, viewsets
#
#
# class User(viewsets.ViewSet):
#     """
#     List all snippets, or create a new snippet.
#     """
#     # def get(self, request):
#     #     users = User.objects.all()
#     #     serializer = UserSerializer(users, many=True)
#     #     return Response(serializer.data)
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.create(serializer.initial_data)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)