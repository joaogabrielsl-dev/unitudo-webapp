# unitudo/views.py
import json
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CompromissoAcademicoForm, CaronaForm, MoradiaForm, EventoAcademicoForm
from .models import CompromissoAcademico, EstabelecimentoParceiro, Carona, Moradia, EventoAcademico, AvaliacaoEstabelecimento


def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}! Você já pode fazer login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'autenticacao/cadastro.html', context)


@login_required  # Garante que apenas usuários logados possam ver esta página
def agenda_view(request):
    # Filtra os compromissos para mostrar apenas os do usuário logado
    compromissos = CompromissoAcademico.objects.filter(usuario=request.user)
    context = {
        'compromissos': compromissos
    }
    return render(request, 'agenda/agenda_list.html', context)


@login_required
def agenda_adicionar_view(request):
    if request.method == 'POST':
        form = CompromissoAcademicoForm(request.POST)
        if form.is_valid():
            compromisso = form.save(commit=False)  # Não salva no banco ainda
            compromisso.usuario = request.user  # Associa o compromisso ao usuário logado
            compromisso.save()  # Agora salva com o usuário associado
            messages.success(request, 'Compromisso adicionado com sucesso!')
            return redirect('agenda')
    else:
        form = CompromissoAcademicoForm()

    context = {'form': form}
    return render(request, 'agenda/agenda_form.html', context)


