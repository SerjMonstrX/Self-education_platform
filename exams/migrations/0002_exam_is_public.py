# Generated by Django 5.0.7 on 2024-07-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='признак публичности'),
        ),
    ]
