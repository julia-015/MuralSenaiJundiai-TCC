from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from .models import Aviso
from datetime import timedelta


class AvisoViewTests(TestCase):

    def setUp(self):
        """Cria um aviso de teste antes de cada teste."""
        self.aviso = Aviso.objects.create(mensagem="Aviso de teste", data_criacao=now())

    def test_criar_aviso(self):
        """Teste para criar um aviso com sucesso."""
        response = self.client.post(reverse('muralaviso'), {'mensagem': 'Novo aviso'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Aviso.objects.count(), 2)
        # A data de criação pode variar, então ignoramos a comparação exata da data
        expected_response = {
            'status': 'sucesso',
            'mensagem': 'Novo aviso',
            'data_criacao': now().strftime("%d/%m/%Y %H:%M")  # Ajuste para comparação
        }
        # Comparando a data e hora de forma mais flexível
        response_data = response.json()
        self.assertEqual(response_data['status'], expected_response['status'])
        self.assertEqual(response_data['mensagem'], expected_response['mensagem'])
        self.assertTrue(response_data['data_criacao'].startswith(now().strftime("%d/%m/%Y")))

    def test_criar_aviso_duplicado(self):
        """Teste para impedir duplicidade de avisos."""
        Aviso.objects.create(mensagem="Mensagem duplicada", data_criacao=now())
        response = self.client.post(reverse('muralaviso'), {'mensagem': 'Mensagem duplicada'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'erro', 'mensagem': 'Aviso duplicado detectado'}
        )

    def test_editar_aviso(self):
        """Teste para editar a mensagem de um aviso."""
        response = self.client.post(reverse('editaraviso', args=[self.aviso.id]), {'mensagem': 'Mensagem editada'})
        self.assertEqual(response.status_code, 302)  # Redireciona após a edição
        self.aviso.refresh_from_db()
        self.assertEqual(self.aviso.mensagem, 'Mensagem editada')

    def test_excluir_aviso(self):
        """Teste para excluir um aviso."""
        response = self.client.post(reverse('excluiraviso', args=[self.aviso.id]))
        self.assertEqual(response.status_code, 302)  # Redireciona após a exclusão
        self.assertEqual(Aviso.objects.count(), 0)

    def test_fluxo_crud(self):
        """Teste completo do fluxo de criação, edição e exclusão de um aviso."""
        # Criar aviso
        response = self.client.post(reverse('muralaviso'), {'mensagem': 'Aviso CRUD'})
        self.assertEqual(Aviso.objects.count(), 2)

        aviso = Aviso.objects.get(mensagem='Aviso CRUD')
        # Editar aviso
        self.client.post(reverse('editaraviso', args=[aviso.id]), {'mensagem': 'Aviso atualizado'})
        aviso.refresh_from_db()
        self.assertEqual(aviso.mensagem, 'Aviso atualizado')

        # Excluir aviso
        self.client.post(reverse('excluiraviso', args=[aviso.id]))
        self.assertEqual(Aviso.objects.count(), 1)

    def test_acesso_negado_para_nao_autenticados(self):
        """Testa se usuários não autenticados são redirecionados ao tentar acessar as views."""
        self.client.logout()
        response = self.client.get(reverse('muralaviso'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/muralaviso')

