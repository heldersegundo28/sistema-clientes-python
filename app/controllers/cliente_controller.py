"""Controlador para gerenciar operações de clientes."""

import re
import sqlite3
from typing import List, Tuple
from app.models.database import conn, close_connection
from app.config import EMAIL_PATTERN, MIN_TELEFONE_LENGTH, MENSAGENS
from app.services.log_service import log


class ClienteController:
    """Controlador para operações CRUD de clientes."""
    
    @staticmethod
    def _validar_email(email: str) -> bool:
        """Valida formato de email.
        
        Args:
            email: Email a validar.
            
        Returns:
            bool: True se email é válido, False caso contrário.
        """
        return re.match(EMAIL_PATTERN, email) is not None
    
    @staticmethod
    def _validar_telefone(telefone: str) -> bool:
        """Valida formato de telefone.
        
        Args:
            telefone: Telefone a validar.
            
        Returns:
            bool: True se telefone é válido, False caso contrário.
        """
        return len(telefone.replace(' ', '').replace('-', '')) >= MIN_TELEFONE_LENGTH
    
    @staticmethod
    def _validar_nome(nome: str) -> bool:
        """Valida formato de nome.
        
        Args:
            nome: Nome a validar.
            
        Returns:
            bool: True se nome é válido, False caso contrário.
        """
        return len(nome.strip()) >= 3
    
    def criar(self, nome: str, email: str, telefone: str) -> None:
        """Cria novo cliente.
        
        Args:
            nome: Nome do cliente.
            email: Email do cliente.
            telefone: Telefone do cliente.
            
        Raises:
            ValueError: Se dados forem inválidos.
            Exception: Se houver erro ao criar cliente.
        """
        nome = nome.strip()
        email = email.strip().lower()
        telefone = telefone.strip()
        
        if not nome or not email or not telefone:
            raise ValueError(MENSAGENS['campos_vazios'])
        
        if not self._validar_nome(nome):
            raise ValueError(MENSAGENS['nome_invalido'])
        
        if not self._validar_email(email):
            raise ValueError(MENSAGENS['email_invalido'])
        
        if not self._validar_telefone(telefone):
            raise ValueError(MENSAGENS['telefone_invalido'])
        
        connection = None
        try:
            connection = conn()
            connection.execute(
                'INSERT INTO clientes(nome, email, telefone) VALUES(?, ?, ?)',
                (nome, email, telefone)
            )
            connection.commit()
            log(f'Cliente criado: {nome} ({email})')
        except sqlite3.IntegrityError:
            raise ValueError('Email já cadastrado')
        except sqlite3.Error as err:
            log(f'Erro ao criar cliente: {err}')
            raise Exception(f'Erro ao criar cliente: {err}') from err
        finally:
            close_connection(connection)
    
    def listar(self) -> List[Tuple]:
        """Lista todos os clientes.
        
        Returns:
            List[Tuple]: Lista de clientes.
            
        Raises:
            Exception: Se houver erro ao listar.
        """
        connection = None
        try:
            connection = conn()
            cursor = connection.execute('SELECT * FROM clientes ORDER BY nome')
            clientes = cursor.fetchall()
            return clientes
        except sqlite3.Error as err:
            log(f'Erro ao listar clientes: {err}')
            raise Exception(f'Erro ao listar clientes: {err}') from err
        finally:
            close_connection(connection)
    
    def atualizar(self, cliente_id: int, nome: str, email: str, telefone: str) -> None:
        """Atualiza dados de um cliente.
        
        Args:
            cliente_id: ID do cliente.
            nome: Novo nome.
            email: Novo email.
            telefone: Novo telefone.
            
        Raises:
            ValueError: Se dados forem inválidos.
            Exception: Se houver erro ao atualizar.
        """
        nome = nome.strip()
        email = email.strip().lower()
        telefone = telefone.strip()
        
        if not nome or not email or not telefone:
            raise ValueError(MENSAGENS['campos_vazios'])
        
        if not self._validar_email(email):
            raise ValueError(MENSAGENS['email_invalido'])
        
        connection = None
        try:
            connection = conn()
            connection.execute(
                'UPDATE clientes SET nome=?, email=?, telefone=?, atualizado_em=CURRENT_TIMESTAMP WHERE id=?',
                (nome, email, telefone, cliente_id)
            )
            connection.commit()
            log(f'Cliente atualizado: ID {cliente_id}')
        except sqlite3.IntegrityError:
            raise ValueError('Email já cadastrado')
        except sqlite3.Error as err:
            log(f'Erro ao atualizar cliente: {err}')
            raise Exception(f'Erro ao atualizar cliente: {err}') from err
        finally:
            close_connection(connection)
    
    def excluir(self, cliente_id: int) -> None:
        """Exclui um cliente.
        
        Args:
            cliente_id: ID do cliente a excluir.
            
        Raises:
            Exception: Se houver erro ao excluir.
        """
        connection = None
        try:
            connection = conn()
            connection.execute('DELETE FROM clientes WHERE id=?', (cliente_id,))
            connection.commit()
            log(f'Cliente excluído: ID {cliente_id}')
        except sqlite3.Error as err:
            log(f'Erro ao excluir cliente: {err}')
            raise Exception(f'Erro ao excluir cliente: {err}') from err
        finally:
            close_connection(connection)