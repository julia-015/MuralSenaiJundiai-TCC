from django.db import models
from django.contrib.auth.hashers import make_password



class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100, default='default_password')

    def __str__(self):
        return self.username

class Cadastro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    PROFISSAO_CHOICES = [
        ('coordenador', 'Coordenador'),
        ('colaborador', 'Colaborador'),
    ]
    profissao = models.CharField(max_length=50, choices=PROFISSAO_CHOICES)
    criarsenha = models.TextField(max_length=1000)

    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)

    class Meta:
        permissions =[
            ("can_add_cadastro", "Pode adicionar alunos")
            
        ]

    def __str__(self):
        return self.nome


class ACurso(models.Model):
    curso = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_add_courses", "Pode adicionar cursos"),
            ("can_edit_courses", "Pode editar cursos"),
            ("can_delete_courses", "Pode excluir cursos")
        ]
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.curso

class ATurma(models.Model):
    turma = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    curso = models.ForeignKey(ACurso, on_delete=models.CASCADE)  # Associação com ACurso

    class Meta:
        permissions =[
            ("can_add_turmas", "Pode adicionar turmas"),
            ("can_edit_turmas", "Pode editar turmas"),
            ("can_delte_turmas", "Pode excluir turmas")
            
        ]

    def __str__(self):
        return f"{self.turma} ({self.curso})"


class AAluno(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    nome_pai = models.CharField(max_length=100, default='Nao informado')
    nome_mae = models.CharField(max_length=100, default='Nao informado')
    turma = models.ForeignKey(ATurma, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        permissions =[
            ("can_add_alunos", "Pode adicionar alunos"),
            ("can_edit_alunos", "Pode editar alunos"),
            ("can_delte_alunoss", "Pode excluir alunos")
            
        ]

    def __str__(self):
        return self.nome


class Aviso(models.Model):
    mensagem = models.TextField("Mensagem de Aviso")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'mensagem': self.mensagem,
            'data_criacao': self.data_criacao.isoformat(),
        }

    def __str__(self):
        return f"Aviso - {self.data_criacao.strftime('%Y-%m-%d')}"
