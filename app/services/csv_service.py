"""Serviço para exportar dados de clientes em formato CSV."""

import csv
from typing import List, Tuple
from app.services.log_service import log
from app.config import CSV_FILENAME


def exportar(clientes: List[Tuple], arquivo: str = CSV_FILENAME) -> None:
    """Exporta lista de clientes para arquivo CSV.
    
    Args:
        clientes: Lista de clientes a exportar.
        arquivo: Caminho do arquivo CSV (padrão: 'clientes.csv').
        
    Raises:
        ValueError: Se lista de clientes estiver vazia.
        Exception: Se houver erro ao exportar.
    """
    if not clientes:
        raise ValueError('Nenhum cliente para exportar')
    
    try:
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Nome', 'Email', 'Telefone', 'Criado em'])
            writer.writerows(clientes)
        
        log(f'Sucesso: {len(clientes)} cliente(s) exportado(s) para {arquivo}')
    except IOError as err:
        log(f'Erro ao exportar CSV: {err}')
        raise Exception(f'Erro ao exportar CSV: {err}') from err