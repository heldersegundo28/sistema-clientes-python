import customtkinter as ctk
from tkinter import ttk,messagebox
from app.models.database import init_db
from app.controllers.cliente_controller import ClienteController
from app.services.csv_service import exportar

init_db()
ctrl=ClienteController()

app=ctk.CTk()
app.title('Sistema de Clientes V2')
app.geometry('900x600')

nome=ctk.CTkEntry(app,placeholder_text='Nome'); nome.pack(pady=5)
email=ctk.CTkEntry(app,placeholder_text='Email'); email.pack(pady=5)
tel=ctk.CTkEntry(app,placeholder_text='Telefone'); tel.pack(pady=5)

tree=ttk.Treeview(app,columns=('id','nome','email','telefone'),show='headings')
for c in ('id','nome','email','telefone'): tree.heading(c,text=c)
tree.pack(fill='both',expand=True,pady=10)

def carregar():
    for i in tree.get_children(): tree.delete(i)
    for r in ctrl.listar(): tree.insert('', 'end', values=r)

def salvar():
    ctrl.criar(nome.get(),email.get(),tel.get())
    carregar()
    messagebox.showinfo('OK','Cliente cadastrado')

def excluir():
    sel=tree.selection()
    if sel:
        ctrl.excluir(tree.item(sel[0])['values'][0])
        carregar()

def csv():
    exportar(ctrl.listar())
    messagebox.showinfo('OK','CSV exportado')

ctk.CTkButton(app,text='Cadastrar',command=salvar).pack()
ctk.CTkButton(app,text='Excluir',command=excluir).pack()
ctk.CTkButton(app,text='Exportar CSV',command=csv).pack()

carregar()
app.mainloop()