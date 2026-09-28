import django
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProdutoForm
from .models import Produto


# ---------- Read ----------

def home_view(request):
    context = {
        'recentes': Produto.objects.order_by('-criado_em', '-pk')[:3],
        'total_itens': Produto.objects.count(),
        'estoque_total': Produto.objects.aggregate(t=Sum('estoque'))['t'] or 0,
    }
    return render(request, 'home.html', context)


def produtos_view(request):
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '')

    lista_produtos = Produto.objects.all()
    if q:
        lista_produtos = lista_produtos.filter(
            Q(nome__icontains=q) | Q(descricao__icontains=q)
        )
    if categoria in dict(Produto.CATEGORIAS):
        lista_produtos = lista_produtos.filter(categoria=categoria)

    context = {
        'produtos': lista_produtos,
        'categorias': Produto.CATEGORIAS,
        'q': q,
        'categoria_atual': categoria,
    }
    return render(request, 'produtos.html', context)


def produto_detalhe_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produto_detalhe.html', {'produto': produto})


# ---------- Create / Update / Delete (exigem login) ----------

@login_required
def produto_criar_view(request):
    form = ProdutoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        produto = form.save()
        messages.success(request, f'"{produto.nome}" foi para a prateleira.')
        return redirect('produto_detalhe', pk=produto.pk)
    return render(request, 'produto_form.html', {'form': form, 'titulo': 'Cadastrar item'})


@login_required
def produto_editar_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'"{produto.nome}" foi atualizado.')
        return redirect('produto_detalhe', pk=produto.pk)
    return render(
        request,
        'produto_form.html',
        {'form': form, 'produto': produto, 'titulo': f'Editar {produto.nome}'},
    )


@login_required
def produto_excluir_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    # Só o POST exclui; o GET apenas mostra a página de confirmação.
    if request.method == 'POST':
        nome = produto.nome
        produto.delete()
        messages.success(request, f'"{nome}" foi removido do catálogo.')
        return redirect('produtos')
    return render(request, 'produto_confirmar_exclusao.html', {'produto': produto})


# ---------- Conta e páginas extras ----------

@login_required
def perfil_view(request):
    context = {
        'nome_usuario': request.user.username,
        'email': request.user.email,
        'cargo': 'Administrador do porão' if request.user.is_superuser else 'Comprador',
        'total_itens': Produto.objects.count(),
    }
    return render(request, 'perfil.html', context)


def status_view(request):
    try:
        total = Produto.objects.count()
        banco = 'Conectado'
    except Exception:  # noqa: BLE001 - só para exibir o diagnóstico
        total, banco = None, 'Indisponível'

    context = {
        'id_servidor': request.get_host(),
        'status_sistema': '200 OK - Online',
        'banco': banco,
        'total_itens': total,
        'esgotados': Produto.objects.filter(estoque=0).count() if total is not None else None,
        'versao_django': django.get_version(),
        'agora': timezone.localtime(),
    }
    return render(request, 'status.html', context)


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('produtos')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada. Bem-vindo ao porão!')
            return redirect('produtos')
    else:
        form = UserCreationForm()

    return render(request, 'cadastro.html', {'form': form})
