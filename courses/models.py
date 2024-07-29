from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
NULLABLE = {'blank': True, 'null': True}


class Section(models.Model):
    title = models.CharField(max_length=200, verbose_name='название раздела')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец')
    description = models.TextField(verbose_name='Описание раздела', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'


class Material(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='название раздела', related_name='materials')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', related_name='materials')
    title = models.CharField(max_length=200, verbose_name='название материалов')
    content = models.TextField(verbose_name='содержимое материалов')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'{self.title} из раздела {self.section}'

    class Meta:
        verbose_name = 'материалы'
        verbose_name_plural = 'материалы'
