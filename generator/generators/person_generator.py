from faker import Faker
from typing import List, Dict


class PersonGenerator:
    '''
    Gera dados de pessoas
    '''
    
    def __init__(self, locale: str = 'pt_BR'):
        self.fake = Faker(locale)
        
    def generate(self, quantity: int) -> List[Dict]:
        """
        Gera dados fake de pessoas usando apenas métodos do Faker.
        
        Args:
            quantity: Quantidade de registros a gerar
            
        Returns:
            Lista de dicionários com dados de pessoas
        """
        return [
            {
                'nome_completo': self.fake.name(),
                'cpf': self.fake.cpf(),
                'rg': self.fake.rg(),
                'email': self.fake.email(),
                'data_nascimento': self.fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d/%m/%Y'),
                'telefone_fixo': self.fake.phone_number(),
                'celular': self.fake.phone_number(),
                'profissao': self.fake.job(),
                'endereco': {
                    'logradouro': self.fake.street_name(),
                    'numero': self.fake.building_number(),
                    'bairro': self.fake.bairro(),
                    'cidade': self.fake.city(),
                    'estado': self.fake.estado_nome(),
                    'estado_sigla': self.fake.estado_sigla(),
                    'cep': self.fake.postcode(),
                    'pais': self.fake.current_country(),
                }
            }
            for _ in range(quantity)
        ]