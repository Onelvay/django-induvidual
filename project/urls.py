from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blogs.urls')),  # Здесь исправляем 'blog' на 'blogs'
    path('users/', include('users.urls')),
]
