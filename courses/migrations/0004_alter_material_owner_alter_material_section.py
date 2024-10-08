# Generated by Django 5.0.7 on 2024-07-24 18:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_section_is_public'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AlterField(
            model_name='material',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.section', verbose_name='название раздела'),
        ),
    ]
