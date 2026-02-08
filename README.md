# 🎲 Fake Data Generator

Gerador de dados fake para testes e desenvolvimento, criado com Django e Python.

## 📋 Sobre o Projeto

O **Fake Data Generator** é uma ferramenta web robusta desenvolvida para simplificar a criação de dados realistas para ambientes de desenvolvimento, QA e testes de software. O projeto evoluiu para uma plataforma completa com sistema de usuários e rastreamento de histórico.

## ✨ Funcionalidades

### 🔐 Autenticação e Usuários
- **Cadastro e Login**: Sistema seguro usando o *Django Auth System*.
- **Gestão de Sessão**: Controle de acesso para funcionalidades exclusivas.
- **Interface Premium**: Telas de login e cadastro integradas ao design system do projeto.

### 📜 Histórico de Gerações
- **Tracking Automático**: Registra todas as operações de geração feitas por usuários logados.
- **Detalhamento**: Salva tipo de dado, quantidade, data/hora e formato de saída (JSON/CSV/Preview).
- **Dashboard Pessoal**: Tela exclusiva para cada usuário visualizar seus registros passados.

### 🏭 Geradores de Dados
- ✅ **Pessoas**: Nome completo, CPF, RG, email, telefone, endereço completo.
- ✅ **Empresas**: CNPJ, razão social, nome fantasia, contatos.
- ✅ **Integrações Externas**:
  - **PokéAPI**: Dados reais de Pokémons com stats e imagens.
  - **Dog API**: Raças e imagens de cães.

### 📤 Exportação e Formatos
- **Preview em Tempo Real**: Visualize os dados na tela antes de baixar.
- **JSON**: Estrutura limpa e pronta para uso em APIs.
- **CSV**: Ideal para importação em planilhas e bancos de dados.

### ⚡ Arquitetura Assíncrona (Alta Performance)
- **Non-blocking I/O**: Refatoração completa para `async/await` usando `httpx`.
- **Concorrência Real**: Geração de múltiplos Pokémons/Dogs simultaneamente (redução de tempo de ~25s para ~1s em cargas médias).
- **Resiliência**: Tratamento robusto de timeouts e falhas de API com fallback automático.

## 🛠️ Destaques Técnicos (Arquitetura)

O projeto segue a arquitetura **MVT (Model-View-Template)** do Django, combinada com padrões modernos de desenvolvimento assíncrono:

1.  **`generator` (Core):**
    *   **Async Generators:** Integrações externas escritas com `asyncio` e `httpx`.
    *   **Strategy Pattern:** Para os exportadores de dados (CSV/JSON).
2.  **`accounts`:** Gerencia todo o fluxo de autenticação e sessões.
3.  **`history`:** Implementa persistência de dados.

### Tecnologias e Bibliotecas
- **Python 3.11+** & **Django 5.0** (Suporte a Views Async)
- **Django REST Framework**
- **HTTPX** & **AsyncIO**: Cliente HTTP assíncrono de alta performance.
- **Faker**: Geração de dados dummy local.
- **pytest-asyncio**: Testes automatizados para coroutines.
- **Bootstrap 5**: Frontend responsivo.

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/laurabonilha/fake-data-generator.git
cd fake-data-generator
```

2. **Crie e ative o ambiente virtual:**
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Prepare o Banco de Dados:**
```bash
# Executa as migrações (cria tabelas de usuários, histórico, etc)
python manage.py migrate
```

5. **Inicie o servidor:**
```bash
python manage.py runserver
```

6. **Acesse:**
- Interface Web: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/v1/docs/`

## 📦 Estrutura do Projeto

A organização modular facilita a escalabilidade e manutenção:

```
fake-data-generator/
├── config/                 # Configurações globais do Django
├── accounts/               # [NOVO] Gestão de usuários e autenticação
│   ├── forms.py            # Formulários customizados com Bootstrap
│   └── views.py            # Lógica de login/registro
├── history/                # [NOVO] Histórico e persistência
│   ├── models.py           # Model GenerationHistory
│   └── views.py            # Dashboard de histórico
├── generator/              # App principal (Core)
│   ├── generators/         # Lógica de geração (Pessoa, Empresa)
│   ├── exporters/          # Lógica de exportação (JSON, CSV)
│   ├── external/           # Clientes HTTP para APIs externas
│   └── api/                # Endpoints REST
├── static/                 # Assets (CSS, JS, Imagens)
├── manage.py
└── requirements.txt
```

## 🧪 Qualidade de Código e Testes

O projeto mantém rigoroso controle de qualidade:
- **Testes Unitários:** Validam geradores e exportadores isoladamente.
- **Testes de Integração:** Validam fluxos de API e Views.
- **Cobertura:** +85% de coverage garantido.

Para rodar os testes:
```bash
pytest --cov --cov-report=term-missing
```

## 🎯 Roadmap

### ✅ Concluído
- [x] Geração de pessoas e empresas (Faker)
- [x] Integração com APIs externas (Pokémon/Dog)
- [x] Exportação JSON/CSV e Preview
- [x] API REST documentada (Swagger)
- [x] **Sistema de Login e Cadastro de Usuários**
- [x] **Histórico de Gerações persistente**
- [x] **Assincronismo:** Refatoração completa com `httpx/asyncio` e views `async`.

### 🚧 Próximos Passos (V2.0 - Performance & Features)
- [ ] **Background Tasks:** Implementar Celery/Redis para gerações massivas (>10k registros).
- [ ] **Docker:** Containerização completa da aplicação e banco.
- [ ] **CI/CD:** Pipelines de teste e deploy automático (GitHub Actions).

## 👩‍💻 Autora

Desenvolvido com 💜 por **Laura Bonilha**

Esta ferramenta foi criada com foco em **Boas Práticas de Engenharia de Software**, demonstrando arquitetura limpa, testes automatizados e evolução consistente de produto.

---

⭐ **Gostou do projeto?** Se ele foi útil para você ou serviu de referência, considere dar uma estrela no repositório!