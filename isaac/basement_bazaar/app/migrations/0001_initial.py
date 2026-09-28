import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('categoria', models.CharField(choices=[('passivo', 'Item passivo'), ('ativo', 'Item ativo'), ('trinket', 'Trinket'), ('carta', 'Carta ou runa')], default='passivo', max_length=20, verbose_name='Categoria')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('preco', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Preço (moedas)')),
                ('estoque', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Estoque')),
                ('imagem', models.URLField(blank=True, default='', max_length=500, verbose_name='URL da imagem')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
                'ordering': ['nome'],
            },
        ),
    ]
