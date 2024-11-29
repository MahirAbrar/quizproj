from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register our viewset
router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
urlpatterns = [
    path('', include(router.urls)), 
    path('login/', views.UserLoginApiView.as_view()),  
]