# unitudo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Usuario, Universidade, CompromissoAcademico, Carona, Moradia, EventoAcademico


class CustomUserCreationForm(UserCreationForm):
    # Definimos os campos que queremos no formulário
    nome_completo = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    universidade = forms.ModelChoiceField(
        queryset=Universidade.objects.all(),
        required=True,
        empty_label="Selecione sua universidade",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    telefone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'})
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario

        fields = ('nome_completo', 'email', 'universidade', 'telefone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicando a classe 'form-control' para os campos de senha
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmação de Senha'})

    def save(self, commit=True):
        user = super().save(commit=False)
        # Populamos os campos do modelo com os dados do formulário
        user.username = self.cleaned_data['email'] # Mantemos o username como o email
        user.email = self.cleaned_data['email']
        user.nome_completo = self.cleaned_data['nome_completo']
        if commit:
            user.save()
        return user


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicando o estilo de floating label para os campos de nova senha
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova Senha'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmação da Nova Senha'})


class CompromissoAcademicoForm(forms.ModelForm):
    # Usamos um widget para que o campo de data e hora use o seletor nativo do navegador
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = CompromissoAcademico
        # O campo 'usuario' será preenchido automaticamente na view, então não o incluímos aqui.
        fields = ['titulo', 'descricao', 'data_hora', 'tipo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }


class CaronaForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Carona
        # O campo 'ofertante' será preenchido na view
        fields = ['origem', 'destino', 'data_hora', 'vagas_disponiveis', 'valor', 'observacoes', 'tipo_contato', 'valor_contato']
        widgets = {
            'origem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Metrô Butantã'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: USP - Portão 1'}),
            'vagas_disponiveis': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Ar condicionado, prefiro não levar animais.'}),
            'tipo_contato': forms.Select(attrs={'class': 'form-select'}),
            'valor_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu WhatsApp, Instagram, etc.'}),
        }



class MoradiaForm(forms.ModelForm):
    class Meta:
        model = Moradia
        fields = ['tipo_imovel', 'endereco', 'preco', 'tipo_contrato', 'descricao', 'fotos', 'tipo_contato', 'valor_contato']
        widgets = {
            'tipo_imovel': forms.Select(attrs={'class': 'form-select'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Número, Bairro, Cidade - SP'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva o imóvel, regras da casa, contas inclusas, etc.'}),
            'fotos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cole as URLs das fotos aqui, separadas por vírgula'}),
            'tipo_contato': forms.Select(attrs={'class': 'form-select'}),
            'valor_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu WhatsApp, e-mail, etc.'}),
        }


class EventoAcademicoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = EventoAcademico
        fields = ['nome', 'descricao', 'local', 'data_hora', 'aberto_para_externos']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Auditório da Reitoria'}),
            'aberto_para_externos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'aberto_para_externos': 'Este evento é aberto para estudantes de outras universidades?'
        }