from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserView, TaskView, LoginViewSet, LogoutView

router = routers.DefaultRouter()
router.register(r'login', LoginViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>', TaskView.as_view())

]
