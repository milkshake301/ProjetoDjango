from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'descricao', 'preco', 'estoque', 'imagem']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'preco': forms.NumberInput(attrs={'step': '0.5', 'min': '0'}),
            'estoque': forms.NumberInput(attrs={'min': '0'}),
            'imagem': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }
