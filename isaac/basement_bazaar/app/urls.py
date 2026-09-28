from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('produtos/novo/', views.produto_criar_view, name='produto_criar'),
    path('produtos/<int:pk>/', views.produto_detalhe_view, name='produto_detalhe'),
    path('produtos/<int:pk>/editar/', views.produto_editar_view, name='produto_editar'),
    path('produtos/<int:pk>/excluir/', views.produto_excluir_view, name='produto_excluir'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('status/', views.status_view, name='status'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
]