@login_required
def agenda_editar_view(request, pk):
    # get_object_or_404 garante que o objeto exista e pertença ao usuário logado, evitando erros e acessos indevidos
    compromisso = get_object_or_404(CompromissoAcademico, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CompromissoAcademicoForm(request.POST, instance=compromisso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compromisso atualizado com sucesso!')
            return redirect('agenda')
    else:
        form = CompromissoAcademicoForm(instance=compromisso)

    context = {'form': form}
    return render(request, 'agenda/agenda_form.html', context)


@login_required
def agenda_excluir_view(request, pk):
    compromisso = get_object_or_404(CompromissoAcademico, pk=pk, usuario=request.user)
    if request.method == 'POST':
        compromisso.delete()
        messages.success(request, 'Compromisso excluído com sucesso!')
        return redirect('agenda')

    context = {'compromisso': compromisso}
    return render(request, 'agenda/agenda_confirm_delete.html', context)

@login_required
def estabelecimento_list_view(request):
    estabelecimentos = EstabelecimentoParceiro.objects.all()
    context = {
        'estabelecimentos': estabelecimentos
    }
    return render(request, 'parceiros/estabelecimento_list.html', context)

@login_required
def estabelecimento_detail_view(request, pk):
    estabelecimento = get_object_or_404(EstabelecimentoParceiro, pk=pk)
    context = {
        'estabelecimento': estabelecimento
    }
    return render(request, 'parceiros/estabelecimento_detail.html', context)

@login_required
def carona_list_view(request):
    origem_query = request.GET.get('origem', '')
    destino_query = request.GET.get('destino', '')

    caronas = Carona.objects.exclude(ofertante=request.user).order_by('data_hora')

    if origem_query:
        caronas = caronas.filter(origem__icontains=origem_query)
    if destino_query:
        caronas = caronas.filter(destino__icontains=destino_query)

    context = {
        'caronas': caronas,
        'origem_query': origem_query,
        'destino_query': destino_query
    }
    return render(request, 'caronas/carona_list.html', context)

@login_required
def carona_adicionar_view(request):
    if request.method == 'POST':
        form = CaronaForm(request.POST)
        if form.is_valid():
            carona = form.save(commit=False)
            carona.ofertante = request.user # Associa a carona ao usuário logado
            carona.save()
            messages.success(request, 'Carona oferecida com sucesso!')
            return redirect('caronas_lista')
    else:
        form = CaronaForm()

    context = {'form': form}
    return render(request, 'caronas/carona_form.html', context)

@login_required
def carona_detail_view(request, pk):
    carona = get_object_or_404(Carona, pk=pk)
    context = {'carona': carona}
    return render(request, 'caronas/carona_detail.html', context)


@login_required
def carona_editar_view(request, pk):
    carona = get_object_or_404(Carona, pk=pk, ofertante=request.user)
    if request.method == 'POST':
        # `instance=carona` pré-preenche o formulário com os dados existentes.
        form = CaronaForm(request.POST, instance=carona)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carona atualizada com sucesso!')
            return redirect('minhas_caronas')  # Redireciona para a nova página "Minhas Caronas"
    else:
        form = CaronaForm(instance=carona)

    # Reutilizamos o mesmo template do formulário de adicionar.
    context = {'form': form}
    return render(request, 'caronas/carona_form.html', context)


@login_required
def carona_excluir_view(request, pk):
    # A mesma verificação de segurança é aplicada aqui.
    carona = get_object_or_404(Carona, pk=pk, ofertante=request.user)
    if request.method == 'POST':
        carona.delete()
        messages.success(request, 'Carona excluída com sucesso!')
        return redirect('minhas_caronas')

    context = {'carona': carona}
    return render(request, 'caronas/carona_confirm_delete.html', context)


@login_required
def minhas_caronas_view(request):
    # Filtra as caronas para mostrar apenas as criadas pelo usuário logado.
    caronas = Carona.objects.filter(ofertante=request.user).order_by('data_hora')
    context = {'caronas': caronas}
    return render(request, 'caronas/minhas_caronas.html', context)


@login_required
def moradia_adicionar_view(request):
    if request.method == 'POST':
        form = MoradiaForm(request.POST)
        if form.is_valid():
            moradia = form.save(commit=False)
            moradia.anunciante = request.user
            moradia.save()
            messages.success(request, 'Anúncio de moradia criado com sucesso!')
            return redirect('minhas_moradias')
    else:
        form = MoradiaForm()
    return render(request, 'moradias/moradia_form.html', {'form': form, 'tipo_operacao': 'Anunciar'})


@login_required
def moradia_detail_view(request, pk):
    moradia = get_object_or_404(Moradia, pk=pk)
    context = {'moradia': moradia}
    return render(request, 'moradias/moradia_detail.html', context)


@login_required
def moradia_editar_view(request, pk):
    moradia = get_object_or_404(Moradia, pk=pk, anunciante=request.user)
    if request.method == 'POST':
        form = MoradiaForm(request.POST, instance=moradia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anúncio atualizado com sucesso!')
            # ATUALIZAÇÃO: Redireciona para a página de gerenciamento[1]
            return redirect('minhas_moradias')
    else:
        form = MoradiaForm(instance=moradia)
    return render(request, 'moradias/moradia_form.html', {'form': form, 'tipo_operacao': 'Editar'})


@login_required
def moradia_excluir_view(request, pk):
    moradia = get_object_or_404(Moradia, pk=pk, anunciante=request.user)
    if request.method == 'POST':
        moradia.delete()
        messages.success(request, 'Anúncio excluído com sucesso!')
        # ATUALIZAÇÃO: Redireciona para a página de gerenciamento[1]
        return redirect('minhas_moradias')
    return render(request, 'moradias/moradia_confirm_delete.html', {'moradia': moradia})


@login_required
def minhas_moradias_view(request):
    moradias = Moradia.objects.filter(anunciante=request.user).order_by('-data_publicacao')
    context = {'moradias': moradias}
    return render(request, 'moradias/minhas_moradias.html', context)


# Atualize a view de listar moradias
@login_required
def moradia_list_view(request):
    # ATUALIZAÇÃO: Excluímos os anúncios do usuário logado da lista principal
    moradias = Moradia.objects.exclude(anunciante=request.user).order_by('-data_publicacao')

    # O resto da lógica de filtro permanece o mesmo
    tipo_query = request.GET.get('tipo', '')
    preco_query = request.GET.get('preco_maximo', '')
    endereco_query = request.GET.get('endereco', '')

    if tipo_query:
        moradias = moradias.filter(tipo_imovel=tipo_query)
    if preco_query:
        moradias = moradias.filter(preco__lte=preco_query)
    if endereco_query:
        moradias = moradias.filter(endereco__icontains=endereco_query)

    context = {
        'moradias': moradias,
        'tipos_imovel': Moradia.TIPOS_IMOVEL,
        'form_values': request.GET
    }
    return render(request, 'moradias/moradia_list.html', context)


@login_required
def evento_list_view(request):
    user = request.user
    eventos = []

    # Apenas executa a query se o usuário tiver uma universidade associada
    if user.universidade:
        # Usamos Q objects para criar uma consulta OR:
        # (evento da universidade do usuário) OU (evento é aberto para externos)
        query = Q(criador__universidade=user.universidade) | Q(aberto_para_externos=True)
        eventos = EventoAcademico.objects.filter(query).distinct().order_by('data_hora')

    context = {'eventos': eventos}
    return render(request, 'eventos/evento_list.html', context)


@login_required
def meus_eventos_view(request):
    eventos = EventoAcademico.objects.filter(criador=request.user).order_by('data_hora')
    context = {'eventos': eventos}
    return render(request, 'eventos/meus_eventos.html', context)


@login_required
def evento_adicionar_view(request):
    if request.method == 'POST':
        form = EventoAcademicoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.criador = request.user
            evento.save()
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('meus_eventos')
    else:
        form = EventoAcademicoForm()
    return render(request, 'eventos/evento_form.html', {'form': form})


@login_required
def evento_detail_view(request, pk):
    evento = get_object_or_404(EventoAcademico, pk=pk)
    context = {'evento': evento}
    return render(request, 'eventos/evento_detail.html', context)


@login_required
def evento_editar_view(request, pk):
    evento = get_object_or_404(EventoAcademico, pk=pk, criador=request.user)
    if request.method == 'POST':
        form = EventoAcademicoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('meus_eventos')
    else:
        form = EventoAcademicoForm(instance=evento)
    return render(request, 'eventos/evento_form.html', {'form': form})


@login_required
def evento_excluir_view(request, pk):
    evento = get_object_or_404(EventoAcademico, pk=pk, criador=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento excluído com sucesso!')
        return redirect('meus_eventos')
    return render(request, 'eventos/evento_confirm_delete.html', {'evento': evento})


@login_required
def avaliar_estabelecimento_view(request, pk):
    if request.method == 'POST':
        try:
            estabelecimento = get_object_or_404(EstabelecimentoParceiro, pk=pk)
            data = json.loads(request.body)
            nota = int(data.get('nota'))

            if not 1 <= nota <= 5:
                return JsonResponse({'sucesso': False, 'erro': 'Nota inválida.'}, status=400)

            # Cria uma nova avaliação ou atualiza uma existente para este usuário e estabelecimento
            avaliacao, created = AvaliacaoEstabelecimento.objects.update_or_create(
                usuario=request.user,
                estabelecimento=estabelecimento,
                defaults={'nota': nota}
            )

            # Recalcula a nova média de notas para o estabelecimento
            nova_media = AvaliacaoEstabelecimento.objects.filter(estabelecimento=estabelecimento).aggregate(Avg('nota'))

            return JsonResponse({
                'sucesso': True,
                'nova_media': round(nova_media['nota__avg'], 1) if nova_media['nota__avg'] else 0,
                'total_avaliacoes': AvaliacaoEstabelecimento.objects.filter(estabelecimento=estabelecimento).count()
            })

        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)

    return JsonResponse({'sucesso': False, 'erro': 'Método inválido.'}, status=405)