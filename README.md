# 🎲 Fake Data Generator

Gerador de dados fake para testes e desenvolvimento, criado com Django e Python.

## 📋 Sobre o Projeto

O Fake Data Generator é uma ferramenta web que permite gerar dados realistas de pessoas e empresas brasileiras para uso em ambientes de desenvolvimento e testes. Os dados podem ser exportados em formatos JSON e CSV.

## ✨ Funcionalidades

- ✅ Geração de dados de pessoas (nome, CPF, email, telefone, endereço)
- ✅ Geração de dados de empresas (CNPJ, razão social, contatos)
- ✅ Exportação em JSON e CSV
- ✅ Preview dos dados antes do download
- ✅ Geração de até 1000 registros por vez
- ✅ Interface responsiva e intuitiva
- ✅ **API REST com documentação interativa**
- ✅ **Rate limiting e validações**

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Django 5.0**
- **Django REST Framework** - API REST
- **drf-spectacular** - Documentação OpenAPI/Swagger
- **Faker** - Geração de dados fake
- **Bootstrap 5** - Framework CSS
- **pytest** - Testes automatizados
- **SQLite** - Banco de dados

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/laurabonilha/fake-data-generator.git
cd fake-data-generator
```

2. Crie e ative o ambiente virtual:
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env na raiz do projeto
cp .env.example .env
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

7. Acesse no navegador:
```
# Interface Web
http://localhost:8000

# Documentação da API
http://localhost:8000/api/v1/docs/
```

## 🌐 API REST

O projeto disponibiliza uma API REST completa para integração com outros sistemas.

### Endpoints Disponíveis

**Base URL:** `http://localhost:8000/api/v1/`

| Endpoint | Método | Descrição | Parâmetros |
|----------|--------|-----------|------------|
| `/api/v1/` | GET | Informações da API | - |
| `/api/v1/generate/person/` | GET | Gerar pessoas | `quantity` (1-1000), `export_format` (json/csv) |
| `/api/v1/generate/company/` | GET | Gerar empresas | `quantity` (1-1000), `export_format` (json/csv) |
| `/api/v1/docs/` | GET | Documentação Swagger | - |
| `/api/v1/redoc/` | GET | Documentação ReDoc | - |
| `/api/v1/schema/` | GET | Schema OpenAPI | - |

### Exemplos de Uso

**Gerar 10 pessoas (JSON):**
```bash
curl "http://localhost:8000/api/v1/generate/person/?quantity=10"
```

**Gerar 5 empresas (CSV):**
```bash
curl "http://localhost:8000/api/v1/generate/company/?quantity=5&export_format=csv" -o empresas.csv
```

**Resposta JSON (exemplo):**
```json
{
  "success": true,
  "data": [
    {
      "nome_completo": "João Silva",
      "cpf": "123.456.789-00",
      "email": "joao@email.com",
      "telefone_fixo": "(11) 1234-5678",
      "endereco": {
        "cidade": "São Paulo",
        "estado": "SP"
      }
    }
  ],
  "total": 1,
  "message": "1 pessoa(s) gerada(s) com sucesso"
}
```

### Rate Limiting

A API possui limite de **100 requisições por hora** para usuários não autenticados.

### Documentação Interativa

Acesse `/api/v1/docs/` para testar os endpoints diretamente no navegador com a interface Swagger.

## 📦 Estrutura do Projeto

```
fake-data-generator/
├── config/                 # Configurações do Django
├── generator/              # App principal
│   ├── generators/         # Geradores de dados
│   ├── exporters/         # Exportadores (JSON, CSV)
│   ├── templates/         # Templates HTML
│   └── views.py           # Views
├── static/                # Arquivos estáticos
├── manage.py
├── requirements.txt
└── README.md
```

## 🧪 Testes

O projeto possui testes automatizados com **pytest** para garantir a qualidade do código.

### Executar os Testes

```bash
# Rodar todos os testes
pytest

# Rodar com mais detalhes
pytest -v

# Rodar com cobertura
pytest --cov

# Gerar relatório HTML de cobertura
pytest --cov --cov-report=html
```

### Cobertura Atual

O projeto mantém **alta cobertura de testes** (85%+), testando:
- ✅ Geradores de dados (PersonGenerator, CompanyGenerator)
- ✅ Exportadores (JSON, CSV)
- ✅ Views e integrações
- ✅ API REST (endpoints, validações, formatos)
- ✅ Validações e casos de erro

### Estrutura de Testes

```
generator/tests/
├── test_generators.py    # Testes dos geradores
├── test_exporters.py     # Testes dos exportadores
├── test_views.py         # Testes das views
└── test_api.py           # Testes da API REST
```

## 🎯 Roadmap

### V0 (Atual)
- [x] Geração de pessoas
- [x] Geração de empresas
- [x] Exportação JSON/CSV
- [x] Interface básica
- [x] Testes automatizados (85%+ cobertura)
- [x] API REST v1
- [x] Documentação interativa (Swagger/ReDoc)

### V1 (Próximas funcionalidades)
- [ ] Mais tipos de dados (produtos, transações)
- [ ] Autenticação JWT na API
- [ ] Templates customizáveis
- [ ] Histórico de gerações
- [ ] CI/CD (GitHub Actions)
- [ ] Deploy em produção

### V2 (Futuro)
- [ ] Autenticação de usuários na interface
- [ ] Dashboard com estatísticas
- [ ] Geração em lote/agendada
- [ ] Webhooks

## 👩‍💻 Autora

Desenvolvido com 🤝 por Laura Bonilha

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!