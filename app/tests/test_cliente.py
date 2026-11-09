"""Testes para o controlador de clientes."""

import unittest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.controllers.cliente_controller import ClienteController
from app.models.database import init_db, conn, close_connection


class TestClienteController(unittest.TestCase):
    """Testes para o ClienteController."""
    
    def setUp(self):
        """Cada teste usa seu próprio banco e diretório de logs temporários."""
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        banco = patch('app.models.database.DATABASE_PATH', str(Path(pasta.name) / 'clientes.db'))
        banco.start()
        self.addCleanup(banco.stop)
        logs = patch('app.services.log_service.LOG_DIR', pasta.name)
        logs.start()
        self.addCleanup(logs.stop)
        arquivo_log = patch('app.services.log_service.LOG_FILE', str(Path(pasta.name) / 'teste.log'))
        arquivo_log.start()
        self.addCleanup(arquivo_log.stop)
        self.ctrl = ClienteController()
        init_db()
    
    # Testes de validação de email
    def test_validar_email_valido(self):
        """Testa validação com email válido."""
        self.assertTrue(self.ctrl._validar_email('usuario@exemplo.com'))
        self.assertTrue(self.ctrl._validar_email('test.email@dominio.co.uk'))
    
    def test_validar_email_invalido(self):
        """Testa validação com email inválido."""
        self.assertFalse(self.ctrl._validar_email('email_invalido'))
        self.assertFalse(self.ctrl._validar_email('email@'))
        self.assertFalse(self.ctrl._validar_email('@dominio.com'))
    
    # Testes de validação de telefone
    def test_validar_telefone_valido(self):
        """Testa validação com telefone válido."""
        self.assertTrue(self.ctrl._validar_telefone('11999999999'))
        self.assertTrue(self.ctrl._validar_telefone('(11) 99999-9999'))
    
    def test_validar_telefone_invalido(self):
        """Testa validação com telefone inválido."""
        self.assertFalse(self.ctrl._validar_telefone('123'))
    
    # Testes de validação de nome
    def test_validar_nome_valido(self):
        """Testa validação com nome válido."""
        self.assertTrue(self.ctrl._validar_nome('João Silva'))
    
    def test_validar_nome_invalido(self):
        """Testa validação com nome inválido."""
        self.assertFalse(self.ctrl._validar_nome('Jo'))
    
    # Testes de criação
    def test_criar_cliente_valido(self):
        """Testa criação de cliente com dados válidos."""
        self.ctrl.criar('João Silva', 'joao@email.com', '11999999999')
        clientes = self.ctrl.listar()
        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0][1], 'João Silva')
    
    def test_criar_cliente_email_duplicado(self):
        """Testa criação com email duplicado."""
        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        with self.assertRaises(ValueError):
            self.ctrl.criar('Maria', 'joao@email.com', '11988888888')
    
    def test_criar_cliente_campos_vazios(self):
        """Testa criação com campos vazios."""
        with self.assertRaises(ValueError):
            self.ctrl.criar('', 'joao@email.com', '11999999999')
    
    def test_criar_cliente_email_invalido(self):
        """Testa criação com email inválido."""
        with self.assertRaises(ValueError):
            self.ctrl.criar('João', 'email_invalido', '11999999999')
    
    def test_criar_cliente_telefone_invalido(self):
        """Testa criação com telefone inválido."""
        with self.assertRaises(ValueError):
            self.ctrl.criar('João', 'joao@email.com', '123')
    
    # Testes de listagem
    def test_listar_clientes(self):
        """Testa listagem de múltiplos clientes."""
        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        self.ctrl.criar('Maria', 'maria@email.com', '11988888888')
        clientes = self.ctrl.listar()
        self.assertEqual(len(clientes), 2)
    
    def test_atualizar_cliente(self):
        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        cliente_id = self.ctrl.listar()[0][0]
        self.ctrl.atualizar(cliente_id, 'Maria Silva', ' MARIA@EMAIL.COM ', '11988888888')
        cliente = self.ctrl.listar()[0]
        self.assertEqual(cliente[1:4], ('Maria Silva', 'maria@email.com', '11988888888'))

    def test_atualizar_rejeita_nome_e_telefone_invalidos(self):
        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        cliente_id = self.ctrl.listar()[0][0]
        for nome, telefone in [('Jo', '11999999999'), ('João', 'abcdefghijk')]:
            with self.subTest(nome=nome, telefone=telefone), self.assertRaises(ValueError):
                self.ctrl.atualizar(cliente_id, nome, 'joao@email.com', telefone)
        self.assertEqual(self.ctrl.listar()[0][1], 'João')

    def test_atualizar_rejeita_email_duplicado(self):
        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        self.ctrl.criar('Maria', 'maria@email.com', '11988888888')
        cliente_id = self.ctrl.listar()[0][0]
        with self.assertRaises(ValueError):
            self.ctrl.atualizar(cliente_id, 'João', 'maria@email.com', '11999999999')

    def test_telefone_rejeita_letras(self):
        self.assertFalse(self.ctrl._validar_telefone('abcdefghijk'))

    def test_exportacao_tem_cabecalho_alinhado(self):
        import csv
        from app.services.csv_service import exportar

        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'clientes.csv'
            exportar(self.ctrl.listar(), arquivo)
            with arquivo.open(encoding='utf-8', newline='') as fonte:
                linhas = list(csv.reader(fonte))
        self.assertEqual(len(linhas[0]), 6)
        self.assertEqual(len(linhas[0]), len(linhas[1]))
        self.assertEqual(linhas[1][1], 'João')

    # Testes de exclusão
    def test_excluir_cliente(self):
        """Testa exclusão de cliente."""
        self.ctrl.criar('João', 'joao@email.com', '11999999999')
        clientes = self.ctrl.listar()
        cliente_id = clientes[0][0]
        self.ctrl.excluir(cliente_id)
        clientes = self.ctrl.listar()
        self.assertEqual(len(clientes), 0)


if __name__ == '__main__':
    unittest.main()
