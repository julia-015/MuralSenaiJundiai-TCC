# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AAluno, Cadastro, ACurso, Login, ATurma

class FormLogin(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class FormCadastro(forms.Form):
    nome = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    PROFISSAO_CHOICES = [
        ('coordenador', 'Coordenador'),
        ('colaborador', 'Colaborador'),
    ]
    profissao = forms.ChoiceField(choices=PROFISSAO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    criarsenha = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class FormAluno(forms.ModelForm):
    class Meta:
        model = AAluno
        fields = ['nome', 'telefone', 'nome_pai', 'nome_mae', 'turma', 'foto','observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_pai': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'fotos':forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
class FormCurso(forms.Form):
    curso = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ACurso
        fields = ['curso']  # Inclua todos os campos que deseja editar

class FormTurma(forms.ModelForm):
    class Meta:
        model = ATurma
        fields = ['turma', 'periodo', 'curso']  # Campos que você deseja editar
        widgets = {
            'turma': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.TextInput(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
        }