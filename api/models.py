from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"Question: {self.quiz.title}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
    

class WordAnswer(models.Model):
    question = models.ForeignKey(Question, related_name='word_answers', on_delete=models.CASCADE)
    correct_words = models.TextField() 

    def get_words_list(self):
        return [word.strip() for word in self.correct_words.split(',')]

    def set_words_list(self, words_list):
        self.correct_words = ','.join(words_list)

    def __str__(self):
        return f"Word Answer for {self.question}"