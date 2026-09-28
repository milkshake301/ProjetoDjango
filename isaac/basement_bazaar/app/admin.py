from django.contrib import admin

from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'criado_em')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'estoque')
