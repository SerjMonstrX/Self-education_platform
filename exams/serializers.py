from rest_framework import serializers
from .models import Exam, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'is_multiple_choice', 'answers']


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'material', 'questions', 'is_public']
        read_only_fields = ['owner']

    def update(self, instance, validated_data):
        validated_data['material'] = instance.material
        return super().update(instance, validated_data)
