from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register our viewset
router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, basename='profile')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),  # This should work now
    path('login/', views.UserLoginApiView.as_view()),  # This is fine as is
]