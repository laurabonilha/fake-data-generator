# generator/generators/external/dog.py
"""Gerador de dados de cachorros usando Dog CEO API."""
import random
from typing import List, Dict
from faker import Faker
from .base import BaseExternalGenerator
import httpx
import asyncio


class DogGenerator(BaseExternalGenerator):
    """
    Gera dados de cachorros usando a Dog CEO API.
    
    API: https://dog.ceo/dog-api/
    Documentação: https://dog.ceo/dog-api/documentation/
    
    Gera informações sobre raças de cachorros com fotos reais.
    """
    
    BASE_URL = "https://dog.ceo/api"
    
    def __init__(self):
        """Inicializa o gerador."""
        self.fake = Faker('pt_BR')
        self._breeds_cache = None
    
    async def generate(self, quantity: int = 1) -> List[Dict]:
        """
        Gera dados de cachorros de forma ASSÍNCRONA.
        
        Args:
            quantity: Quantidade de cachorros a gerar
            
        Returns:
            Lista com dados dos cachorros
        """
        dogs = []
        tasks = []
        
        async with httpx.AsyncClient() as client:
            # Busca lista de raças (uma única vez, assincronamente)
            if not self._breeds_cache:
                breeds_data = await self._make_request(client, 'breeds/list/all')
                if breeds_data and 'message' in breeds_data:
                    self._breeds_cache = list(breeds_data['message'].keys())
            
            if not self._breeds_cache:
                # Fallback se API falhar na listagem
                return [self._generate_fallback() for _ in range(quantity)]
            
            # Cria tarefas concorrentes
            for _ in range(quantity):
                tasks.append(self._fetch_random_dog(client))
                
            # Dispara todas
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                 if isinstance(result, Exception) or not result:
                      dogs.append(self._generate_fallback())
                 else:
                      dogs.append(result)
        
        return dogs
    
    async def _fetch_random_dog(self, client: httpx.AsyncClient) -> Dict:
        """Busca dados de um cachorro aleatório assincronamente."""
        if not self._breeds_cache:
             return None
             
        breed = random.choice(self._breeds_cache)
        
        # Busca imagem da raça
        images_data = await self._make_request(client, f'breed/{breed}/images/random')
        
        if not images_data or 'message' not in images_data:
            return None
        
        # A API retorna a imagem como string única, mas o método de formatação espera lista?
        # O código original passava images_data['message'] que é string (url).
        # Vamos corrigir isso e passar como lista de 1 item.
        image_url = images_data['message']
        
        return self._format_dog_data(breed, [image_url])
    
    def _format_dog_data(self, breed: str, images: List[str]) -> Dict:
        """Formata dados do cachorro."""
        # Nomes de cachorros populares no Brasil
        nomes_populares = [
            'Thor', 'Mel', 'Nina', 'Bob', 'Luna', 'Bella', 'Rex',
            'Max', 'Amora', 'Pitoco', 'Fred', 'Belinha', 'Duke', 'Lola'
        ]
        
        # Tradução de algumas raças populares
        traducao_racas = {
            'bulldog': 'Buldogue',
            'poodle': 'Poodle',
            'retriever': 'Retriever',
            'beagle': 'Beagle',
            'husky': 'Husky',
            'terrier': 'Terrier',
            'shepherd': 'Pastor',
            'corgi': 'Corgi',
            'dachshund': 'Dachshund',
            'pug': 'Pug',
        }
        
        # Tenta traduzir a raça
        raca_pt = breed.capitalize()
        for en, pt in traducao_racas.items():
            if en in breed.lower():
                raca_pt = breed.replace(en, pt).title()
                break
        
        return {
            'nome': random.choice(nomes_populares),
            'raca': raca_pt,
            'raca_original': breed,
            'idade': random.randint(1, 15),
            'peso': round(random.uniform(3, 40), 1),
            'cor': random.choice([
                'Preto', 'Branco', 'Marrom', 'Caramelo', 'Cinza',
                'Mesclado', 'Tigrado', 'Dourado'
            ]),
            'genero': random.choice(['Macho', 'Fêmea']),
            'castrado': random.choice([True, False]),
            'vacinado': random.choice([True, False]),
            'temperamento': random.choice([
                'Calmo', 'Brincalhão', 'Protetor', 'Carinhoso',
                'Energético', 'Dócil', 'Independente'
            ]),
            'fotos': images,
            'dono': {
                'nome': self.fake.name(),
                'telefone': self.fake.phone_number(),
                'email': self.fake.email(),
            }
        }
    
    def _generate_fallback(self) -> Dict:
        """Gera dados fake quando API está indisponível."""
        racas_comuns = [
            'Vira-lata', 'Poodle', 'Labrador', 'Golden Retriever',
            'Bulldog', 'Beagle', 'Pastor Alemão', 'Shih Tzu'
        ]
        
        nomes = [
            'Thor', 'Mel', 'Nina', 'Bob', 'Luna', 'Bella',
            'Rex', 'Max', 'Amora', 'Pitoco'
        ]
        
        return {
            'nome': random.choice(nomes),
            'raca': random.choice(racas_comuns),
            'raca_original': 'unknown',
            'idade': random.randint(1, 15),
            'peso': round(random.uniform(3, 40), 1),
            'cor': random.choice(['Preto', 'Branco', 'Marrom', 'Caramelo']),
            'genero': random.choice(['Macho', 'Fêmea']),
            'castrado': random.choice([True, False]),
            'vacinado': random.choice([True, False]),
            'temperamento': random.choice(['Calmo', 'Brincalhão', 'Protetor']),
            'fotos': [],
            'dono': {
                'nome': self.fake.name(),
                'telefone': self.fake.phone_number(),
                'email': self.fake.email(),
            },
            'fonte': 'fallback'
        }