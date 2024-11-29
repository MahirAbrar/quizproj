from rest_framework import viewsets
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizSubmissionSerializer
from .models import QuizAttempt


# A viewset that will handle CRUD operations for Quiz model
class QuizViewSet(viewsets.ModelViewSet):
    # Query on potentially all Quiz objects
    queryset = Quiz.objects.all()
    # Specify which serializer class to use for converting to/from JSON
    serializer_class = QuizSerializer
    

class QuestionViewSet(viewsets.ModelViewSet):
   queryset = Question.objects.all() 
   serializer_class = QuestionSerializer


class QuizSubmissionView(APIView):
    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)

        # Add quiz to the data
        data = {
            'quiz': quiz_id,
            'answers': request.data.get('answers', {})
        }

        serializer = QuizSubmissionSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        attempt = serializer.save()
        
        return Response({
            'score': attempt.score,
            'message': f"You scored {attempt.score}%"
        })