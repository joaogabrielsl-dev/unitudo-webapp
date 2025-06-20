from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Universidade, Usuario, CompromissoAcademico, EstabelecimentoParceiro,
    AvaliacaoEstabelecimento, Carona, Moradia, EventoAcademico
)


# Customiza o admin de usuário para incluir os campos customizados
class UsuarioAdmin(UserAdmin):
    # Campos a serem exibidos na lista de usuários
    list_display = ('username', 'email', 'nome_completo', 'is_staff')

    # Organiza os campos na página de edição do usuário
    # Adicionamos 'nome_completo' ao lado de 'first_name' e 'last_name'
    fieldsets = UserAdmin.fieldsets + (
        (('Informações Adicionais', {'fields': ('nome_completo', 'telefone', 'universidade')}),)
    )
    # Também é bom adicionar ao add_fieldsets para o formulário de criação de usuário no admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (('Informações Adicionais', {'fields': ('nome_completo', 'telefone', 'universidade')}),)
    )


# Registra os modelos no painel administrativo
admin.site.register(Universidade)
admin.site.register(Usuario, UsuarioAdmin)  # Garante que estamos usando nossa classe customizada
admin.site.register(CompromissoAcademico)
admin.site.register(EstabelecimentoParceiro)
admin.site.register(AvaliacaoEstabelecimento)
admin.site.register(Carona)
admin.site.register(Moradia)
admin.site.register(EventoAcademico)
