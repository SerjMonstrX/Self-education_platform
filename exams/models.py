from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Material

User = get_user_model()
NULLABLE = {'blank': True, 'null': True}


class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name='название теста')
    description = models.TextField(verbose_name='Описание теста', **NULLABLE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='exams', verbose_name='Материал')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams', verbose_name='Владелец')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name='Экзамен')
    text = models.TextField(verbose_name='Текст вопроса')
    is_multiple_choice = models.BooleanField(default=False, verbose_name='Множественный выбор')

    def __str__(self):
        return f'Вопрос {self.id} для {self.exam.title}'

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    text = models.CharField(max_length=500, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f'Ответ {self.id} для {self.question.text}'

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
