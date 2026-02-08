
import pytest
from unittest.mock import Mock, AsyncMock, patch
from generator.external import PokemonGenerator, DogGenerator

@pytest.mark.asyncio
class TestPokemonGenerator:
    """Testes assíncronos para o PokemonGenerator."""
    
    async def test_generate_returns_list(self):
        """Testa se generate() retorna uma lista e se os dados têm a estrutura esperada."""
        generator = PokemonGenerator()
        
        # Mock do httpx.AsyncClient para não bater na API real
        # Criamos um mock que simula o comportamento do cliente HTTP
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 25,
            'name': 'pikachu',
            'height': 4,
            'weight': 60,
            'types': [{'type': {'name': 'electric'}}],
            'abilities': [{'ability': {'name': 'static'}}],
            'stats': [
                {'base_stat': 35}, {'base_stat': 55}, {'base_stat': 40}, 
                {'base_stat': 50}, {'base_stat': 50}, {'base_stat': 90}
            ],
            'sprites': {
                'front_default': 'url',
                'back_default': 'url',
                'other': {'official-artwork': {'front_default': 'url'}}
            }
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()

        # Mock para species data
        mock_species_response = Mock()
        mock_species_response.json.return_value = {
            'names': [{'language': {'name': 'pt-BR'}, 'name': 'Pikachu'}],
            'flavor_text_entries': [{'language': {'name': 'pt-BR'}, 'flavor_text': 'Pika pika!'}]
        }
        mock_species_response.status_code = 200

        # Patch no _make_request para retornar nossos mocks
        # Como o método original aceita um cliente, podemos mockar o _make_request diretamente
        # para simular o retorno processado da API
        
        # Vamos usar uma abordagem mais simples: testar se o método roda e retorna algo (mesmo que seja fallback)
        # em um teste de integração "fake" ou mockar o _make_request da classe
        
        with patch.object(PokemonGenerator, '_make_request', new_callable=AsyncMock) as mock_request:
            # Configura o mock para devolver primeiro os dados do pokemon, depois da especie
            mock_request.side_effect = [
                mock_response.json(), 
                mock_species_response.json()
            ]
            
            result = await generator.generate(quantity=1)
            
            assert isinstance(result, list)
            assert len(result) == 1
            pokemon = result[0]
            assert pokemon['nome'] == 'Pikachu'
            assert pokemon['id'] == 25

    async def test_generate_fallback_on_error(self):
        """Testa se o gerador usa fallback quando a API falha."""
        generator = PokemonGenerator()
        
        # Simula erro na requisição retornando None
        with patch.object(PokemonGenerator, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            
            result = await generator.generate(quantity=1)
            
            assert len(result) == 1
            assert result[0]['fonte'] == 'fallback'


@pytest.mark.asyncio
class TestDogGenerator:
    """Testes assíncronos para o DogGenerator."""
    
    async def test_generate_returns_list(self):
        """Testa se generate() retorna lista de cachorros."""
        generator = DogGenerator()
        
        # Mock das respostas da API
        breeds_response = {'message': {'poodle': [], 'bulldog': []}, 'status': 'success'}
        image_response = {'message': 'https://images.dog.ceo/breeds/poodle/n02113799_1080.jpg', 'status': 'success'}
        
        with patch.object(DogGenerator, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                breeds_response,  # Lista de raças
                image_response    # Imagem aleatória
            ]
            
            result = await generator.generate(quantity=1)
            
            assert isinstance(result, list)
            assert len(result) == 1
            dog = result[0]
            assert dog['raca_original'] in ['poodle', 'bulldog']
            assert len(dog['fotos']) > 0

    async def test_generate_fallback_on_error(self):
        """Testa fallback quando a API de raças falha."""
        generator = DogGenerator()
        
        with patch.object(DogGenerator, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None  # Falha ao buscar raças
            
            result = await generator.generate(quantity=1)
            
            assert len(result) == 1
            assert result[0]['fonte'] == 'fallback'
