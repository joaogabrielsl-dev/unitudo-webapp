# unitudo/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import MySetPasswordForm

urlpatterns = [
    path('parceiros/<int:pk>/', views.estabelecimento_detail_view, name='parceiros_detalhe'),
    # ADICIONE ESTA LINHA
    path('parceiros/<int:pk>/avaliar/', views.avaliar_estabelecimento_view, name='parceiros_avaliar'),
    path('eventos/', views.evento_list_view, name='eventos_lista'),
    path('eventos/meus/', views.meus_eventos_view, name='meus_eventos'),
    path('eventos/adicionar/', views.evento_adicionar_view, name='eventos_adicionar'),
    path('eventos/<int:pk>/', views.evento_detail_view, name='eventos_detalhe'),
    path('eventos/editar/<int:pk>/', views.evento_editar_view, name='eventos_editar'),
    path('eventos/excluir/<int:pk>/', views.evento_excluir_view, name='eventos_excluir'),
    path('moradias/minhas/', views.minhas_moradias_view, name='minhas_moradias'),
    path('moradias/', views.moradia_list_view, name='moradias_lista'),
    path('moradias/adicionar/', views.moradia_adicionar_view, name='moradias_adicionar'),
    path('moradias/<int:pk>/', views.moradia_detail_view, name='moradias_detalhe'),
    path('moradias/editar/<int:pk>/', views.moradia_editar_view, name='moradias_editar'),
    path('moradias/excluir/<int:pk>/', views.moradia_excluir_view, name='moradias_excluir'),
    path('caronas/minhas/', views.minhas_caronas_view, name='minhas_caronas'),
    path('caronas/editar/<int:pk>/', views.carona_editar_view, name='caronas_editar'),
    path('caronas/excluir/<int:pk>/', views.carona_excluir_view, name='caronas_excluir'),
    path('caronas/', views.carona_list_view, name='caronas_lista'),
    path('caronas/adicionar/', views.carona_adicionar_view, name='caronas_adicionar'),
    path('caronas/<int:pk>/', views.carona_detail_view, name='caronas_detalhe'),
    path('parceiros/', views.estabelecimento_list_view, name='parceiros_lista'),
    path('parceiros/<int:pk>/', views.estabelecimento_detail_view, name='parceiros_detalhe'),
    path('', views.agenda_view, name='agenda'),  # A página inicial será a agenda
    path('agenda/adicionar/', views.agenda_adicionar_view, name='agenda_adicionar'),
    path('agenda/editar/<int:pk>/', views.agenda_editar_view, name='agenda_editar'),
    path('agenda/excluir/<int:pk>/', views.agenda_excluir_view, name='agenda_excluir'),
    # URLs de Cadastro
    path('cadastro/', views.cadastro_view, name='cadastro'),

    # URLs de Login e Logout (usando as views prontas do Django)
    path('login/', auth_views.LoginView.as_view(template_name='autenticacao/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # URLs de Recuperação de Senha (usando as views prontas do Django)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='autenticacao/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='autenticacao/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='autenticacao/password_reset_confirm.html',
        form_class=MySetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='autenticacao/password_reset_complete.html'), name='password_reset_complete'),
]
