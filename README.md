# Pagamento

Ferramenta de linha de comando para calcular e gerar relatórios de produção e pagamento variável (freelancer e FH) a partir dos dados do Gmax (view `vBIAcoes` em um SQL Server). O sistema permite cadastrar atividades, pessoas, supervisores e metas, e gera relatórios em PDF e Excel consolidados por pessoa e por supervisor.

## Principais funcionalidades

- Cadastro de **Atividades** com:
  - ação (nome da atividade),
  - unidade de pagamento (NS ou US),
  - valor por unidade,
  - coluna de referência de US,
  - ações de redução e de comparação.

- Cadastro de **Pessoas**:
  - dados básicos (nome, matrícula, chave Pix, e‑mail);
  - associação de atividades (FH e freelancer);
  - cadastro de **meta** por pessoa, com diferentes formas de pagamento (Fixo, Excedente, Fixo+Excedente, ProducaoTotal).

- Cadastro de **Supervisores**:
  - dados básicos (nome, matrícula, e‑mail, pasta de saída);
  - associação de pessoas ao supervisor.

- Geração de relatórios:
  - **Relação Gmax por supervisor** (produção por pessoa/atividade) em PDF e Excel;
  - **Relatórios de metas** por pessoa (PDF), também replicados nas pastas dos supervisores por período.

Os cadastros são armazenados localmente para reaproveitamento entre execuções.

## Arquitetura geral

- `main.py` – ponto de entrada do sistema e menu principal.
- `ControllerAtividade.py`, `ControllerPessoa.py`, `ControllerSupervisor.py`, `ControllerAcoesConcGmax.py`, `ControllerMeta.py` – camada de controle (regras de negócio e navegação de menus).
- `Atividade.py`, `Pessoa.py`, `Supervisor.py`, `Meta.py`, `AcoesConcGmax.py` – modelos de domínio.
- `MenuSimples.py` – componente simples de menu de texto.
- `Utils.py` – utilitários para leitura de floats, formatação e geração dos PDFs/Excel.
- `DatabaseHandler.py` – encapsula a conexão com o SQL Server (pyodbc + SQLAlchemy).
- `requirements.txt` – dependências Python do projeto.
- `setup.bat` – script de configuração do ambiente virtual e dependências.
- `Executavel.bat` – script para ativar o ambiente virtual e executar o sistema.

## Requisitos

- **Sistema operacional**: Windows (os scripts `.bat` e a dependência `pywin32` são específicos de Windows).
- **Python**: 3.x instalado e disponível no `PATH`.
- **Banco de dados**:
  - SQL Server acessível na rede com a view `vBIAcoes` (utilizada por `AcoesConcGmax`).
  - Driver **ODBC Driver 18 for SQL Server** instalado.
- **Bibliotecas Python**: serão instaladas automaticamente pelo `setup.bat` a partir de `requirements.txt`:
  - `pyodbc`
  - `sqlalchemy`
  - `pandas`
  - `openpyxl`
  - `reportlab`
  - `xlsxwriter`
  - `PyPDF2`
  - `pywin32`

Além disso, é necessário ter permissão de leitura no banco e permissão de escrita nas pastas onde os relatórios serão gerados.

## Scripts de automação

### `setup.bat`

Script para preparar o ambiente de execução. Ele executa:

```bat
python -m venv venv
call .\venv\scripts\activate.bat
pip install -r requirements.txt
mkdir exported_data
mkdir compressed_data
pause
```

Ou seja, ele:

1. Cria um ambiente virtual Python na pasta `venv`.
2. Ativa o ambiente virtual.
3. Instala as dependências listadas em `requirements.txt`.
4. Cria as pastas:
   - `exported_data` – onde serão salvos os PDFs e arquivos Excel gerados.
   - `compressed_data` – onde serão salvos os arquivos `.pkl` com os cadastros.
5. Faz uma pausa ao final para que você possa ver possíveis mensagens de erro.

> Execute este script **apenas na primeira vez** (ou quando quiser recriar o ambiente).

