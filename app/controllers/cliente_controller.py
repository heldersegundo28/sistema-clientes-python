from app.models.database import conn
class ClienteController:
    def criar(self,n,e,t):
        c=conn(); c.execute('INSERT INTO clientes(nome,email,telefone) VALUES(?,?,?)',(n,e,t)); c.commit(); c.close()
    def listar(self):
        c=conn(); r=c.execute('SELECT * FROM clientes').fetchall(); c.close(); return r
    def atualizar(self,i,n,e,t):
        c=conn(); c.execute('UPDATE clientes SET nome=?,email=?,telefone=? WHERE id=?',(n,e,t,i)); c.commit(); c.close()
    def excluir(self,i):
        c=conn(); c.execute('DELETE FROM clientes WHERE id=?',(i,)); c.commit(); c.close()