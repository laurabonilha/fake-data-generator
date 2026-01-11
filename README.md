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

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Django 5.0**
- **Faker** - Geração de dados fake
- **Bootstrap 5** - Framework CSS
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
http://localhost:8000
```

## 📦 Estrutura do Projeto

```
fake-data-generator/
├── config/                 # Configurações do Django
├── generator/              # App principal
│   ├── generators/         # Geradores de dados
│   ├── exporters/          # Exportadores (JSON, CSV)
|   ├── migrations          # Migrações Django
│   ├── templates/          # Templates HTML
│   └── views.py            # Views
├── static/                 # Arquivos estáticos
├── manage.py
├── requirements.txt
└── README.md
```

## 🎯 Roadmap

### V0 (Atual)
- [x] Geração de pessoas
- [x] Geração de empresas
- [x] Exportação JSON/CSV
- [x] Interface básica

### V1 (Próximas funcionalidades)
- [ ] API REST
- [ ] Mais tipos de dados (produtos, transações)
- [ ] Templates customizáveis
- [ ] Histórico de gerações
- [ ] Testes automatizados

### V2 (Futuro)
- [ ] Autenticação de usuários
- [ ] Dashboard com estatísticas
- [ ] Geração em lote/agendada

## 👩‍💻 Autora

Desenvolvido com 🤝 por Laura Bonilha

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!