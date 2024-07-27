from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Exam, Question, Answer
from .serializers import ExamSerializer, QuestionSerializer, AnswerSerializer
from courses.permissions import IsOwner, IsModerator


class ExamCreateAPIView(generics.CreateAPIView):
    """
    API для создания экзамена.
    Позволяет владелецам материала создавать экзамены для него.
    """
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        material = serializer.validated_data['material']
        if material.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого материала.")
        serializer.save(owner=self.request.user)


class ExamListAPIView(generics.ListAPIView):
    """
    API для получения списка экзаменов.
    Возвращает экзамены, принадлежащие аутентифицированному пользователю, или публичные экзамены.
    """
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Exam.objects.filter(Q(material__owner=user) | Q(is_public=True))
        else:
            return Exam.objects.filter(is_public=True)


class ExamDetailAPIView(generics.RetrieveAPIView):
    """
    API для получения информации об одном экзамене.
    Доступно только владельцу или модераторам.
    """
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class ExamUpdateAPIView(generics.UpdateAPIView):
    """
    API для обновления экзамена.
    Обновлять экзамен могут только владелец или модераторы.
    """
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        exam_id = self.kwargs['pk']
        exam = Exam.objects.get(pk=exam_id)
        if exam.owner == user or user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот раздел.")


class ExamDeleteAPIView(generics.DestroyAPIView):
    """
    API для удаления экзамена.
    Удалять экзамен могут только владелец или модераторы.
    """
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class QuestionCreateAPIView(generics.CreateAPIView):
    """
    API для создания вопроса.
    Позволяет аутентифицированным пользователям создавать вопросы для их экзаменов.
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        exam = serializer.validated_data['exam']
        if exam.material.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого материала.")
        serializer.save()


class QuestionListAPIView(generics.ListAPIView):
    """
    API для получения списка вопросов.
    Возвращает вопросы, принадлежащие аутентифицированному пользователю, или публичные вопросы.
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Question.objects.filter(Q(exam__material__owner=user) | Q(exam__is_public=True))
        else:
            return Question.objects.filter(exam__is_public=True)


class QuestionDetailAPIView(generics.RetrieveAPIView):
    """
    API для получения информации об одном вопросе.
    Доступно только владельцу или модераторам.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class QuestionUpdateAPIView(generics.UpdateAPIView):
    """
    API для обновления вопроса.
    Обновлять вопрос могут только владелец или модераторы.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        question = self.get_object()
        if question.exam.material.owner == user or user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот вопрос.")


class QuestionDeleteAPIView(generics.DestroyAPIView):
    """
    API для удаления вопроса.
    Удалять вопрос могут только владелец или модераторы.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class AnswerCreateAPIView(generics.CreateAPIView):
    """
    API для создания ответа.
    Позволяет аутентифицированным пользователям создавать ответы на вопросы в их экзаменах.
    """
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        if question.exam.material.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого материала.")
        serializer.save()


class AnswerListAPIView(generics.ListAPIView):
    """
    API для получения списка ответов.
    Возвращает ответы, принадлежащие аутентифицированному пользователю, или публичные ответы.
    """
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Answer.objects.filter(Q(question__exam__material__owner=user) | Q(question__exam__is_public=True))
        else:
            return Answer.objects.filter(question__exam__is_public=True)


class AnswerDetailAPIView(generics.RetrieveAPIView):
    """
    API для получения информации об одном ответе.
    Доступно только владельцу или модераторам.
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class AnswerUpdateAPIView(generics.UpdateAPIView):
    """
    API для обновления ответа.
    Обновлять ответ могут только владелец или модераторы.
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        answer = self.get_object()
        if answer.question.exam.material.owner == user or user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот ответ.")


class AnswerDeleteAPIView(generics.DestroyAPIView):
    """
    API для удаления ответа.
    Удалять ответ могут только владелец или модераторы.
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class SubmitExamAPIView(APIView):
    """
    API для отправки экзамена.
    Аутентифицированные пользователи могут отправить свои ответы и получить оценку.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        exam = Exam.objects.get(pk=pk)
        user_answers = request.data.get('answers')

        # Логика проверки ответов
        correct_answers = 0
        total_questions = exam.questions.count()

        for question in exam.questions.all():
            correct_answer = question.answers.filter(is_correct=True).first()
            user_answer = user_answers.get(str(question.id))
            if correct_answer and user_answer == correct_answer.id:
                correct_answers += 1

        score = (correct_answers / total_questions) * 100
        return Response({'score': score, 'correct_answers': correct_answers, 'total_questions': total_questions}, status=status.HTTP_200_OK)
