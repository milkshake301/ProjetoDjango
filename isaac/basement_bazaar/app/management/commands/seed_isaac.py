from django.core.management.base import BaseCommand

from app.models import Produto

ITENS = [
    # nome, categoria, descrição, preço, estoque
    ('The Sad Onion', 'passivo', 'Faz as lágrimas saírem mais rápido: aumenta a cadência de tiro.', 15, 8),
    ('Spoon Bender', 'passivo', 'Suas lágrimas passam a perseguir os inimigos.', 15, 5),
    ('The Inner Eye', 'passivo', 'Dispara três lágrimas de uma vez, em leque.', 15, 3),
    ('Brimstone', 'passivo', 'Troca as lágrimas por um laser de sangue que precisa ser carregado.', 25, 2),
    ("Mom's Knife", 'passivo', 'Em vez de lágrimas, você arremessa uma faca com dano alto.', 20, 1),
    ("Guppy's Head", 'ativo', 'Ao usar, invoca moscas azuis que lutam ao seu lado.', 12, 6),
    ('The D6', 'ativo', 'Reroda todos os itens que estiverem no chão da sala.', 30, 1),
    ('Yum Heart', 'ativo', 'Recupera um coração vermelho quando usado.', 10, 9),
    ('Swallowed Penny', 'trinket', 'Solta moedas no chão sempre que você leva dano.', 5, 12),
    ('Pinky Eye', 'trinket', 'Chance de disparar lágrimas envenenadas.', 5, 0),
    ('Rainbow Worm', 'trinket', 'Concede um efeito aleatório de verme enquanto você o carrega.', 6, 4),
    ('The Fool', 'carta', 'Teleporta você de volta para a sala inicial do andar.', 4, 15),
    ('Chaos Card', 'carta', 'Arremessada, destrói quase qualquer inimigo que ela acertar.', 8, 3),
]


class Command(BaseCommand):
    help = 'Cadastra itens de exemplo no catálogo (não duplica os que já existem).'

    def add_arguments(self, parser):
        parser.add_argument('--limpar', action='store_true', help='Apaga todos os itens antes.')

    def handle(self, *args, **options):
        if options['limpar']:
            apagados, _ = Produto.objects.all().delete()
            self.stdout.write(f'{apagados} registro(s) apagado(s).')

        criados = 0
        for nome, categoria, descricao, preco, estoque in ITENS:
            _, novo = Produto.objects.get_or_create(
                nome=nome,
                defaults={
                    'categoria': categoria,
                    'descricao': descricao,
                    'preco': preco,
                    'estoque': estoque,
                },
            )
            criados += novo
        self.stdout.write(self.style.SUCCESS(f'{criados} item(ns) criado(s).'))
