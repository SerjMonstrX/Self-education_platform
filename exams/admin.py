from django.contrib import admin

from exams.models import Exam, Question, Answer


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'description')
    list_filter = ('owner',)
    search_fields = ('owner', 'title')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'text')
    list_filter = ('exam', 'text')
    search_fields = ('exam', 'text')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text')
    list_filter = ('question',)
    search_fields = ('question', 'text')