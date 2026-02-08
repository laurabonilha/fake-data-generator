from django.shortcuts import render
from django.http import JsonResponse
from .generators import PersonGenerator, CompanyGenerator
from generator.external import PokemonGenerator, DogGenerator
from .exporters import JSONExporter, CSVExporter
from history.models import GenerationHistory


def home(request):
    """
    View da página inicial.
    
    Se logado -> Mostra Gerador (generator/home.html)
    Se deslogado -> Mostra Landing Page (generator/landing.html)
    """
    if request.user.is_authenticated:
        return render(request, 'generator/home.html')
    else:
        return render(request, 'generator/landing.html')


async def generate_data(request):
    """
    View ASSÍNCRONA para gerar dados fake.
    
    APENAS PARA USUÁRIOS LOGADOS.
    """
    # Verificação de login assíncrona
    user = await request.auser()
    if not user.is_authenticated:
        return JsonResponse({
            'error': 'Você precisa estar logado para gerar dados.'
        }, status=401)

    data_type = request.GET.get('data_type', 'person')
    try:
        quantity = int(request.GET.get('quantity', 10))
    except ValueError:
        quantity = 10
        
    export_format = request.GET.get('export_format', 'preview')
    
    # Validações
    if quantity < 1 or quantity > 1000:
        return JsonResponse({
            'error': 'A quantidade deve ser entre 1 e 1000'
        }, status=400)
    
    # Gera os dados
    if data_type == 'person':
        generator = PersonGenerator()
        data = generator.generate(quantity)
        filename = f'pessoas_{quantity}.{export_format}'
    elif data_type == 'company':
        generator = CompanyGenerator()
        data = generator.generate(quantity)
        filename = f'empresas_{quantity}.{export_format}'
    elif data_type == 'pokemon':
        generator = PokemonGenerator()
        # Aqui está a mágica: await na chamada async!
        data = await generator.generate(quantity)
        filename = f'pokemons_{quantity}.{export_format}'
    elif data_type == 'dog':
        generator = DogGenerator()
        data = await generator.generate(quantity)
        filename = f'cachorros_{quantity}.{export_format}'
    else:
        return JsonResponse({
            'error': 'Tipo de dado inválido'
        }, status=400)
    
    # Salva no histórico (usuário já está validado no início)
    if user.is_authenticated:
        await GenerationHistory.objects.acreate(
            user=user,
            data_type=data_type,
            quantity=quantity,
            export_format=export_format
        )
            
    # Exporta no formato solicitado
    if export_format == 'json':
        return JSONExporter.export(data, filename)
    elif export_format == 'csv':
        return CSVExporter.export(data, filename)
    else:  # preview
        return JsonResponse({
            'success': True,
            'data': data[:5],  # Mostra apenas os 5 primeiros
            'total': len(data),
            'message': f'{len(data)} registro(s) gerado(s) com sucesso!'
        })


def about(request):
    """View da página sobre o projeto."""
    return render(request, 'generator/about.html')
