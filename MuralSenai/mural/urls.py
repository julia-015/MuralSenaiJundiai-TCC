from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('inicio', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro/'),
    path('muralaviso', views.muralaviso, name='muralaviso'),
    path('carometro', views.carometro, name='carometro'),
    path('carometro2/<int:curso_id>/', views.carometro2, name='carometro2'),
    path('carometro3/<int:turma_id>/', views.carometro3, name='carometro3'),
    path('informacoescar/<int:aluno_id>/', views.informacoescar, name='informacoescar'),
    path('adicionarcurso', views.adicionarcurso, name='adicionarcurso'),
    path('adicionarturma', views.adicionarturma, name='adicionarturma'),
    path('adicionaraluno', views.adicionaraluno, name='adicionaraluno'),
    path('editarcurso/<int:curso_id>/', views.editarcurso, name='editarcurso'),
    path('editarturma/<int:turma_id>/', views.editarturma, name='editarturma'),
    path('editaraluno/<int:aluno_id>/', views.editaraluno, name='editaraluno'),  # Adicionada a URL com ID
    path('criar-aviso/', views.criar_aviso_ajax, name='criar_aviso_ajax'),
    path('editaraviso/<int:aviso_id>/', views.editaraviso, name='editaraviso'),
    path('excluiraviso/<int:aviso_id>/', views.excluiraviso, name='excluiraviso'),
]