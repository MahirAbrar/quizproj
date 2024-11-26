from rest_framework import serializers
from .models import Quiz

#Serializer convert Quiz model instances to JSON and vice versa
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        # Quiz model from models.py
        model = Quiz
        # List which fields to include in the JSON output
        fields = ['id', 'title', 'description']