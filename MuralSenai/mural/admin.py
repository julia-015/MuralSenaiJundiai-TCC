from django.contrib import admin
from .models import AAluno, Cadastro, ACurso, ATurma, AAluno

admin.site.register(AAluno)
admin.site.register(Cadastro)
admin.site.register(ACurso)
admin.site.register(ATurma)