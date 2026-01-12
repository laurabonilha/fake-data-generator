"""Testes para os geradores de dados."""
import pytest
from generator.generators import PersonGenerator, CompanyGenerator


class TestPersonGenerator:
    """Testes para o PersonGenerator."""
    
    def setup_method(self):
        """Executado antes de cada teste."""
        self.generator = PersonGenerator()
    
    def test_generate_returns_list(self):
        """Testa se generate() retorna uma lista."""
        result = self.generator.generate(quantity=1)
        assert isinstance(result, list), "Resultado deve ser uma lista"
    
    def test_generate_correct_quantity(self):
        """Testa se gera a quantidade correta de registros."""
        for qty in [1, 5, 10, 50]:
            result = self.generator.generate(quantity=qty)
            assert len(result) == qty, f"Deveria gerar {qty} registros"
    
    def test_person_has_required_fields(self):
        """Testa se pessoa tem todos os campos obrigatórios."""
        result = self.generator.generate(quantity=1)
        person = result[0]
        
        required_fields = [
            'nome_completo', 'cpf', 'rg', 'email', 
            'data_nascimento', 'telefone_fixo', 'celular', 
            'profissao', 'endereco'
        ]
        
        for field in required_fields:
            assert field in person, f"Campo '{field}' está faltando"
    
    def test_endereco_structure(self):
        """Testa se endereço tem a estrutura correta."""
        result = self.generator.generate(quantity=1)
        endereco = result[0]['endereco']
        
        assert isinstance(endereco, dict), "Endereço deve ser um dicionário"
        
        required_fields = [
            'logradouro', 'numero', 'bairro', 'cidade', 
            'estado', 'estado_sigla', 'cep', 'pais'
        ]
        
        for field in required_fields:
            assert field in endereco, f"Campo '{field}' está faltando no endereço"
    
    def test_cpf_format(self):
        """Testa se CPF está no formato correto (XXX.XXX.XXX-XX)."""
        result = self.generator.generate(quantity=1)
        cpf = result[0]['cpf']
        
        assert isinstance(cpf, str), "CPF deve ser string"
        assert len(cpf) == 14, f"CPF deve ter 14 caracteres, tem {len(cpf)}"
        assert cpf[3] == '.', "Posição 3 deve ter ponto"
        assert cpf[7] == '.', "Posição 7 deve ter ponto"
        assert cpf[11] == '-', "Posição 11 deve ter hífen"
    
    def test_email_is_valid(self):
        """Testa se email tem formato válido."""
        result = self.generator.generate(quantity=1)
        email = result[0]['email']
        
        assert '@' in email, "Email deve conter @"
        assert '.' in email, "Email deve conter domínio"
    
    def test_data_nascimento_format(self):
        """Testa se data de nascimento está no formato DD/MM/YYYY."""
        result = self.generator.generate(quantity=1)
        data = result[0]['data_nascimento']
        
        assert isinstance(data, str), "Data deve ser string"
        assert len(data) == 10, f"Data deve ter 10 caracteres (DD/MM/YYYY)"
        assert data[2] == '/', "Posição 2 deve ter barra"
        assert data[5] == '/', "Posição 5 deve ter barra"
    
    def test_multiple_generations_are_different(self):
        """Testa se gerações múltiplas produzem dados diferentes."""
        result1 = self.generator.generate(quantity=1)
        result2 = self.generator.generate(quantity=1)
        
        # É extremamente improvável que CPFs sejam iguais
        assert result1[0]['cpf'] != result2[0]['cpf'], "CPFs devem ser diferentes"
    
    def test_large_quantity(self):
        """Testa geração de grande quantidade de dados."""
        result = self.generator.generate(quantity=100)
        assert len(result) == 100, "Deve gerar 100 registros"
        
        # Verifica que todos têm os campos necessários
        for person in result:
            assert 'nome_completo' in person
            assert 'cpf' in person


class TestCompanyGenerator:
    """Testes para o CompanyGenerator."""
    
    def setup_method(self):
        """Executado antes de cada teste."""
        self.generator = CompanyGenerator()
    
    def test_generate_returns_list(self):
        """Testa se generate() retorna uma lista."""
        result = self.generator.generate(quantity=1)
        assert isinstance(result, list), "Resultado deve ser uma lista"
    
    def test_generate_correct_quantity(self):
        """Testa se gera a quantidade correta de registros."""
        for qty in [1, 5, 10, 50]:
            result = self.generator.generate(quantity=qty)
            assert len(result) == qty, f"Deveria gerar {qty} registros"
    
    def test_company_has_required_fields(self):
        """Testa se empresa tem todos os campos obrigatórios."""
        result = self.generator.generate(quantity=1)
        company = result[0]
        
        required_fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 
            'email', 'telefone', 'endereco'
        ]
        
        for field in required_fields:
            assert field in company, f"Campo '{field}' está faltando"
    
    def test_cnpj_format(self):
        """Testa se CNPJ está no formato correto (XX.XXX.XXX/XXXX-XX)."""
        result = self.generator.generate(quantity=1)
        cnpj = result[0]['cnpj']
        
        assert isinstance(cnpj, str), "CNPJ deve ser string"
        assert len(cnpj) == 18, f"CNPJ deve ter 18 caracteres, tem {len(cnpj)}"
        assert cnpj[2] == '.', "Posição 2 deve ter ponto"
        assert cnpj[6] == '.', "Posição 6 deve ter ponto"
        assert cnpj[10] == '/', "Posição 10 deve ter barra"
        assert cnpj[15] == '-', "Posição 15 deve ter hífen"
    
    def test_email_is_valid(self):
        """Testa se email tem formato válido."""
        result = self.generator.generate(quantity=1)
        email = result[0]['email']
        
        assert '@' in email, "Email deve conter @"
        assert '.' in email, "Email deve conter domínio"
    
    def test_endereco_structure(self):
        """Testa se endereço tem a estrutura correta."""
        result = self.generator.generate(quantity=1)
        endereco = result[0]['endereco']
        
        assert isinstance(endereco, dict), "Endereço deve ser um dicionário"
        assert 'cidade' in endereco
        assert 'estado' in endereco
        assert 'cep' in endereco
    
    def test_multiple_generations_are_different(self):
        """Testa se gerações múltiplas produzem dados diferentes."""
        result1 = self.generator.generate(quantity=1)
        result2 = self.generator.generate(quantity=1)
        
        # CNPJs devem ser diferentes
        assert result1[0]['cnpj'] != result2[0]['cnpj'], "CNPJs devem ser diferentes"


# Testes parametrizados (bonus!)
@pytest.mark.parametrize("locale", ['pt_BR'])
def test_generator_with_locale(locale):
    """Testa se gerador funciona com locale brasileiro."""
    generator = PersonGenerator(locale=locale)
    result = generator.generate(quantity=1)
    
    assert len(result) == 1
    assert 'nome_completo' in result[0]
    assert 'cpf' in result[0]