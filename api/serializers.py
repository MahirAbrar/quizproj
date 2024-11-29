from rest_framework import serializers
from .models import Quiz, Choice, Question, QuizAttempt

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
    questions = QuestionSerializer(many=True, read_only=True, source='question_set') #Read_only allows for 0 questions
    class Meta:
        # Quiz model from models.py
        model = Quiz
        # List which fields to include in the JSON output
        fields = ['id', 'title', 'description', 'questions']





#Quiz attemps
class QuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['quiz', 'answers']

    def validate_answers(self, answers):
        """
        Validate answer format and question types
        answers format: {
            "question_id": [choice_ids]
        }
        """
        if not isinstance(answers, dict):
            raise serializers.ValidationError("Answers must be a dictionary")

        for question_id, selected_choices in answers.items():
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                raise serializers.ValidationError(f"Question {question_id} does not exist")

            # Validate selected choices exist for this question
            valid_choice_ids = set(question.choice_set.values_list('id', flat=True))
            invalid_choices = [c for c in selected_choices if c not in valid_choice_ids]
            if invalid_choices:
                raise serializers.ValidationError(f"Invalid choices for question {question_id}: {invalid_choices}")

            # Validate based on question type
            if question.question_type == 'single' and len(selected_choices) != 1:
                raise serializers.ValidationError(f"Question {question_id} requires exactly one answer")
            elif not selected_choices:
                raise serializers.ValidationError(f"No answers provided for question {question_id}")

        return answers

    def create(self, validated_data):
        attempt = QuizAttempt.objects.create(**validated_data)
        attempt.calculate_score()  # Calculate and save score
        return attempt