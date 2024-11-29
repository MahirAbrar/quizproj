from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router instance
router = DefaultRouter()
# Register QuizViewSet so we can route in /quizzes
# GET /quizzes/ - list all quizzes
# POST /quizzes/ - create a new quiz
# GET /quizzes/{id}/ - get a specific quiz
# PUT /quizzes/{id}/ - update a specific quiz
# DELETE /quizzes/{id}/ - delete a specific quiz
router.register(r'quizzes', views.QuizViewSet)
router.register(r'questions', views.QuestionViewSet)

# Create the URL patterns
urlpatterns = [
    # Include all the URLs created by the router
    path('', include(router.urls)),
]