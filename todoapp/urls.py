from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', obtain_auth_token),
    # url(r'', include('api.api_urls'))
]
