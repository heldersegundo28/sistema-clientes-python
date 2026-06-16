import csv
def exportar(clientes,arquivo='clientes.csv'):
    with open(arquivo,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['id','nome','email','telefone']); w.writerows(clientes)