from faker import Faker
from typing import List, Dict


class CompanyGenerator:
    '''
    Gerador de dados de empresas
    '''
    
    def __init__(self, locale: str = 'pt_BR'):
        self.fake = Faker(locale)
        
    def generate(self, quantity: int) -> List[Dict]:
        '''
        Gera dados fake de empresas.
        
        Args:
            quantity: Quantidade de registros a gerar
        
        Returns:
            Lista de dicionários com dados de empresas
        
        '''
        return [
            {
                'razao_social': self.fake.company(),
                'nome_fantasia': self.fake.company(),
                'cnpj': self.fake.cnpj(),
                'email': self.fake.company_email(),
                'telefone': self.fake.phone_number(),
                'endereco': {
                    'logradouro': self.fake.street_address(),
                    'cidade': self.fake.city(),
                    'estado': self.fake.estado_sigla(),
                    'cep': self.fake.postcode()
                }
            }
            for _ in range(quantity)
        ]
        
        
        