# Generated by Django 5.1.3 on 2024-11-12 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mural', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aturma',
            name='curso',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mural.acurso'),
            preserve_default=False,
        ),
    ]
