
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import FormAluno, FormCadastro, FormLogin, FormCurso, FormTurma
from .models import AAluno, Cadastro, ACurso, ATurma, Aviso
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import connection

def homepage(request):
    if request.method == "POST":
        form = FormLogin(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('inicio')
            else:
                form.add_error(None, "Nome de usuário ou senha inválidos.")
    else:
        form = FormLogin()
    return render(request, 'homepage.html', {'form': form})

def inicio(request):
    context={}
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()
    context["is_coordenador"] = is_coordenador
    return render(request, 'telainicial.html', context)

@login_required
def cadastro(request):
    context = {}
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()
    if request.method == "POST":
        form = FormCadastro(request.POST)
        if form.is_valid():
            var_nome = form.cleaned_data['nome']
            var_email = form.cleaned_data['email']
            var_profissao = form.cleaned_data['profissao']
            var_criar_senha = form.cleaned_data['criarsenha']
            try:
                if User.objects.filter(email=var_email).exists():
                    context["error"] = "Este email já está cadastrado!"
                else:
                    # Criação do usuário no sistema de autenticação
                    novo_usuario = User.objects.create_user(
                        username=var_nome,
                        email=var_email,
                        password=var_criar_senha
                    )

                    # Associa o usuário a um grupo com base na profissão
                    if var_profissao.lower() == 'coordenador':
                        coordenador_group = Group.objects.get(name='Coordenador')
                        novo_usuario.groups.add(coordenador_group)
                    elif var_profissao.lower() == 'colaborador':
                        colaborador_group = Group.objects.get(name='Colaborador')
                        novo_usuario.groups.add(colaborador_group)

                    novo_usuario.save()  # Salva o usuário com o grupo associado

                    # Salva no modelo `Cadastro` se for necessário
                    novo_cadastro = Cadastro(
                        nome=var_nome,
                        email=var_email,
                        profissao=var_profissao,
                        criarsenha=var_criar_senha
                    )
                    novo_cadastro.save()

                    context["success"] = "Cadastro realizado com sucesso!"
                    form = FormCadastro()  # Reseta o formulário
            except Group.DoesNotExist:
                context["error"] = "Erro: O grupo associado não existe. Verifique sua configuração no Django Admin."
            except Exception as e:
                context["error"] = f"Ocorreu um erro: {str(e)}"
    else:
        form = FormCadastro()

    context["form"] = form
    context["is_coordenador"] = is_coordenador
    return render(request, 'cadastro.html', context)

@login_required
def carometro(request):
    # Ordena os cursos pelo campo 'curso'
    cursos = ACurso.objects.all().order_by('curso')

    # Verifica se o usuário é coordenador
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()

    # Passa os dados para o contexto
    context = {'cursos': cursos, 'is_coordenador': is_coordenador}
    return render(request, 'carometro.html', context)


@login_required
def carometro2(request, curso_id):
    # Filtra as turmas pelo curso e ordena pelo campo 'turma'
    turmas = ATurma.objects.filter(curso=curso_id).order_by('turma')

    # Verifica se o usuário é coordenador
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()

    # Passa os dados para o contexto
    context = {'turmas': turmas, 'is_coordenador': is_coordenador}
    return render(request, 'carometro2.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import AAluno

@login_required
def carometro3(request, turma_id):
    # Filtra os alunos pela turma e os ordena pelo nome
    alunos = AAluno.objects.filter(turma=turma_id).order_by('nome')
    
    # Verifica se o usuário é coordenador
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()

    # Passa os dados para o contexto
    context = {
        'alunos': alunos,
        'is_coordenador': is_coordenador
    }

    # Retorna o template com o contexto
    return render(request, 'carometro3.html', context)



def informacoescar(request, aluno_id):
    alunos = AAluno.objects.filter(id=aluno_id)
    context = {'alunos': alunos}
    return render(request, 'informacoescar.html', context)

def adicionarcurso(request):
    context = {}
    if request.method == "POST":
        form = FormCurso(request.POST)
        if form.is_valid():
            var_curso = form.cleaned_data['curso']
            try:
                if ACurso.objects.filter(curso=var_curso).exists():
                    context["error"] = "Curso já adicionado!"
                else:
                    user_curso = ACurso(curso=var_curso)
                    user_curso.save()
                    context["success"] = "Curso adicionado com sucesso!"
                    form = FormCurso()  
                    return redirect('carometro')
            except Exception as e:
                context["error"] = f"Ocorreu um erro: {str(e)}"
        context["form"] = form 
    else:
        form = FormCurso()
    context["form"] = form
    return render(request, 'adicionarcurso.html', context) 

# Edição e exclusão de Cursos
def editarcurso(request, curso_id):
    curso = get_object_or_404(ACurso, id=curso_id)

    if request.method == 'POST':  # Verifica se o método é POST
        novo_nome = request.POST.get('curso')  # Captura o novo nome do campo 'curso'
        if novo_nome:  # Verifica se o novo nome foi enviado
            curso.curso = novo_nome
            curso.save()  # Salva as alterações no banco de dados
            return redirect('carometro')  # Redireciona para a página do carômetro

    return render(request, 'editarcurso.html', {'curso': curso})

def excluircurso(request, curso_id):
    curso = get_object_or_404(ACurso, id=curso_id)
    if request.method == 'POST':
        # Obtenha as turmas associadas ao curso
        turmas = ATurma.objects.filter(curso=curso)
        for turma in turmas:
            # Excluir alunos manualmente usando SQL
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM mural_aaluno WHERE turma = %s", [turma.turma])
            
            # Exclua a turma
            turma.delete()

        # Exclua o curso após excluir as dependências
        curso.delete()
        return redirect('carometro')

    return render(request, 'carometro.html', {'curso': curso})
    
def adicionarturma(request):
    context = {}

    if request.method == "POST":
        form = FormTurma(request.POST)
        if form.is_valid():
            var_turma = form.cleaned_data['turma']
            var_periodo = form.cleaned_data['periodo']
            var_curso = form.cleaned_data['curso']  # Captura o curso selecionado
            try:
                if ATurma.objects.filter(turma=var_turma, curso=var_curso).exists():
                    context["error"] = "Essa turma já foi adicionada para o curso selecionado!"
                else:
                    user_turma = ATurma(turma=var_turma, periodo=var_periodo, curso=var_curso)
                    user_turma.save()
                    context["success"] = "Turma adicionada com sucesso!"
                    return redirect('carometro')
            except Exception as e:
                context["error"] = f"Ocorreu um erro: {str(e)}"
        context["form"] = form
    else:
        form = FormTurma()
        context["form"] = form
    return render(request, 'adicionarturma.html', context)

def editarturma(request, turma_id):
    turma = get_object_or_404(ATurma, id=turma_id)

    if request.method == 'POST':  # Verifica se o método é POST
        novo_nome = request.POST.get('turma')  # Nome da turma
        novo_periodo = request.POST.get('periodo')  # Período da turma

        # Atualiza a turma com os novos valores
        if novo_nome:
            turma.turma = novo_nome
        if novo_periodo:
            turma.periodo = novo_periodo

        turma.save()  # Salva as alterações no banco de dados
        return redirect('carometro')  # Redireciona para a página do carômetro

    return render(request, 'editarturma.html', {'turma': turma, 'cursos': ACurso.objects.all()})

def excluirturma(request, turma_id):
    turma = get_object_or_404(ATurma, id=turma_id)
    if request.method == 'POST':
        # Exclua todas as turmas associadas ao curso
        alunos = AAluno.objects.filter(turma=turma)
        for aluno in alunos:
            # Exclua todos os alunos associados à turma
            aluno.delete()
        
        # Após excluir dependências, exclua o curso
        turma.delete()        
        return redirect('inicio')
    return render(request, 'inicio.html')

def adicionaraluno(request):
    context = {}

    if request.method == "POST":
        form = FormAluno(request.POST, request.FILES)  # Inclusão de request.FILES
        if form.is_valid():
            var_nome = form.cleaned_data['nome']
            var_telefone = form.cleaned_data['telefone']
            var_nome_pai = form.cleaned_data['nome_pai']
            var_nome_mae = form.cleaned_data['nome_mae']
            var_turma = form.cleaned_data['turma']
            var_observacoes = form.cleaned_data.get('observacoes', '')
            var_foto = form.cleaned_data.get('foto')

            try:
                if AAluno.objects.filter(nome=var_nome, turma=var_turma).exists():
                    context["error"] = "Aluno já adicionado na turma!"
                else:
                    user_aluno = AAluno(
                        nome=var_nome,
                        telefone=var_telefone,
                        nome_pai=var_nome_pai,
                        nome_mae=var_nome_mae,
                        turma=var_turma,
                        observacoes=var_observacoes,
                        foto=var_foto  # Salvando a foto do aluno
                    )
                    user_aluno.save()  # Salvando no banco de dados
                    context["success"] = "Aluno adicionado com sucesso!"
                    return redirect('carometro')  # Redireciona após o sucesso
            except Exception as e:
                context["error"] = f"Ocorreu um erro: {str(e)}"
        context["form"] = form
    else:
        form = FormAluno()
        context["form"] = form

    return render(request, 'adicionaraluno.html', context)

def editaraluno(request, aluno_id):
    aluno = get_object_or_404(AAluno, id=aluno_id)

    if request.method == 'POST':
        # Processa os dados do formulário
        aluno.nome = request.POST.get('nome')
        aluno.telefone = request.POST.get('telefone')
        aluno.nome_pai = request.POST.get('nome_pai')
        aluno.nome_mae = request.POST.get('nome_mae')
        aluno.observacoes = request.POST.get('observacoes')

        # Se houver uma foto enviada, atualiza a foto do aluno
        if 'foto' in request.FILES:
            aluno.foto = request.FILES['foto']

        aluno.save()  # Salva as alterações no banco de dados
        return redirect('carometro')  # Redireciona para a página do carômetro

    return render(request, 'editaraluno.html', {'aluno': aluno})

def excluiraluno(request, aluno_id):
    aluno = get_object_or_404(AAluno, id=aluno_id)
    if request.method == 'POST':
        aluno.delete()
        return redirect('carometro')
    return render(request, 'carometro.html')



def upload_foto(request, aluno_id):
    aluno = get_object_or_404(AAluno, id=aluno_id)  # Busca o aluno pelo ID

    if request.method == 'POST' and request.FILES.get('foto'):
        foto = request.FILES['foto']  # Captura o arquivo enviado
        aluno.foto = foto  # Supondo que o modelo AAluno tem um campo chamado 'foto'
        aluno.save()  # Salva a foto no banco de dados
        return JsonResponse({'status': 'sucesso', 'mensagem': 'Foto enviada com sucesso!'})
    elif request.method == 'POST':
        return JsonResponse({'status': 'erro', 'mensagem': 'Nenhuma foto enviada.'}, status=400)

    return render(request, 'upload_foto.html', {'aluno': aluno})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Aviso
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404, redirect
from .models import Aviso


from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test


from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Aviso

@login_required
def muralaviso(request):
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()

    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        if mensagem:
            # Verifica duplicidade com base na mensagem e tempo de criação
            similar_aviso = Aviso.objects.filter(
                mensagem=mensagem,
                data_criacao__gte=now() - timedelta(seconds=5)
            ).exists()
            if similar_aviso:
                return JsonResponse({'status': 'erro', 'mensagem': 'Aviso publicado com sucesso!'})

            aviso = Aviso.objects.create(mensagem=mensagem)
            return JsonResponse({
                'status': 'sucesso',
                'mensagem': aviso.mensagem,
                'data_criacao': aviso.data_criacao.strftime("%d/%m/%Y %H:%M")

            })

    avisos = Aviso.objects.all()
    context = {
        'avisos': avisos,
        'is_coordenador': is_coordenador
    }
    return render(request, 'muralaviso.html', context)

@login_required
def editaraviso(request, aviso_id):
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()
    aviso = get_object_or_404(Aviso, id=aviso_id)

    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        if mensagem:
            aviso.mensagem = mensagem
            aviso.save()
            return redirect('muralaviso')

    context = {
        'aviso': aviso,
        'is_coordenador': is_coordenador
    }
    return render(request, 'editaraviso.html', context)

@login_required
def excluiraviso(request, aviso_id):
    is_coordenador = request.user.groups.filter(name='Coordenador').exists()
    aviso = get_object_or_404(Aviso, id=aviso_id)

    if request.method == 'POST':
        aviso.delete()
        return redirect('muralaviso')

    context = {
        'aviso': aviso,
        'is_coordenador': is_coordenador
    }
    return render(request, 'excluiraviso.html', context)

@login_required
def criar_aviso_ajax(request):
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem', '')
        if mensagem:
            aviso = Aviso.objects.create(mensagem=mensagem)
            return JsonResponse({'status': 'sucesso', 'mensagem': aviso.mensagem}, status=201)
        else:
            return JsonResponse({'status': 'erro', 'mensagem': 'Mensagem vazia'}, status=400)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse


