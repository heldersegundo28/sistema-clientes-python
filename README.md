# Sistema de Gestão de Clientes v2.0

Uma aplicação desktop moderna para gerenciar clientes com interface gráfica intuitiva, desenvolvida com Python e customtkinter.

## ✨ Funcionalidades

- ✅ **Cadastro de Clientes** - Adicione novos clientes com validação de dados
- ✅ **Listagem** - Visualize todos os clientes em uma tabela interativa
- ✅ **Edição** - Atualize dados de clientes existentes
- ✅ **Exclusão** - Remova clientes com confirmação
- ✅ **Exportação** - Exporte dados para arquivo CSV
- ✅ **Validações** - Email e telefone são validados automaticamente
- ✅ **Logging** - Registro detalhado de todas as operações
- ✅ **Banco de Dados** - Persistência de dados em SQLite

## 🛠️ Tecnologias

- **Python 3.12+**
- **customtkinter** - Interface gráfica moderna
- **SQLite** - Banco de dados local
- **unittest** - Testes automatizados

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. Clone ou baixe o projeto:
```bash
git clone https://github.com/heldersegundo28/sistema-clientes-python.git
cd sistema-clientes-python
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Executar a Aplicação

```bash
python main.py
```

### Executar Testes

```bash
python -m unittest app.tests.test_cliente -v
```

## 📁 Estrutura do Projeto

```
sistema-clientes-python/
├── main.py                          # Arquivo principal
├── requirements.txt                 # Dependências
├── README.md                        # Documentação
├── .gitignore                       # Arquivos ignorados
├── app/
│   ├── config.py                    # Configurações
│   ├── controllers/
│   │   └── cliente_controller.py    # Lógica de negócio
│   ├── models/
│   │   └── database.py              # Banco de dados
│   ├── services/
│   │   ├── csv_service.py           # Exportação CSV
│   │   └── log_service.py           # Logging
│   └── tests/
│       └── test_cliente.py          # Testes
└── logs/
    └── sistema.log                  # Logs de operações
```

## ✔️ Validações

- **Email**: Formato válido, sem duplicatas, normalizado para minúsculas
- **Telefone**: Mínimo 10 caracteres
- **Nome**: Mínimo 3 caracteres

## 🧪 Testes

```bash
python -m unittest app.tests.test_cliente -v
```

Cobertura: 9+ testes automatizados

## 📝 Principais Classes

### ClienteController
Gerencia operações CRUD de clientes com validações robustas

### DatabaseManager
Gerencia conexões e operações com SQLite

### SistemaClientes (GUI)
Interface gráfica com customtkinter

## 📊 Exemplo de Uso

```python
from app.controllers.cliente_controller import ClienteController

ctrl = ClienteController()
ctrl.criar('João Silva', 'joao@email.com', '11999999999')
clientes = ctrl.listar()
```

## 🐛 Tratamento de Erros

Todos os erros são capturados e logados em `logs/sistema.log`

## 📄 Licença

MIT