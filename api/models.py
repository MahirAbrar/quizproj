from django.db import models
from django.contrib.auth.models import User

#Always singular class

class Quiz(models.Model):
    # Name of the Quiz
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    SELECT_WORD = 'word'
    
    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (SELECT_WORD, 'word'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default=SINGLE_CHOICE)

    
    def get_words(text):
        """
        Extracts all unique words from the question text.
        - Removes punctuation
        - Splits on whitespace
        - Preserves contractions and hyphenated words
        - Removes empty strings
        - Maintains original case
        
        Returns:
            list: List of unique words from the text
        """
        # First, handle special cases (contractions, hyphenated words)
        preserved_text = text
        # Split on whitespace
        words = preserved_text.split()
        
        # Clean up each word
        cleaned_words = []
        for word in words:
            # Remove punctuation from start and end, but preserve internal punctuation
            word = word.strip('.,!?()[]{}":;')
            
            # Skip empty strings or strings with only punctuation
            if word and not word.isspace():
                cleaned_words.append(word)
        
        # Remove duplicates while preserving order
        unique_words = []
        seen = set()
        for word in cleaned_words:
            if word.lower() not in seen:
                unique_words.append(word)
                seen.add(word.lower())
        
        return unique_words

    def __str__(self):
        return f"Question: {self.quiz.title}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
    