from django.contrib import admin
from django.urls import path, include

# Main URL configuration for the entire project
urlpatterns = [
    # admin interface
    path('admin/', admin.site.urls),
    # all API endpoints will start with /api/
    path('api/', include('api.urls')),
]