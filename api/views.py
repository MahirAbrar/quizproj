from rest_framework import viewsets
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

# A viewset that will handle CRUD operations for Quiz model
class QuizViewSet(viewsets.ModelViewSet):
    # Query on potentially all Quiz objects
    queryset = Quiz.objects.all()
    # Specify which serializer class to use for converting to/from JSON
    serializer_class = QuizSerializer
    

class QuestionViewSet(viewsets.ModelViewSet):
   queryset = Question.objects.all() 
   serializer_class = QuestionSerializer


