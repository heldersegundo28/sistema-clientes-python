"""Serviço de logging para registro de eventos do sistema."""

import os
from datetime import datetime
from app.config import LOG_DIR, LOG_FILE


def _criar_diretorio_logs() -> None:
    """Cria diretório de logs se não existir."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log(mensagem: str) -> None:
    """Registra mensagem no arquivo de log.
    
    Args:
        mensagem: Mensagem a registrar.
    """
    try:
        _criar_diretorio_logs()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {mensagem}\n')
    except Exception as err:
        # Falha silenciosa para não interromper o programa
        print(f'Aviso: não foi possível registrar log: {err}')


def limpar_logs() -> None:
    """Limpa o arquivo de log."""
    try:
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, 'w').close()
            log('Arquivo de log limpo')
    except Exception as err:
        print(f'Erro ao limpar logs: {err}')