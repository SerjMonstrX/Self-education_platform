# Generated by Django 5.0.7 on 2024-07-24 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название раздела')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание раздела')),
                ('is_public', models.BooleanField(default=False, verbose_name='признак публичности')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'раздел',
                'verbose_name_plural': 'разделы',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название материалов')),
                ('content', models.TextField(verbose_name='содержимое материалов')),
                ('is_public', models.BooleanField(default=False, verbose_name='признак публичности')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.section', verbose_name='название раздела')),
            ],
            options={
                'verbose_name': 'материалы',
                'verbose_name_plural': 'материалы',
            },
        ),
    ]
