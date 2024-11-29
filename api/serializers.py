from rest_framework import serializers
from .models import Quiz, Choice, Question, WordAnswer

#Serializer convert instances to JSON and vice versa and allows for post requests

#A quiz can have 0 or more questions.
#A question can have 2 or more choices.
#A choice can only belong to one question.

# all potential answers for a question
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'answer', 'is_correct']

class WordAnswerSerializer(serializers.ModelSerializer):
    correct_words = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        model = WordAnswer
        fields = ['id', 'correct_words']

    def validate(self, data):
        # Get the question text from the parent serializer's context
        question_text = self.context.get('question_text', '').lower()
        
        # Validate each word exists in the question text
        for word in data['correct_words']:
            if word.lower() not in question_text:
                raise serializers.ValidationError(
                    f'Word "{word}" is not found in the question text.'
                )
        return data



class QuestionSerializer(serializers.ModelSerializer):
    # Add source='choice_set' to tell Django where to find the choices. FK makes it be referenced as choice_set
    choices = ChoiceSerializer(many=True, source='choice_set', required=False, default=list)
    word_answer = WordAnswerSerializer(required=False)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'question_type', 'choices', 'word_answer']

    def create(self, validated_data):
        if validated_data['question_type'] == Question.SELECT_WORD:
            # Pop word_answers data before creating question
            word_answers_data = validated_data.pop('word_answers', [])
            question = Question.objects.create(**validated_data)
            
            # Pass question text to WordAnswerSerializer for validation
            for word_answer in word_answers_data:
                serializer = WordAnswerSerializer(
                    data=word_answer,
                    context={'question_text': validated_data['text']}
                )
                if serializer.is_valid():
                    WordAnswer.objects.create(
                        question=question,
                        correct_words=','.join(serializer.validated_data['correct_words'])
                    )
            return question
        else:
            # For single and multiple choice questions
            choices_data = validated_data.pop('choice_set')
            question = Question.objects.create(**validated_data)
            
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
                
            return question

    
    # overwrite the default validate method to add custom validation
    def validate(self, data):
        if data['question_type'] == Question.SELECT_WORD:
            if 'word_answers' not in self.initial_data: 
                raise serializers.ValidationError(
                    'Word selection questions must have at least 1 correct answers specified.'
                )
            
        # Validate that single choice questions only have one correct answer
        elif data['question_type'] == Question.SINGLE_CHOICE:
            choices = data['choice_set']    
            if data['question_type'] == Question.SINGLE_CHOICE:
                count = 0
                for choice in choices:
                    if choice['is_correct']:
                        count += 1
                    if count > 1:
                        raise serializers.ValidationError(
                            'Single choice questions can only have one correct answer.'
                        )
           
        
        # # Validate that questions have at least 2 choices 
        else:
            if len(choices) < 2:
                raise serializers.ValidationError(
                    'Questions must have at least 2 choices.'
                )
        return data

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True) #Read_only allows for 0 questions
    class Meta:
        # Quiz model from models.py
        model = Quiz
        # List which fields to include in the JSON output
        fields = ['id', 'title', 'description', 'questions']


