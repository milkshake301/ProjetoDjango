from django.core.validators import MinValueValidator
from django.db import models

# tipo string   -> CharField(max_length=*)
# tipo inteiro  -> IntegerField()
# tipo decimal  -> FloatField()
# tipo booleano -> BooleanField()


class Produto(models.Model):  # o certo é PRODUTO, no singular
    """Um item à venda no bazar do porão."""

    CATEGORIAS = [
        ('passivo', 'Item passivo'),
        ('ativo', 'Item ativo'),
        ('trinket', 'Trinket'),
        ('carta', 'Carta ou runa'),
    ]

    nome = models.CharField('Nome', max_length=200)
    categoria = models.CharField(
        'Categoria', max_length=20, choices=CATEGORIAS, default='passivo'
    )
    descricao = models.TextField('Descrição', blank=True)
    preco = models.FloatField('Preço (moedas)', validators=[MinValueValidator(0)])
    estoque = models.IntegerField('Estoque', validators=[MinValueValidator(0)])
    imagem = models.URLField('URL da imagem', max_length=500, blank=True, default='')
    criado_em = models.DateTimeField('Cadastrado em', auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return self.nome
