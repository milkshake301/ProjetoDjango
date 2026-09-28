# Basement Bazaar

Catálogo web em **Django** com tema **The Binding of Isaac**, feito para o Desafio da Aula 12 (Back-end com Python).
Cadastre, consulte, edite e exclua itens (passivos, ativos, trinkets e cartas) de um bazar no porão.

> Fã-projeto sem fins lucrativos. *The Binding of Isaac* pertence a seus criadores.

## O que o projeto faz

| Página | Rota | Acesso |
|---|---|---|
| Home | `/` | público |
| Listagem (Read) com busca e filtro | `/produtos/` | público |
| Detalhes | `/produtos/<id>/` | público |
| Cadastrar (Create) | `/produtos/novo/` | **login** |
| Editar (Update) | `/produtos/<id>/editar/` | **login** |
| Excluir (Delete, via POST + confirmação) | `/produtos/<id>/excluir/` | **login** |
| Login / Logout | `/accounts/login/`, `/accounts/logout/` | público |
| Criar conta | `/cadastro/` | público |
| Perfil | `/perfil/` | **login** |
| Status do sistema | `/status/` | público |
| Admin | `/admin/` | superusuário |

- **MVT**: model `Produto`, views em `app/views.py`, templates em `app/templates/`.
- **Herança de templates**: todas as páginas estendem `base.html` (Bootstrap 5, navbar e rodapé globais).
- **Segurança**: `@login_required` em criar/editar/excluir/perfil; botões de editar e excluir só aparecem com `{% if user.is_authenticated %}`; logout por POST com `{% csrf_token %}`.

## Como rodar

```bash
python -m venv venv
# Windows:      venv\Scripts\activate
# Linux/macOS:  source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_isaac        # opcional: cadastra 13 itens de exemplo
python manage.py runserver
```

Acesse http://127.0.0.1:8000. Para rodar os testes: `python manage.py test`.

## Imagens dos itens

O campo **URL da imagem** aceita qualquer link direto para uma imagem (png/gif/jpg). Sem imagem, o card mostra uma lágrima com "?". Sprites em pixel art são exibidos com `image-rendering: pixelated`.

## Estrutura

```
basement_bazaar/
├── manage.py
├── requirements.txt
├── config/            # settings, urls, wsgi, asgi
└── app/
    ├── models.py  views.py  forms.py  urls.py  admin.py  tests.py
    ├── management/commands/seed_isaac.py
    ├── migrations/
    ├── static/app/css/isaac.css
    └── templates/     # base.html, home, produtos, detalhe, form, exclusão, login...
```
