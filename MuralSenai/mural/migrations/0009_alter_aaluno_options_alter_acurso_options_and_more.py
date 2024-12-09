# Generated by Django 5.1.3 on 2024-12-03 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mural', '0008_aaluno_foto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aaluno',
            options={},
        ),
        migrations.AlterModelOptions(
            name='acurso',
            options={'permissions': [('can_add_courses', 'Pode adicionar cursos'), ('can_edit_courses', 'Pode editar cursos'), ('can_delete_courses', 'Pode excluir cursos')]},
        ),
        migrations.AlterModelOptions(
            name='aviso',
            options={'permissions': [('can_add_aviso', 'Pode adicionar avisos'), ('can_edit_aviso', 'Pode editar avisos'), ('can_delete_aviso', 'Pode excluir avisos')]},
        ),
        migrations.AlterField(
            model_name='aaluno',
            name='nome_mae',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aaluno',
            name='nome_pai',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aaluno',
            name='telefone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='aaluno',
            name='turma',
            field=models.CharField(max_length=100),
        ),
    ]