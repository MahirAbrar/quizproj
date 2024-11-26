from rest_framework import viewsets
from .models import Quiz
from .serializers import QuizSerializer

# A viewset that will handle CRUD operations for Quiz model
class QuizViewSet(viewsets.ModelViewSet):
    # Query on potentially all Quiz objects
    queryset = Quiz.objects.all()
    # Specify which serializer class to use for converting to/from JSON
    serializer_class = QuizSerializer
    http_method_names = ['get', 'post', 'put', 'delete']