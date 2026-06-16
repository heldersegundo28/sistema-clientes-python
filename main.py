"""Aplicação principal de gestão de clientes com interface gráfica."""

import customtkinter as ctk
from tkinter import ttk, messagebox
from app.models.database import init_db
from app.controllers.cliente_controller import ClienteController
from app.services.csv_service import exportar
from app.services.log_service import log
from app.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    MENSAGENS
)


class SistemaClientes:
    """Classe principal da aplicação de gestão de clientes."""
    
    def __init__(self):
        """Inicializa a aplicação."""
        self.ctrl = ClienteController()
        self.app = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        self.carregar_dados()
        log('Aplicação iniciada')
    
    def setup_window(self) -> None:
        """Configura a janela principal."""
        self.app.title(WINDOW_TITLE)
        self.app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.app.resizable(False, False)
    
    def create_widgets(self) -> None:
        """Cria os widgets da interface gráfica."""
        # Frame superior para entrada de dados
        frame_entrada = ctk.CTkFrame(self.app)
        frame_entrada.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(frame_entrada, text='Nome:').pack(anchor='w')
        self.nome = ctk.CTkEntry(frame_entrada, placeholder_text='Digite o nome')
        self.nome.pack(fill='x', pady=(0, 5))
        
        ctk.CTkLabel(frame_entrada, text='Email:').pack(anchor='w')
        self.email = ctk.CTkEntry(frame_entrada, placeholder_text='exemplo@dominio.com')
        self.email.pack(fill='x', pady=(0, 5))
        
        ctk.CTkLabel(frame_entrada, text='Telefone:').pack(anchor='w')
        self.tel = ctk.CTkEntry(frame_entrada, placeholder_text='(XX) XXXXX-XXXX')
        self.tel.pack(fill='x', pady=(0, 10))
        
        # Frame para botões de ação
        frame_botoes = ctk.CTkFrame(frame_entrada)
        frame_botoes.pack(fill='x', pady=(0, 10))
        
        ctk.CTkButton(
            frame_botoes,
            text='Cadastrar',
            command=self.salvar,
            width=280
        ).pack(side='left', padx=(0, 5))
        
        ctk.CTkButton(
            frame_botoes,
            text='Limpar',
            command=self.limpar_campos,
            width=280
        ).pack(side='left')
        
        # Treeview para exibir clientes
        frame_tabela = ctk.CTkFrame(self.app)
        frame_tabela.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.tree = ttk.Treeview(
            frame_tabela,
            columns=('id', 'nome', 'email', 'telefone'),
            show='headings',
            height=15
        )
        
        # Configuração das colunas
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('email', text='Email')
        self.tree.heading('telefone', text='Telefone')
        
        self.tree.column('id', width=30, anchor='center')
        self.tree.column('nome', width=200, anchor='w')
        self.tree.column('email', width=250, anchor='w')
        self.tree.column('telefone', width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame inferior com botões
        frame_rodape = ctk.CTkFrame(self.app)
        frame_rodape.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkButton(
            frame_rodape,
            text='Excluir Selecionado',
            command=self.excluir,
            fg_color='#cc0000'
        ).pack(side='left', padx=(0, 5))
        
        ctk.CTkButton(
            frame_rodape,
            text='Exportar CSV',
            command=self.exportar_csv
        ).pack(side='left')
    
    def carregar_dados(self) -> None:
        """Carrega dados de clientes na tabela."""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            clientes = self.ctrl.listar()
            if not clientes:
                log('Nenhum cliente cadastrado')
                return
            
            for cliente in clientes:
                self.tree.insert('', 'end', values=cliente)
        except Exception as err:
            log(f'Erro ao carregar dados: {err}')
            messagebox.showerror('Erro', f'Erro ao carregar clientes: {err}')
    
    def limpar_campos(self) -> None:
        """Limpa os campos de entrada."""
        self.nome.delete(0, 'end')
        self.email.delete(0, 'end')
        self.tel.delete(0, 'end')
        self.nome.focus()
    
    def salvar(self) -> None:
        """Cadastra um novo cliente."""
        try:
            nome = self.nome.get().strip()
            email = self.email.get().strip()
            telefone = self.tel.get().strip()
            
            self.ctrl.criar(nome, email, telefone)
            
            self.carregar_dados()
            self.limpar_campos()
            messagebox.showinfo('Sucesso', 'Cliente cadastrado com sucesso!')
        
        except ValueError as err:
            messagebox.showwarning('Aviso', str(err))
            log(f'Validação: {err}')
        except Exception as err:
            messagebox.showerror('Erro', f'Erro ao cadastrar: {err}')
            log(f'Erro ao cadastrar: {err}')
    
    def excluir(self) -> None:
        """Exclui o cliente selecionado."""
        try:
            selecao = self.tree.selection()
            if not selecao:
                messagebox.showwarning('Aviso', MENSAGENS['cliente_nao_selecionado'])
                return
            
            cliente_id = self.tree.item(selecao[0])['values'][0]
            cliente_nome = self.tree.item(selecao[0])['values'][1]
            
            if messagebox.askyesno('Confirmar', MENSAGENS['confirmacao_excluir']):
                self.ctrl.excluir(cliente_id)
                self.carregar_dados()
                messagebox.showinfo('Sucesso', f'Cliente "{cliente_nome}" excluído!')
        
        except Exception as err:
            messagebox.showerror('Erro', f'Erro ao excluir: {err}')
            log(f'Erro ao excluir: {err}')
    
    def exportar_csv(self) -> None:
        """Exporta os dados para CSV."""
        try:
            clientes = self.ctrl.listar()
            if not clientes:
                messagebox.showwarning('Aviso', MENSAGENS['nenhum_cliente_exportar'])
                return
            
            exportar(clientes)
            messagebox.showinfo('Sucesso', f'{len(clientes)} cliente(s) exportado(s)!')
        
        except Exception as err:
            messagebox.showerror('Erro', f'Erro ao exportar: {err}')
            log(f'Erro ao exportar: {err}')
    
    def executar(self) -> None:
        """Inicia a aplicação."""
        self.app.mainloop()


if __name__ == '__main__':
    try:
        init_db()
        app = SistemaClientes()
        app.executar()
    except Exception as err:
        log(f'Erro ao iniciar aplicação: {err}')
        messagebox.showerror('Erro Fatal', f'Erro ao iniciar: {err}')