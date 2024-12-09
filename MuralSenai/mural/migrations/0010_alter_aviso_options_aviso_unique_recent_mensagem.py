# Generated by Django 5.1.3 on 2024-12-05 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mural', '0009_alter_aaluno_options_alter_acurso_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aviso',
            options={},
        ),
        migrations.AddConstraint(
            model_name='aviso',
            constraint=models.UniqueConstraint(condition=models.Q(('data_criacao__gte', datetime.datetime(2024, 12, 5, 11, 20, 1, 90912, tzinfo=datetime.timezone.utc))), fields=('mensagem',), name='unique_recent_mensagem'),
        ),
    ]