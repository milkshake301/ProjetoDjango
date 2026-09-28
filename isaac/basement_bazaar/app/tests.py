from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Produto


class BazarTests(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome='The Sad Onion', categoria='passivo',
            descricao='Cebola triste.', preco=15, estoque=5,
        )
        self.user = get_user_model().objects.create_user('isaac', password='senha-forte-123')

    # ----- Read -----
    def test_paginas_publicas(self):
        for nome in ('home', 'produtos', 'status', 'cadastro', 'login'):
            self.assertEqual(self.client.get(reverse(nome)).status_code, 200, nome)

    def test_listagem_e_detalhe(self):
        self.assertContains(self.client.get(reverse('produtos')), 'The Sad Onion')
        resp = self.client.get(reverse('produto_detalhe', args=[self.produto.pk]))
        self.assertContains(resp, 'Cebola triste.')

    def test_busca_filtra(self):
        resp = self.client.get(reverse('produtos'), {'q': 'inexistente'})
        self.assertNotContains(resp, 'The Sad Onion')

    # ----- Proteção das rotas -----
    def test_anonimo_e_redirecionado_para_login(self):
        alvos = [
            reverse('produto_criar'),
            reverse('produto_editar', args=[self.produto.pk]),
            reverse('produto_excluir', args=[self.produto.pk]),
            reverse('perfil'),
        ]
        for url in alvos:
            resp = self.client.get(url)
            self.assertRedirects(resp, f"{reverse('login')}?next={url}")

    def test_anonimo_nao_consegue_excluir_via_post(self):
        self.client.post(reverse('produto_excluir', args=[self.produto.pk]))
        self.assertTrue(Produto.objects.filter(pk=self.produto.pk).exists())

    def test_botoes_ocultos_para_anonimo(self):
        resp = self.client.get(reverse('produtos'))
        self.assertNotContains(resp, reverse('produto_editar', args=[self.produto.pk]))
        self.assertNotContains(resp, reverse('produto_excluir', args=[self.produto.pk]))

    def test_botoes_visiveis_para_logado(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('produtos'))
        self.assertContains(resp, reverse('produto_editar', args=[self.produto.pk]))
        self.assertContains(resp, reverse('produto_excluir', args=[self.produto.pk]))

    # ----- Create / Update / Delete -----
    def test_criar(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('produto_criar'), {
            'nome': 'Brimstone', 'categoria': 'passivo', 'descricao': '',
            'preco': '25', 'estoque': '2', 'imagem': '',
        })
        novo = Produto.objects.get(nome='Brimstone')
        self.assertRedirects(resp, reverse('produto_detalhe', args=[novo.pk]))

    def test_editar(self):
        self.client.force_login(self.user)
        self.client.post(reverse('produto_editar', args=[self.produto.pk]), {
            'nome': 'The Sad Onion', 'categoria': 'passivo', 'descricao': '',
            'preco': '20', 'estoque': '5', 'imagem': '',
        })
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.preco, 20)

    def test_excluir_exige_post_e_confirmacao(self):
        self.client.force_login(self.user)
        url = reverse('produto_excluir', args=[self.produto.pk])
        resp = self.client.get(url)  # GET só mostra a confirmação
        self.assertContains(resp, 'Excluir')
        self.assertTrue(Produto.objects.filter(pk=self.produto.pk).exists())
        self.client.post(url)
        self.assertFalse(Produto.objects.filter(pk=self.produto.pk).exists())

    def test_estoque_negativo_e_rejeitado(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('produto_criar'), {
            'nome': 'X', 'categoria': 'ativo', 'descricao': '',
            'preco': '1', 'estoque': '-1', 'imagem': '',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Produto.objects.filter(nome='X').exists())

    # ----- Autenticação -----
    def test_cadastro_cria_usuario_e_loga(self):
        self.client.post(reverse('cadastro'), {
            'username': 'binah', 'password1': 'senha-forte-987', 'password2': 'senha-forte-987',
        })
        self.assertTrue(get_user_model().objects.filter(username='binah').exists())
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_via_post(self):
        self.client.force_login(self.user)
        self.client.post(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
