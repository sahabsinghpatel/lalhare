from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('payments/', include('payments.urls')),
]
