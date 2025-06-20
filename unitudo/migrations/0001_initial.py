# Generated by Django 5.2.3 on 2025-06-18 21:24

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstabelecimentoParceiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('endereco', models.CharField(max_length=255, verbose_name='Endereço Completo')),
                ('tipo', models.CharField(choices=[('BAR', 'Bar'), ('RESTAURANTE', 'Restaurante'), ('MERCADO', 'Mercado'), ('LIVRARIA', 'Livraria'), ('ACADEMIA', 'Academia'), ('OUTRO', 'Outro')], default='OUTRO', max_length=20, verbose_name='Tipo de Estabelecimento')),
                ('fotos', models.TextField(blank=True, null=True, verbose_name='URLs das Fotos (separadas por vírgula)')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
            ],
            options={
                'verbose_name': 'Estabelecimento Parceiro',
                'verbose_name_plural': 'Estabelecimentos Parceiros',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Universidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome da Universidade')),
            ],
            options={
                'verbose_name': 'Universidade',
                'verbose_name_plural': 'Universidades',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('universidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unitudo.universidade', verbose_name='Universidade')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Carona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origem', models.CharField(max_length=255, verbose_name='Origem')),
                ('destino', models.CharField(max_length=255, verbose_name='Destino')),
                ('data_hora', models.DateTimeField(verbose_name='Data e Hora da Partida')),
                ('vagas_disponiveis', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Vagas Disponíveis')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Valor (R$)')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('contato', models.CharField(max_length=255, verbose_name='Contato para Carona (Tel, Email, Instagram, etc.)')),
                ('data_publicacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Publicação')),
                ('ofertante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caronas_ofertadas', to=settings.AUTH_USER_MODEL, verbose_name='Ofertante')),
            ],
            options={
                'verbose_name': 'Carona',
                'verbose_name_plural': 'Caronas',
                'ordering': ['data_hora'],
            },
        ),
        migrations.CreateModel(
            name='CompromissoAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('data_hora', models.DateTimeField(verbose_name='Data e Hora')),
                ('tipo', models.CharField(choices=[('PROVA', 'Prova'), ('TRABALHO', 'Trabalho'), ('AULA', 'Aula'), ('EVENTO', 'Evento'), ('OUTRO', 'Outro')], default='OUTRO', max_length=10, verbose_name='Tipo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compromissos', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Compromisso Acadêmico',
                'verbose_name_plural': 'Compromissos Acadêmicos',
                'ordering': ['data_hora'],
            },
        ),
        migrations.CreateModel(
            name='EventoAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Evento')),
                ('descricao', models.TextField(verbose_name='Descrição do Evento')),
                ('local', models.CharField(max_length=255, verbose_name='Local')),
                ('data_hora', models.DateTimeField(verbose_name='Data e Hora')),
                ('aberto_para_externos', models.BooleanField(default=False, verbose_name='Aberto para outras universidades?')),
                ('data_publicacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Publicação')),
                ('criador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_criados', to=settings.AUTH_USER_MODEL, verbose_name='Criador do Evento')),
            ],
            options={
                'verbose_name': 'Evento Acadêmico',
                'verbose_name_plural': 'Eventos Acadêmicos',
                'ordering': ['data_hora'],
            },
        ),
        migrations.CreateModel(
            name='Moradia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_imovel', models.CharField(choices=[('APARTAMENTO', 'Apartamento'), ('KITNET', 'Kitnet'), ('CASA', 'Casa'), ('QUARTO', 'Quarto'), ('REPUBLICA', 'República'), ('OUTRO', 'Outro')], max_length=20, verbose_name='Tipo de Imóvel')),
                ('endereco', models.CharField(max_length=255, verbose_name='Endereço Completo')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço (R$)')),
                ('tipo_contrato', models.CharField(choices=[('MENSAL', 'Mensal'), ('SEMESTRAL', 'Semestral'), ('ANUAL', 'Anual'), ('NEGOCIAVEL', 'Negociável')], default='MENSAL', max_length=20, verbose_name='Tipo de Contrato')),
                ('descricao', models.TextField(verbose_name='Descrição Detalhada')),
                ('fotos', models.TextField(blank=True, null=True, verbose_name='URLs das Fotos (separadas por vírgula)')),
                ('contato', models.CharField(max_length=255, verbose_name='Contato para Moradia (Tel, Email, Instagram, etc.)')),
                ('data_publicacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Publicação')),
                ('anunciante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moradias_anunciadas', to=settings.AUTH_USER_MODEL, verbose_name='Anunciante')),
            ],
            options={
                'verbose_name': 'Moradia',
                'verbose_name_plural': 'Moradias',
                'ordering': ['-data_publicacao'],
            },
        ),
        migrations.CreateModel(
            name='AvaliacaoEstabelecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Nota (1 a 5)')),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True, verbose_name='Data da Avaliação')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes_feitas', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='unitudo.estabelecimentoparceiro', verbose_name='Estabelecimento')),
            ],
            options={
                'verbose_name': 'Avaliação de Estabelecimento',
                'verbose_name_plural': 'Avaliações de Estabelecimentos',
                'ordering': ['-data_avaliacao'],
                'unique_together': {('estabelecimento', 'usuario')},
            },
        ),
    ]