### `Executavel.bat`

Script para iniciar o sistema já dentro do ambiente virtual:

```bat
call .\venv\scripts\activate.bat
python main.py
pause
```

Ele ativa a `venv`, roda `main.py` e, ao final, mantém a janela aberta para visualização de mensagens.

> Este é o script recomendado para uso diário do sistema.

## Como executar

1. **Clonar ou copiar** o projeto para uma pasta local no Windows.
2. Certificar‑se de que o Python 3.x está instalado e o **ODBC Driver 18 for SQL Server** também.
3. Abrir o **Prompt de Comando** na pasta do projeto.
4. Rodar o script de configuração (apenas na primeira vez):

   ```bat
   setup.bat
   ```

5. Após a configuração, sempre que quiser utilizar o sistema, execute:

   ```bat
   Executavel.bat
   ```

6. O menu principal será exibido no terminal.

## Uso do sistema (visão geral)

No menu principal (`main.py`) você terá as opções:

1. **Menu de Atividades**
   - Cadastrar, remover, alterar e listar atividades.
2. **Menu de Pessoas**
   - Cadastrar, remover, alterar e listar pessoas.
   - Atribuir/remover atividades.
   - Cadastrar/alterar/remover metas por pessoa.
3. **Menu de Supervisores**
   - Cadastrar, remover, alterar e listar supervisores.
   - Associar/remover pessoas sob supervisão.
4. **Gerar Relação Gmax**
   - Solicita data inicial e final.
   - Gera PDFs e um Excel consolidado com a produção por pessoa, organizados nas pastas dos supervisores (por período) e/ou em `exported_data`.
5. **Gerar Metas**
   - Solicita data inicial e final.
   - Calcula a produção relacionada às metas configuradas e gera relatórios de metas em PDF por pessoa, salvos em `exported_data` e nas pastas dos supervisores por período.
6. **Salvar e Sair**
   - Persiste as listas de atividades, pessoas e supervisores em arquivos `.pkl` dentro de `compressed_data` e encerra o programa.
7. **Sair sem Salvar**
   - Encerra o programa sem alterar os arquivos de dados.

## Persistência de dados

- `compressed_data/lista_atividades.pkl` – atividades cadastradas.
- `compressed_data/lista_pessoas.pkl` – pessoas cadastradas (com atividades e metas).
- `compressed_data/lista_supervisores.pkl` – supervisores cadastrados (com pessoas associadas).

Esses arquivos são carregados automaticamente na inicialização do sistema, se existirem.

## Geração de relatórios

Os relatórios são gerados a partir dos dados retornados da view `vBIAcoes` do SQL Server:

- Para **produção por pessoa/supervisor** (`gerar_producao_por_supervisor`):
  - PDFs individuais por pessoa com o detalhamento por NS, serviço, ação, data de conclusão, US, reduções, comparações e valor a pagar.
  - Arquivo Excel com uma aba por pessoa.

- Para **metas** (`gerar_pagamento_metas`):
  - Calcula a produção total na unidade configurada na meta (NS ou soma de colunas de US).
  - Aplica a regra de pagamento definida (Fixo, Excedente, Fixo+Excedente, ProducaoTotal).
  - Gera PDFs de resumo da meta + detalhamento da produção usada no cálculo.

Relatórios são salvos em:

- `exported_data/` – saída padrão generalista.
- `<pasta_do_supervisor>/<AAAA-MM-DD>_a_<AAAA-MM-DD>/` – relatórios por supervisor e período.

## Configuração do banco de dados

A conexão com o SQL Server é centralizada em `DatabaseHandler.py`. Para apontar para outro servidor, base, usuário ou senha, ajuste os parâmetros utilizados em:

- `AcoesConcGmax.py` (instanciação de `DatabaseHandler`).

É recomendável, em produção, mover as credenciais para variáveis de ambiente ou um arquivo de configuração externo.

---

Autor: **Caio Cezar Dias**  
Contato: **caiocd007@gmail.com**