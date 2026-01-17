# generator/tests/test_api.py
"""Testes para a API REST."""
import pytest
import json
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestAPIRoot:
    """Testes para o endpoint raiz da API."""
    
    def setup_method(self):
        self.client = Client()
        self.url = reverse('api:api-root')
    
    def test_api_root_status_code(self):
        """Testa se a raiz da API retorna 200."""
        response = self.client.get(self.url)
        assert response.status_code == 200
    
    def test_api_root_returns_json(self):
        """Testa se retorna JSON."""
        response = self.client.get(self.url)
        data = json.loads(response.content)
        
        assert 'message' in data
        assert 'version' in data
        assert 'endpoints' in data
    
    def test_api_root_has_endpoints_info(self):
        """Testa se retorna informações sobre endpoints."""
        response = self.client.get(self.url)
        data = json.loads(response.content)
        
        assert 'persons' in data['endpoints']
        assert 'companies' in data['endpoints']
        assert 'docs' in data['endpoints']


@pytest.mark.django_db
class TestGeneratePersonAPI:
    """Testes para o endpoint de geração de pessoas."""
    
    def setup_method(self):
        self.client = Client()
        self.url = reverse('api:generate-person')
    
    def test_generate_person_default_quantity(self):
        """Testa geração com quantidade padrão (10)."""
        response = self.client.get(self.url)
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['success'] is True
        assert data['total'] == 10
        assert len(data['data']) == 10
    
    def test_generate_person_custom_quantity(self):
        """Testa geração com quantidade customizada."""
        response = self.client.get(self.url, {'quantity': 25})
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['total'] == 25
        assert len(data['data']) == 25
    
    def test_generate_person_data_structure(self):
        """Testa se os dados retornados têm a estrutura correta."""
        response = self.client.get(self.url, {'quantity': 1})
        data = json.loads(response.content)
        
        person = data['data'][0]
        
        assert 'nome_completo' in person
        assert 'cpf' in person
        assert 'email' in person
        assert 'endereco' in person
    
    def test_generate_person_json_format(self):
        """Testa formato JSON."""
        response = self.client.get(self.url, {'quantity': 5, 'export_format': 'json'})
        
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'data' in data
    
    def test_generate_person_csv_format(self):
        """Testa formato CSV."""
        response = self.client.get(self.url, {'quantity': 5, 'export_format': 'csv'})
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment' in response['Content-Disposition']
    
    def test_invalid_quantity_below_minimum(self):
        """Testa quantidade inválida abaixo do mínimo."""
        response = self.client.get(self.url, {'quantity': 0})
        
        assert response.status_code == 400
        data = json.loads(response.content)
        assert 'error' in data
    
    def test_invalid_quantity_above_maximum(self):
        """Testa quantidade inválida acima do máximo."""
        response = self.client.get(self.url, {'quantity': 1001})
        
        assert response.status_code == 400
        data = json.loads(response.content)
        assert 'error' in data
    
    def test_invalid_quantity_not_integer(self):
        """Testa quantidade que não é inteiro."""
        response = self.client.get(self.url, {'quantity': 'abc'})
        
        assert response.status_code == 400
    
    def test_response_has_success_field(self):
        """Testa se resposta tem campo success."""
        response = self.client.get(self.url, {'quantity': 5})
        data = json.loads(response.content)
        
        assert 'success' in data
        assert data['success'] is True
    
    def test_response_has_message(self):
        """Testa se resposta tem mensagem."""
        response = self.client.get(self.url, {'quantity': 5})
        data = json.loads(response.content)
        
        assert 'message' in data
        assert 'gerada(s)' in data['message']


@pytest.mark.django_db
class TestGenerateCompanyAPI:
    """Testes para o endpoint de geração de empresas."""
    
    def setup_method(self):
        self.client = Client()
        self.url = reverse('api:generate-company')
    
    def test_generate_company_default_quantity(self):
        """Testa geração com quantidade padrão."""
        response = self.client.get(self.url)
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['success'] is True
        assert data['total'] == 10
    
    def test_generate_company_custom_quantity(self):
        """Testa geração com quantidade customizada."""
        response = self.client.get(self.url, {'quantity': 15})
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['total'] == 15
        assert len(data['data']) == 15
    
    def test_generate_company_data_structure(self):
        """Testa se os dados têm a estrutura correta."""
        response = self.client.get(self.url, {'quantity': 1})
        data = json.loads(response.content)
        
        company = data['data'][0]
        
        assert 'razao_social' in company
        assert 'cnpj' in company
        assert 'email' in company
        assert 'endereco' in company
    
    def test_generate_company_csv_format(self):
        """Testa exportação em CSV."""
        response = self.client.get(self.url, {'quantity': 3, 'export_format': 'csv'})
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
    
    def test_invalid_quantity(self):
        """Testa validação de quantidade."""
        response = self.client.get(self.url, {'quantity': -5})
        assert response.status_code == 400


@pytest.mark.django_db
class TestAPIDocumentation:
    """Testes para a documentação da API."""
    
    def setup_method(self):
        self.client = Client()
    
    def test_swagger_docs_accessible(self):
        """Testa se a documentação Swagger está acessível."""
        response = self.client.get(reverse('api:swagger-ui'))
        assert response.status_code == 200
    
    def test_redoc_docs_accessible(self):
        """Testa se a documentação ReDoc está acessível."""
        response = self.client.get(reverse('api:redoc'))
        assert response.status_code == 200
    
    def test_schema_accessible(self):
        """Testa se o schema OpenAPI está acessível."""
        response = self.client.get(reverse('api:schema'))
        assert response.status_code == 200