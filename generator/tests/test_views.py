"""Testes para as views do app generator."""
import pytest
import json
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestHomeView:
    """Testes para a view home."""
    
    def setup_method(self):
        """Executado antes de cada teste."""
        self.client = Client()
        self.url = reverse('generator:home')
    
    def test_home_view_status_code(self):
        """Testa se a página inicial retorna status 200."""
        response = self.client.get(self.url)
        assert response.status_code == 200
    
    def test_home_view_uses_correct_template(self):
        """Testa se usa o template correto."""
        response = self.client.get(self.url)
        template_names = [t.name for t in response.templates]
        
        assert 'generator/home.html' in template_names
        assert 'generator/base.html' in template_names
    
    def test_home_view_contains_title(self):
        """Testa se a página contém o título correto."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        
        assert 'Gerador de Dados Fake' in content
    
    def test_home_view_contains_form_elements(self):
        """Testa se a página contém os elementos do formulário."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        
        assert 'generatorForm' in content
        assert 'data_type' in content
        assert 'quantity' in content
        assert 'export_format' in content
    
    def test_home_view_has_person_option(self):
        """Testa se tem a opção de gerar pessoas."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        
        assert 'person' in content
        assert 'Pessoas' in content
    
    def test_home_view_has_company_option(self):
        """Testa se tem a opção de gerar empresas."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        
        assert 'company' in content
        assert 'Empresas' in content


@pytest.mark.django_db
class TestGenerateDataView:
    """Testes para a view generate_data."""
    
    def setup_method(self):
        """Executado antes de cada teste."""
        self.client = Client()
        self.url = reverse('generator:generate_data')
    
    def test_generate_person_preview_success(self):
        """Testa geração de pessoas em modo preview."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 5,
            'export_format': 'preview'
        })
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['success'] is True
        assert data['total'] == 5
        assert len(data['data']) == 5
        assert 'message' in data
    
    def test_generate_company_preview_success(self):
        """Testa geração de empresas em modo preview."""
        response = self.client.get(self.url, {
            'data_type': 'company',
            'quantity': 3,
            'export_format': 'preview'
        })
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['success'] is True
        assert data['total'] == 3
        assert len(data['data']) == 3
    
    def test_generate_person_data_structure(self):
        """Testa se dados de pessoa têm estrutura correta."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 1,
            'export_format': 'preview'
        })
        
        data = json.loads(response.content)
        person = data['data'][0]
        
        assert 'nome_completo' in person
        assert 'cpf' in person
        assert 'email' in person
        assert 'endereco' in person
    
    def test_generate_json_export(self):
        """Testa exportação em formato JSON."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 2,
            'export_format': 'json'
        })
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'
        assert 'attachment' in response['Content-Disposition']
        assert '.json' in response['Content-Disposition']
    
    def test_generate_csv_export(self):
        """Testa exportação em formato CSV."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 2,
            'export_format': 'csv'
        })
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment' in response['Content-Disposition']
        assert '.csv' in response['Content-Disposition']
    
    def test_invalid_quantity_zero(self):
        """Testa quantidade inválida (zero)."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 0,
            'export_format': 'preview'
        })
        
        assert response.status_code == 400
        data = json.loads(response.content)
        assert 'error' in data
    
    def test_invalid_quantity_negative(self):
        """Testa quantidade inválida (negativa)."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': -5,
            'export_format': 'preview'
        })
        
        assert response.status_code == 400
    
    def test_invalid_quantity_above_maximum(self):
        """Testa quantidade acima do máximo permitido."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 1001,
            'export_format': 'preview'
        })
        
        assert response.status_code == 400
        data = json.loads(response.content)
        assert 'error' in data
    
    def test_invalid_data_type(self):
        """Testa tipo de dado inválido."""
        response = self.client.get(self.url, {
            'data_type': 'invalid_type',
            'quantity': 10,
            'export_format': 'preview'
        })
        
        assert response.status_code == 400
        data = json.loads(response.content)
        assert 'error' in data
        assert 'inválido' in data['error'].lower()
    
    def test_preview_shows_only_first_5(self):
        """Testa se preview mostra apenas os 5 primeiros registros."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 20,
            'export_format': 'preview'
        })
        
        data = json.loads(response.content)
        
        assert len(data['data']) == 5, "Preview deve mostrar apenas 5 registros"
        assert data['total'] == 20, "Total deve ser 20"
    
    def test_default_quantity_is_10(self):
        """Testa se quantidade padrão é 10."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'export_format': 'preview'
        })
        
        data = json.loads(response.content)
        assert data['total'] == 10
    
    def test_default_export_format_is_preview(self):
        """Testa se formato padrão é preview."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 5
        })
        
        # Se é preview, retorna JSON com estrutura específica
        data = json.loads(response.content)
        assert 'success' in data
        assert 'data' in data
        assert 'total' in data
    
    def test_filename_contains_quantity(self):
        """Testa se nome do arquivo contém a quantidade."""
        response = self.client.get(self.url, {
            'data_type': 'person',
            'quantity': 15,
            'export_format': 'json'
        })
        
        filename = response['Content-Disposition']
        assert '15' in filename


@pytest.mark.django_db
class TestAboutView:
    """Testes para a view about."""
    
    def setup_method(self):
        """Executado antes de cada teste."""
        self.client = Client()
        self.url = reverse('generator:about')
    
    def test_about_view_status_code(self):
        """Testa se a página sobre retorna status 200."""
        response = self.client.get(self.url)
        assert response.status_code == 200
    
    def test_about_view_uses_correct_template(self):
        """Testa se usa o template correto."""
        response = self.client.get(self.url)
        template_names = [t.name for t in response.templates]
        
        assert 'generator/about.html' in template_names
        assert 'generator/base.html' in template_names
    
    def test_about_view_contains_title(self):
        """Testa se a página contém informações sobre o projeto."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        
        assert 'Sobre' in content or 'sobre' in content
    
    def test_about_view_contains_technologies(self):
        """Testa se menciona as tecnologias usadas."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        
        # Verifica se menciona as principais tecnologias
        assert 'Django' in content or 'django' in content