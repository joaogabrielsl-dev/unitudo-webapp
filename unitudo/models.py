# unitudo/models.py
from django.db.models import Avg
from django.db import models
from django.contrib.auth.models import AbstractUser # Importa AbstractUser para estender o modelo de usuário
from django.core.validators import MinValueValidator, MaxValueValidator # Para validação de notas

# Modelo de Universidade
class Universidade(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome da Universidade")

    class Meta:
        verbose_name = "Universidade"
        verbose_name_plural = "Universidades"
        ordering = ['nome'] # Ordena as universidades por nome

    def __str__(self):
        return self.nome

# Modelo de Usuário Personalizado
class Usuario(AbstractUser):

    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    universidade = models.ForeignKey(Universidade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Universidade")

    nome_completo = models.CharField(max_length=150, blank=True, verbose_name="Nome Completo")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        # Podemos melhorar o __str__ para usar o nome completo se existir
        return self.nome_completo or self.email or self.username

# Modelo de Compromisso da Agenda
class CompromissoAcademico(models.Model):
    TIPOS_COMPROMISSO = [
        ('PROVA', 'Prova'),
        ('TRABALHO', 'Trabalho'),
        ('AULA', 'Aula'),
        ('EVENTO', 'Evento'),
        ('OUTRO', 'Outro'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compromissos', verbose_name="Usuário")
    titulo = models.CharField(max_length=255, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    tipo = models.CharField(max_length=10, choices=TIPOS_COMPROMISSO, default='OUTRO', verbose_name="Tipo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Compromisso Acadêmico"
        verbose_name_plural = "Compromissos Acadêmicos"
        ordering = ['data_hora'] # Ordena os compromissos por data e hora

    def __str__(self):
        return f"{self.titulo} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

# Modelo de Estabelecimento Parceiro
class EstabelecimentoParceiro(models.Model):
    TIPOS_ESTABELECIMENTO = [
        ('BAR', 'Bar'),
        ('RESTAURANTE', 'Restaurante'),
        ('MERCADO', 'Mercado'),
        ('LIVRARIA', 'Livraria'),
        ('ACADEMIA', 'Academia'),
        ('OUTRO', 'Outro'),
    ]

    nome = models.CharField(max_length=255, verbose_name="Nome")
    endereco = models.CharField(max_length=255, verbose_name="Endereço Completo")
    tipo = models.CharField(max_length=20, choices=TIPOS_ESTABELECIMENTO, default='OUTRO', verbose_name="Tipo de Estabelecimento")
    # Para fotos, podemos usar um campo de texto simples para URLs ou, futuramente, ImageField
    # Por simplicidade, usaremos um TextField para armazenar URLs de fotos separadas por vírgula
    fotos = models.TextField(blank=True, null=True, verbose_name="URLs das Fotos (separadas por vírgula)")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    def get_first_foto_url(self):
        """Retorna a URL da primeira foto da lista."""
        if self.fotos:
            # Pega o primeiro item após separar a string pela vírgula
            return self.fotos.split(',')[0].strip()
        return None  # Retorna None se não houver fotos

        # Adicione este segundo método
    @property
    def average_rating(self):
        avg = self.avaliacoes.aggregate(Avg('nota'))['nota__avg']
        return round(avg, 1) if avg else None


    def get_fotos_list(self):
        """Retorna uma lista com todas as URLs de fotos."""
        if self.fotos:
            # Separa a string pela vírgula e remove espaços em branco de cada URL
            return [url.strip() for url in self.fotos.split(',')]
        return []  # Retorna uma lista vazia se não houver fotos

    class Meta:
        verbose_name = "Estabelecimento Parceiro"
        verbose_name_plural = "Estabelecimentos Parceiros"
        ordering = ['nome']

    def __str__(self):
        return self.nome

# Modelo de Avaliação de Estabelecimento
class AvaliacaoEstabelecimento(models.Model):
    estabelecimento = models.ForeignKey(EstabelecimentoParceiro, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name="Estabelecimento")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas', verbose_name="Usuário")
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota (1 a 5)"
    )
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")

    class Meta:
        verbose_name = "Avaliação de Estabelecimento"
        verbose_name_plural = "Avaliações de Estabelecimentos"
        unique_together = ('estabelecimento', 'usuario') # Um usuário só pode avaliar um estabelecimento uma vez
        ordering = ['-data_avaliacao']

    def __str__(self):
        return f"Avaliação de {self.estabelecimento.nome} por {self.usuario.username}: {self.nota} estrelas"

# Modelo de Carona
class Carona(models.Model):
    TIPO_CONTATO_CHOICES = [
        ('TELEFONE', 'Telefone/WhatsApp'),
        ('EMAIL', 'E-mail'),
        ('INSTAGRAM', 'Instagram'),
        ('OUTRO', 'Outro'),
    ]

    ofertante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='caronas_ofertadas', verbose_name="Ofertante")
    origem = models.CharField(max_length=255, verbose_name="Origem")
    destino = models.CharField(max_length=255, verbose_name="Destino")
    data_hora = models.DateTimeField(verbose_name="Data e Hora da Partida")
    vagas_disponiveis = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Vagas Disponíveis")
    valor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Valor (R$)")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    # Campos de contato atualizados[1]
    tipo_contato = models.CharField(max_length=20, choices=TIPO_CONTATO_CHOICES, default='TELEFONE', verbose_name="Tipo de Contato")
    valor_contato = models.CharField(max_length=255, verbose_name="Contato")
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")

    class Meta:
        verbose_name = "Carona"
        verbose_name_plural = "Caronas"
        ordering = ['data_hora']

    def __str__(self):
        return f"Carona de {self.origem} para {self.destino} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

# Modelo de Moradia
class Moradia(models.Model):
    TIPOS_IMOVEL = [
        ('APARTAMENTO', 'Apartamento'),
        ('KITNET', 'Kitnet'),
        ('CASA', 'Casa'),
        ('QUARTO', 'Quarto'),
        ('REPUBLICA', 'República'),
        ('OUTRO', 'Outro'),
    ]

    TIPOS_CONTRATO = [
        ('MENSAL', 'Mensal'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
        ('NEGOCIAVEL', 'Negociável'),
    ]

    TIPO_CONTATO_CHOICES = [
        ('TELEFONE', 'Telefone/WhatsApp'),
        ('EMAIL', 'E-mail'),
        ('INSTAGRAM', 'Instagram'),
        ('OUTRO', 'Outro'),
    ]

    anunciante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='moradias_anunciadas', verbose_name="Anunciante")
    tipo_imovel = models.CharField(max_length=20, choices=TIPOS_IMOVEL, verbose_name="Tipo de Imóvel")
    endereco = models.CharField(max_length=255, verbose_name="Endereço Completo")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")
    tipo_contrato = models.CharField(max_length=20, choices=TIPOS_CONTRATO, default='MENSAL', verbose_name="Tipo de Contrato")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    # Para fotos, similar aos estabelecimentos, usaremos um campo de texto para URLs
    fotos = models.TextField(blank=True, null=True, verbose_name="URLs das Fotos (separadas por vírgula)")
    tipo_contato = models.CharField(max_length=20, choices=TIPO_CONTATO_CHOICES, default='TELEFONE', verbose_name="Tipo de Contato")
    valor_contato = models.CharField(max_length=255, verbose_name="Contato")
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")

    def get_first_foto_url(self):
        """Retorna a URL da primeira foto da lista."""
        if self.fotos:
            return self.fotos.split(',')[0].strip()
        # Opcional: Retorna uma URL de uma imagem padrão se não houver fotos
        return 'https://via.placeholder.com/400x300.png?text=Sem+Foto'

    def get_fotos_list(self):
        """Retorna uma lista com todas as URLs de fotos."""
        if self.fotos:
            return [url.strip() for url in self.fotos.split(',')]
        return []

    class Meta:
        verbose_name = "Moradia"
        verbose_name_plural = "Moradias"
        ordering = ['-data_publicacao'] # Ordena pela mais recente

    def __str__(self):
        return f"{self.tipo_imovel} em {self.endereco} - R${self.preco}/mês"

# Modelo de Evento Acadêmico
class EventoAcademico(models.Model):
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_criados', verbose_name="Criador do Evento")
    nome = models.CharField(max_length=255, verbose_name="Nome do Evento")
    descricao = models.TextField(verbose_name="Descrição do Evento")
    local = models.CharField(max_length=255, verbose_name="Local")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    aberto_para_externos = models.BooleanField(default=False, verbose_name="Aberto para outras universidades?")
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")

    class Meta:
        verbose_name = "Evento Acadêmico"
        verbose_name_plural = "Eventos Acadêmicos"
        ordering = ['data_hora']

    def __str__(self):
        return f"{self.nome} em {self.local} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

