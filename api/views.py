from rest_framework import viewsets
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer

# A viewset that will handle CRUD operations for Quiz model
class QuizViewSet(viewsets.ModelViewSet):
    # Query on potentially all Quiz objects
    queryset = Quiz.objects.all()
    # Specify which serializer class to use for converting to/from JSON
    serializer_class = QuizSerializer
    

class QuestionViewSet(viewsets.ModelViewSet):
   queryset = Question.objects.all() 
   serializer_class = QuestionSerializer

#    def create(self, request, *args, **kwargs):
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
       
#        # Create the question
#        question = Question.objects.create(
#            quiz_id=serializer.validated_data['quiz'].id,
#            text=serializer.validated_data['text'],
#            question_type=serializer.validated_data['question_type']
#        )

#        # Create choices for the question
#        choices_data = request.data.get('choices', [])
#        for choice_data in choices_data:
#            Choice.objects.create(
#                question=question,
#                answer=choice_data['answer'],
#                is_correct=choice_data['is_correct']
#            )

#        headers = self.get_success_headers(serializer.data)
#        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)