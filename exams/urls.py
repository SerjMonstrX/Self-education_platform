from django.urls import path
from .views import (
    ExamCreateAPIView, ExamListAPIView, ExamDetailAPIView,
    ExamUpdateAPIView, ExamDeleteAPIView, QuestionCreateAPIView, QuestionListAPIView, QuestionDetailAPIView,
    QuestionUpdateAPIView, QuestionDeleteAPIView, AnswerCreateAPIView, AnswerListAPIView, AnswerDetailAPIView,
    AnswerUpdateAPIView, AnswerDeleteAPIView, SubmitExamAPIView
)

urlpatterns = [
    path('create/', ExamCreateAPIView.as_view(), name='exam-create'),
    path('', ExamListAPIView.as_view(), name='exam-list'),
    path('<int:pk>/', ExamDetailAPIView.as_view(), name='exam-detail'),
    path('<int:pk>/update/', ExamUpdateAPIView.as_view(), name='exam-update'),
    path('<int:pk>/delete/', ExamDeleteAPIView.as_view(), name='exam-delete'),

    path('questions/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='question-detail'),
    path('questions/<int:pk>/update/', QuestionUpdateAPIView.as_view(), name='question-update'),
    path('questions/<int:pk>/delete/', QuestionDeleteAPIView.as_view(), name='question-delete'),

    path('answers/create/', AnswerCreateAPIView.as_view(), name='answer-create'),
    path('answers/', AnswerListAPIView.as_view(), name='answer-list'),
    path('answers/<int:pk>/', AnswerDetailAPIView.as_view(), name='answer-detail'),
    path('answers/<int:pk>/update/', AnswerUpdateAPIView.as_view(), name='answer-update'),
    path('answers/<int:pk>/delete/', AnswerDeleteAPIView.as_view(), name='answer-delete'),

    path('exams/<int:pk>/submit/', SubmitExamAPIView.as_view(), name='exam-submit'),
]