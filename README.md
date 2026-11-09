# Sistema de gestão de clientes

Aplicação desktop de portfólio para cadastrar, consultar e excluir clientes, persistir dados em SQLite e exportá-los para CSV.

**Tecnologias:** Python, CustomTkinter, SQLite e unittest.

## Funcionalidades e escopo

| Recurso | Disponibilidade |
| --- | --- |
| Cadastro, listagem e exclusão com confirmação | Interface gráfica |
| Validação de nome, e-mail e telefone | Controlador |
| Normalização de e-mail e bloqueio de duplicatas | Controlador e SQLite |
| Atualização de dados | API Python do controlador |
| Exportação CSV com datas de criação e atualização | Interface e serviço |
| Testes com banco e logs temporários | Suíte automatizada |

A interface ainda não possui formulário de edição. A atualização está implementada em `ClienteController.atualizar()` e coberta por testes.

## Executar localmente

Use Python 3.12 e Git, em um ambiente com interface gráfica e Tk disponível.

~~~bash
git clone https://github.com/heldersegundo28/sistema-clientes-python.git
cd sistema-clientes-python
python -m venv .venv
~~~

Ative no PowerShell:

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

No Linux/macOS, use `source .venv/bin/activate`.

~~~bash
python -m pip install -r requirements.txt
python main.py
~~~

No Linux, o Tk pode precisar ser instalado pelo gerenciador de pacotes da distribuição.

## Uso e dados locais

1. Preencha nome, e-mail e telefone e clique em **Cadastrar**.
2. Consulte os registros na tabela.
3. Selecione um cliente para excluí-lo, confirmando a operação.
4. Use **Exportar CSV** para gerar `clientes.csv`.

O banco `clientes.db` e os logs são criados no diretório de execução. Os parâmetros ficam em `app/config.py`. O arquivo `.env.example` é apenas uma referência e não é carregado automaticamente nesta versão.

## Testes

~~~bash
python -m unittest discover -s app/tests -v
~~~

Cada teste usa um banco temporário separado do banco da aplicação. A suíte verifica cadastro, normalização e duplicidade de e-mail, atualização, validações, exclusão e alinhamento das colunas do CSV.

## Organização

| Caminho | Responsabilidade |
| --- | --- |
| `main.py` | Interface e inicialização |
| `app/controllers/cliente_controller.py` | Operações e validações |
| `app/models/database.py` | Conexão e criação da tabela SQLite |
| `app/services/` | Exportação CSV e logs |
| `app/tests/` | Testes automatizados |

Exemplo do controlador, em um diretório de demonstração:

~~~python
from app.models.database import init_db
from app.controllers.cliente_controller import ClienteController

init_db()
ctrl = ClienteController()
ctrl.criar("Cliente Exemplo", "cliente@example.com", "11999999999")
cliente_id = ctrl.listar()[0][0]
ctrl.atualizar(cliente_id, "Cliente Atualizado", "cliente@example.com", "11988888888")
~~~

## Limitações

Aplicação local para estudo, sem autenticação, controle de acesso ou implantação como serviço web. O telefone é validado pelo formato e quantidade mínima de dígitos, sem consultar a existência da linha. O Dockerfile existente não configura uma sessão gráfica; a execução desktop recomendada é local.

Licença: [MIT](LICENSE).
