from django.urls import path
from .views import (
    ExamCreateAPIView, ExamListAPIView, ExamDetailAPIView,
    ExamUpdateAPIView, ExamDeleteAPIView
)

urlpatterns = [
    path('create/', ExamCreateAPIView.as_view(), name='exam-create'),
    path('', ExamListAPIView.as_view(), name='exam-list'),
    path('<int:pk>/', ExamDetailAPIView.as_view(), name='exam-detail'),
    path('<int:pk>/update/', ExamUpdateAPIView.as_view(), name='exam-update'),
    path('<int:pk>/delete/', ExamDeleteAPIView.as_view(), name='exam-delete'),
]