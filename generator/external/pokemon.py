# generator/generators/external/pokemon.py
"""Gerador de dados de Pokémons usando a PokéAPI."""
import random
from typing import List, Dict
from faker import Faker
from .base import BaseExternalGenerator


class PokemonGenerator(BaseExternalGenerator):
    """
    Gera dados de Pokémons usando a PokéAPI.
    
    API: https://pokeapi.co/
    Documentação: https://pokeapi.co/docs/v2
    """
    
    BASE_URL = "https://pokeapi.co/api/v2"
    MAX_POKEMON_ID = 1010  # Total de Pokémons disponíveis
    
    def __init__(self, generation: int = None):
        """
        Inicializa o gerador.
        
        Args:
            generation: Geração específica (1-9) ou None para todas
        """
        self.fake = Faker('pt_BR')
        self.generation = generation
        
        # Ranges de IDs por geração
        self.generation_ranges = {
            1: (1, 151),      # Kanto
            2: (152, 251),    # Johto
            3: (252, 386),    # Hoenn
            4: (387, 493),    # Sinnoh
            5: (494, 649),    # Unova
            6: (650, 721),    # Kalos
            7: (722, 809),    # Alola
            8: (810, 905),    # Galar
            9: (906, 1010),   # Paldea
        }
    
    def generate(self, quantity: int = 1) -> List[Dict]:
        """
        Gera dados de Pokémons.
        
        Args:
            quantity: Quantidade de Pokémons a gerar
            
        Returns:
            Lista com dados dos Pokémons
        """
        pokemons = []
        
        for _ in range(quantity):
            pokemon_data = self._fetch_random_pokemon()
            if pokemon_data:
                pokemons.append(pokemon_data)
            else:
                # Fallback se API falhar
                pokemons.append(self._generate_fallback())
        
        return pokemons
    
    def _fetch_random_pokemon(self) -> Dict:
        """Busca dados de um Pokémon aleatório."""
        pokemon_id = self._get_random_pokemon_id()
        
        data = self._make_request(f"pokemon/{pokemon_id}")
        
        if not data:
            return None
        
        # Busca dados da espécie para obter descrição em PT
        species_data = self._make_request(f"pokemon-species/{pokemon_id}")
        
        return self._format_pokemon_data(data, species_data)
    
    def _get_random_pokemon_id(self) -> int:
        """Retorna ID aleatório baseado na geração especificada."""
        if self.generation and self.generation in self.generation_ranges:
            min_id, max_id = self.generation_ranges[self.generation]
            return random.randint(min_id, max_id)
        else:
            return random.randint(1, self.MAX_POKEMON_ID)
    
    def _format_pokemon_data(self, data: Dict, species_data: Dict = None) -> Dict:
        """Formata dados do Pokémon."""
        # Pega nome em português se disponível
        nome_pt = data['name'].capitalize()
        if species_data and 'names' in species_data:
            for name_entry in species_data['names']:
                if name_entry['language']['name'] == 'pt-BR':
                    nome_pt = name_entry['name']
                    break
        
        # Descrição em português
        descricao = "Pokémon misterioso"
        if species_data and 'flavor_text_entries' in species_data:
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'pt-BR':
                    descricao = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                    break
        
        return {
            'id': data['id'],
            'nome': nome_pt,
            'nome_original': data['name'],
            'altura': data['height'] / 10,  # decímetros -> metros
            'peso': data['weight'] / 10,    # hectogramas -> kg
            'tipos': [t['type']['name'].capitalize() for t in data['types']],
            'habilidades': [a['ability']['name'].replace('-', ' ').title() for a in data['abilities']],
            'stats': {
                'hp': data['stats'][0]['base_stat'],
                'ataque': data['stats'][1]['base_stat'],
                'defesa': data['stats'][2]['base_stat'],
                'velocidade': data['stats'][5]['base_stat'],
            },
            'imagens': {
                'frente': data['sprites']['front_default'],
                'costas': data['sprites']['back_default'],
                'oficial': data['sprites']['other']['official-artwork']['front_default'],
            },
            'descricao': descricao,
            'geracao': self._get_generation_from_id(data['id']),
        }
    
    def _get_generation_from_id(self, pokemon_id: int) -> int:
        """Determina a geração baseado no ID."""
        for gen, (min_id, max_id) in self.generation_ranges.items():
            if min_id <= pokemon_id <= max_id:
                return gen
        return 1
    
    def _generate_fallback(self) -> Dict:
        """Gera dados fake quando API está indisponível."""
        tipos_possiveis = ['Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Dragon', 'Dark', 'Fairy']
        
        return {
            'id': random.randint(1, 1010),
            'nome': f'{self.fake.first_name()}mon',
            'nome_original': 'unknown',
            'altura': round(random.uniform(0.3, 2.5), 1),
            'peso': round(random.uniform(5, 100), 1),
            'tipos': random.sample(tipos_possiveis, random.randint(1, 2)),
            'habilidades': [self.fake.word().title() for _ in range(random.randint(1, 3))],
            'stats': {
                'hp': random.randint(30, 100),
                'ataque': random.randint(30, 100),
                'defesa': random.randint(30, 100),
                'velocidade': random.randint(30, 100),
            },
            'imagens': {
                'frente': None,
                'costas': None,
                'oficial': None,
            },
            'descricao': 'API temporariamente indisponível - dados gerados aleatoriamente',
            'geracao': random.randint(1, 9),
            'fonte': 'fallback'
        }