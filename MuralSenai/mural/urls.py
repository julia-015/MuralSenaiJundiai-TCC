from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('inicio', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro/'),
    path('muralaviso', views.muralaviso, name='muralaviso'),
    path('carometro', views.carometro, name='carometro'),
    path('carometro2/<int:curso_id>/', views.carometro2, name='carometro2'),
    path('carometro3/<str:turma_id>/', views.carometro3, name='carometro3'),
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
    path('excluircurso/<int:curso_id>/', views.excluircurso, name='excluircurso'),
    path('excluirturma/<int:turma_id>/', views.excluirturma, name='excluirturma'),
    path('excluiraluno/<int:aluno_id>/', views.excluiraluno, name='excluiraluno'),
    path('uploadfoto/<int:aluno_id>/', views.upload_foto, name='uploadfoto'),  # Nova rota para upload de fotos
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
