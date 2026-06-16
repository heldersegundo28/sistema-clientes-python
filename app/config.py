"""Arquivo de configuração da aplicação."""

import os

# Banco de dados
DATABASE_PATH = 'clientes.db'

# Logs
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'sistema.log')

# Exportação
CSV_FILENAME = 'clientes.csv'

# Validações
EMAIL_PATTERN = r'^[^@]+@[^@]+\.[^@]+$'
MIN_TELEFONE_LENGTH = 10

# Interface Gráfica
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WINDOW_TITLE = 'Sistema de Gestão de Clientes v2.0'

# Mensagens de validação
MENSAGENS = {
    'campos_vazios': 'Por favor, preencha todos os campos.',
    'nome_invalido': 'Nome deve ter no mínimo 3 caracteres.',
    'email_invalido': 'Email inválido. Use o formato: exemplo@dominio.com',
    'telefone_invalido': f'Telefone deve ter no mínimo {MIN_TELEFONE_LENGTH} caracteres.',
    'cliente_nao_selecionado': 'Por favor, selecione um cliente.',
    'nenhum_cliente': 'Nenhum cliente cadastrado.',
    'nenhum_cliente_exportar': 'Não há clientes para exportar.',
    'confirmacao_excluir': 'Tem certeza que deseja excluir este cliente?',
}

# Temas
THEME_COLOR = '#2b2b2b'
