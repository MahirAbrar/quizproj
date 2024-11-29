from rest_framework import serializers
from .models import Quiz, Choice, Question

#A quiz can have 0 or more questions.
#A question can have 2 or more choices.
#A choice can only belong to one question.

# all potential answers for a question
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'answer', 'is_correct']



class QuestionSerializer(serializers.ModelSerializer):
    # Add source='choice_set' to tell Django where to find the choices. FK makes it be referenced as choice_set

    choices = ChoiceSerializer(many=True, source='choice_set' ,required=True)
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'question_type', 'choices']

    def create(self, validated_data):
        if validated_data['question_type'] == Question.SELECT_WORD:
            choices_data = validated_data.pop('choice_set')
            
            # Create question without the choices data
            question = Question.objects.create(**validated_data)
            
            # Get the correct word from choices_data
            correct_words = [choice['answer'] for choice in choices_data if choice['is_correct']]
            if not correct_words:
                raise serializers.ValidationError(
                    'At least one correct word must be provided for select word questions.'
                )
            # Get all words from text
            words = Question.get_words(validated_data['text'])
            
            # Create a Choice object for each word
            for word in words:
                Choice.objects.create(
                    question=question,
                    answer=word,
                    is_correct=(word in correct_words)  
                )
        else:
        #     # # For single and multiple choice questions
            choices_data = validated_data.pop('choice_set')
            question = Question.objects.create(**validated_data)
            
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
                
        return question

    # # overwrite the default validate method to add custom validation
    def validate(self, data):
        choices = data['choice_set']  
        if data['question_type'] == Question.SELECT_WORD:
            question_text = data['text'].lower()
            for choice in choices:
                if choice['is_correct'] and choice['answer'].lower() not in question_text:
                    raise serializers.ValidationError(
                        f'Word "{choice["answer"]}" is not found in the question text.'
                    )
            
        # Validate that single choice questions only have one correct answer
        elif data['question_type'] == Question.SINGLE_CHOICE:
            count = 0  

            for choice in choices:
                if choice['is_correct']:
                    count += 1
                if count > 1:
                    raise serializers.ValidationError(
                        'Single choice questions can maximum of one correct answer.'
                    )
            if count == 0:
                raise serializers.ValidationError(
                    'Single choice questions must have one correct answer.'
                )
    
           
        
        else:
            if len(choices) < 2:
                raise serializers.ValidationError(
                    'Questions must have at least 2 choices.'
                )
            for choice in choices:
                if choice['is_correct']:
                    return data
            raise serializers.ValidationError(
                'Multiple choice questions must have at least one correct answer.'
            )
            
        return data

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True) #Read_only allows for 0 questions
    class Meta:
        # Quiz model from models.py
        model = Quiz
        # List which fields to include in the JSON output
        fields = ['id', 'title', 'description', 'questions']


