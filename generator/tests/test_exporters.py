"""Testes para os exportadores de dados."""
import pytest
import json
import csv
from io import StringIO
from generator.exporters import JSONExporter, CSVExporter


class TestJSONExporter:
    """Testes para o JSONExporter."""
    
    def test_export_returns_http_response(self):
        """Testa se export() retorna HttpResponse."""
        data = [{'nome': 'João Silva', 'idade': 30}]
        response = JSONExporter.export(data)
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'
    
    def test_export_has_correct_filename(self):
        """Testa se o filename está correto no header."""
        data = [{'nome': 'João'}]
        response = JSONExporter.export(data, filename='test.json')
        
        content_disposition = response['Content-Disposition']
        assert 'attachment' in content_disposition
        assert 'test.json' in content_disposition
    
    def test_export_default_filename(self):
        """Testa se usa filename padrão quando não especificado."""
        data = [{'nome': 'João'}]
        response = JSONExporter.export(data)
        
        assert 'data.json' in response['Content-Disposition']
    
    def test_export_valid_json(self):
        """Testa se o conteúdo exportado é JSON válido."""
        data = [
            {'nome': 'João Silva', 'idade': 30, 'cidade': 'São Paulo'},
            {'nome': 'Maria Santos', 'idade': 25, 'cidade': 'Rio de Janeiro'}
        ]
        response = JSONExporter.export(data)
        
        content = response.content.decode('utf-8')
        parsed = json.loads(content)
        
        assert isinstance(parsed, list), "JSON deve ser uma lista"
        assert len(parsed) == 2, "Deve ter 2 itens"
        assert parsed[0]['nome'] == 'João Silva'
        assert parsed[1]['idade'] == 25
    
    def test_export_preserves_nested_structure(self):
        """Testa se exportação preserva estruturas aninhadas."""
        data = [{
            'nome': 'João Silva',
            'endereco': {
                'rua': 'Rua das Flores',
                'cidade': 'São Paulo',
                'estado': 'SP'
            }
        }]
        response = JSONExporter.export(data)
        
        content = response.content.decode('utf-8')
        parsed = json.loads(content)
        
        assert 'endereco' in parsed[0], "Deve preservar estrutura aninhada"
        assert isinstance(parsed[0]['endereco'], dict)
        assert parsed[0]['endereco']['cidade'] == 'São Paulo'
    
    def test_export_handles_special_characters(self):
        """Testa se exportação lida com caracteres especiais."""
        data = [
            {'nome': 'José da Silva', 'cidade': 'São Paulo'},
            {'nome': 'João Araújo', 'cidade': 'Brasília'}
        ]
        response = JSONExporter.export(data)
        
        content = response.content.decode('utf-8')
        parsed = json.loads(content)
        
        assert parsed[0]['nome'] == 'José da Silva'
        assert parsed[0]['cidade'] == 'São Paulo'
        assert parsed[1]['cidade'] == 'Brasília'
    
    def test_export_empty_list(self):
        """Testa exportação de lista vazia."""
        data = []
        response = JSONExporter.export(data)
        
        content = response.content.decode('utf-8')
        parsed = json.loads(content)
        
        assert parsed == []
        assert response.status_code == 200
    
    def test_export_with_numbers(self):
        """Testa exportação com diferentes tipos de dados."""
        data = [{
            'nome': 'João',
            'idade': 30,
            'salario': 5000.50,
            'ativo': True,
            'dependentes': None
        }]
        response = JSONExporter.export(data)
        
        content = response.content.decode('utf-8')
        parsed = json.loads(content)
        
        assert parsed[0]['idade'] == 30
        assert parsed[0]['salario'] == 5000.50
        assert parsed[0]['ativo'] is True
        assert parsed[0]['dependentes'] is None


class TestCSVExporter:
    """Testes para o CSVExporter."""
    
    def test_export_returns_http_response(self):
        """Testa se export() retorna HttpResponse."""
        data = [{'nome': 'João', 'idade': 30}]
        response = CSVExporter.export(data)
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
    
    def test_export_has_correct_filename(self):
        """Testa se o filename está correto no header."""
        data = [{'nome': 'João'}]
        response = CSVExporter.export(data, filename='test.csv')
        
        content_disposition = response['Content-Disposition']
        assert 'attachment' in content_disposition
        assert 'test.csv' in content_disposition
    
    def test_export_empty_data_returns_error(self):
        """Testa se dados vazios retornam erro 400."""
        response = CSVExporter.export([])
        assert response.status_code == 400
    
    def test_flatten_dict_simple(self):
        """Testa achatamento de dicionário simples."""
        data = {'nome': 'João Silva', 'idade': 30}
        result = CSVExporter._flatten_dict(data)
        
        assert result == {'nome': 'João Silva', 'idade': 30}
    
    def test_flatten_dict_nested_one_level(self):
        """Testa achatamento de dicionário com um nível de aninhamento."""
        data = {
            'nome': 'João',
            'endereco': {
                'cidade': 'São Paulo',
                'estado': 'SP'
            }
        }
        result = CSVExporter._flatten_dict(data)
        
        assert 'nome' in result
        assert 'endereco_cidade' in result
        assert 'endereco_estado' in result
        assert result['endereco_cidade'] == 'São Paulo'
        assert result['endereco_estado'] == 'SP'
    
    def test_flatten_dict_deeply_nested(self):
        """Testa achatamento de dicionário profundamente aninhado."""
        data = {
            'nome': 'João',
            'contato': {
                'endereco': {
                    'cidade': 'São Paulo'
                }
            }
        }
        result = CSVExporter._flatten_dict(data)
        
        assert 'contato_endereco_cidade' in result
        assert result['contato_endereco_cidade'] == 'São Paulo'
    
    def test_export_valid_csv(self):
        """Testa se o conteúdo exportado é CSV válido."""
        data = [
            {'nome': 'João Silva', 'idade': 30},
            {'nome': 'Maria Santos', 'idade': 25}
        ]
        response = CSVExporter.export(data)
        
        content = response.content.decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)
        
        assert len(rows) == 2, "Deve ter 2 linhas"
        assert rows[0]['nome'] == 'João Silva'
        assert rows[0]['idade'] == '30'
        assert rows[1]['nome'] == 'Maria Santos'
    
    def test_export_flattens_nested_data(self):
        """Testa se exportação achata dados aninhados corretamente."""
        data = [{
            'nome': 'João',
            'endereco': {
                'cidade': 'São Paulo',
                'estado': 'SP'
            }
        }]
        response = CSVExporter.export(data)
        
        content = response.content.decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)
        
        assert 'endereco_cidade' in rows[0]
        assert 'endereco_estado' in rows[0]
        assert rows[0]['endereco_cidade'] == 'São Paulo'
        assert rows[0]['endereco_estado'] == 'SP'
    
    def test_export_with_special_characters(self):
        """Testa exportação com caracteres especiais."""
        data = [{'nome': 'José da Silva', 'cidade': 'São Paulo'}]
        response = CSVExporter.export(data)
        
        content = response.content.decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)
        
        assert rows[0]['nome'] == 'José da Silva'
        assert rows[0]['cidade'] == 'São Paulo'
    
    def test_export_header_present(self):
        """Testa se o CSV contém cabeçalho."""
        data = [{'nome': 'João', 'idade': 30}]
        response = CSVExporter.export(data)
        
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        
        assert len(lines) >= 2, "Deve ter cabeçalho + pelo menos uma linha"
        assert 'nome' in lines[0]
        assert 'idade' in lines[0]