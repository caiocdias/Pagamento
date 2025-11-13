from shutil import make_archive

from View import MenuSimples
from Model import Meta
from Generic import read_float


class ControllerMeta:
    def __init__(self):
        pass

    @staticmethod
    def cadastrar():
        acoes = []
        while True:
            acao = input("Digite uma ação para adicionar a meta, deixe vazio para sair: ")
            if acao == "":
                break
            acoes.append(acao)

        meta = read_float("Entre com o valor da meta: ", min_=0)
        opcoes_unidade = Meta.get_coluna_us_options()
        opcao_unidade_selecionada = MenuSimples("Unidade de Pagamento", opcoes_unidade).choose(include_exit=False)
        unidade = opcoes_unidade[opcao_unidade_selecionada]

        colunas = []
        if unidade == "US":
            while True:
                coluna = input("Digite a coluna para , deixe vazio para sair: ")
                if coluna == "":
                    break
                colunas.append(coluna)

        opcoes_forma_pagamento = Meta.get_forma_pagamento_options()
        opcao_forma_pagamento_selecionada = MenuSimples("Forma de Pagamento", opcoes_forma_pagamento).choose(include_exit=False)
        forma_pagamento = opcoes_forma_pagamento[opcao_forma_pagamento_selecionada]

        fator_excedente = None
        if forma_pagamento in ("Excedente", "Fixo+Excedente"):
            fator_excedente = read_float("Fator a ser pago por undidade excedente: ",0)

        valor_fixo = None
        if forma_pagamento in ("Fixo", "Fixo+Excedente"):
            valor_fixo = read_float("Valor fixo a ser pago", 0)

        fator_producao_total = None
        if forma_pagamento == "ProducaoTotal":
            fator_producao_total = read_float("Fator a ser pago pela produção total: ",0)

        meta = Meta(meta, unidade, forma_pagamento, fator_excedente, valor_fixo, fator_producao_total, acoes, colunas)
        return meta

    @staticmethod
    def alterar(meta: Meta):
        if not isinstance(meta, Meta):
            raise TypeError(f"Objeto meta é do tipo [{type(meta).__name__}] e não uma instância de Meta.")

        opcoes_alterar = ["Meta", "Unidade", "Acoes", "Forma Pagamento"]
        if meta.forma_pagamento in ("Excedente", "Fixo+Excedente"): opcoes_alterar.append("Fator Excedente")
        if meta.forma_pagamento in ("Fixo", "Fixo+Excedente"): opcoes_alterar.append("Valor Fixo")
        if meta.forma_pagamento == "ProducaoTotal": opcoes_alterar.append("Valor Produção Total")
        if meta.unidade == "US": opcoes_alterar.append("Colunas US")

        idx_alterar = MenuSimples("Selecione o que deseja alterar", opcoes_alterar).choose(include_exit=True)

        if idx_alterar is None:
            return "Nenhum campo de meta foi alterado."

        match opcoes_alterar[idx_alterar]:
            case "Meta":
                nova_meta = read_float("Entre com o novo valor da meta: ")
                meta.set_meta(nova_meta)
                return "Meta alterada com sucesso."

            case "Unidade":
                opcoes_unidade = Meta.get_coluna_us_options()
                opcao_unidade_selecionada = MenuSimples("Nova unidade de Pagamento", opcoes_unidade).choose(include_exit=False)
                unidade = opcoes_unidade[opcao_unidade_selecionada]
                meta.set_unidade(unidade)
                return "Meta alterada com sucesso."

            case "Acoes":
                return ControllerMeta._alterar_acoes(meta.acoes)

            case "Forma Pagamento":
                opcoes_forma_pagamento = Meta.get_forma_pagamento_options()
                opcao_forma_pagamento_selecionada = MenuSimples("Nova forma de Pagamento", opcoes_forma_pagamento).choose(include_exit=False)
                forma_pagamento = opcoes_forma_pagamento[opcao_forma_pagamento_selecionada]
                meta.set_forma_pagamento(forma_pagamento)

            case "Colunas US":
                return ControllerMeta._alterar_colunas_us(meta.colunas_us)

            case "Fator Excedente":
                fator_excedente = read_float("Novo fator a ser pago por undiade excedente: ", 0)
                meta.set_fator_excedente(fator_excedente)

            case "Valor Fixo":
                valor_fixo = read_float("Novo valor fixo a ser pago", 0)
                meta.set_valor_fixo(valor_fixo)

            case "Valor Produção Total":
                fator_producao_total = read_float("Novo fator a ser pago pela produção total: ", 0)
                meta.set_fator_producao_total(fator_producao_total)

            case _:
                raise ValueError("Erro no index de alteração.")

        return "Meta alterada com sucesso."


    @staticmethod
    def _alterar_acoes(lista_acoes):
        opcoes_alteracao = ["Adicionar acao", "Remover acao"]
        idx = MenuSimples("Selecione o que deseja fazer com a lista de ações", opcoes_alteracao).choose(include_exit=True)

        if idx is None:
            return "Nenhum campo de meta foi alterado."

        match opcoes_alteracao[idx]:
            case "Adicionar acao":
                while True:
                    print(f"Ações atuais: {lista_acoes}")
                    nova_acao = input("Digite a nova ação para adicionar ou deixe vazio para sair: ")

                    if nova_acao == "":
                        break

                    if nova_acao in lista_acoes:
                        raise ValueError("Esta ação já está na lista.")

                    lista_acoes.append(nova_acao)

                return "Meta alterada com sucesso."

            case "Remover acao":
                while True:
                    for i, acao in enumerate(lista_acoes):
                        print(f"{i+1}- {acao}")

                    remover = int(input("Digite o indexador da ação a ser removida ou deixe vazio para sair: "))

                    if remover == "":
                        break

                    if remover < 1 or remover > len(lista_acoes):
                        raise ValueError("Valor fora do intervalo.")

                    lista_acoes.pop(remover-1)

                return "Meta alterada com sucesso."

            case _:
                raise ValueError("Erro no index de alteração.")

    @staticmethod
    def _alterar_colunas_us(colunas_us):
        opcoes_alteracao = ["Adicionar coluna", "Remover coluna"]
        idx = MenuSimples("Selecione o que deseja fazer com a lista de colunas de US", opcoes_alteracao).choose(include_exit=True)

        if idx is None:
            return "Nenhum campo de meta foi alterado."

        match opcoes_alteracao[idx]:
            case "Adicionar coluna":
                while True:
                    print(f"Colunas atuais: {colunas_us}")
                    nova_coluna = input("Digite a nova coluna para adicionar ou deixe vazio para sair: ")

                    if nova_coluna == "":
                        break

                    if nova_coluna in colunas_us:
                        raise ValueError("Esta coluna já está na lista.")

                    colunas_us.append(nova_coluna)

                return "Meta alterada com sucesso."

            case "Remover coluna":
                while True:
                    for i, coluna in enumerate(colunas_us):
                        print(f"{i+1}- {coluna}")

                    remover = int(input("Digite o indexador da coluna a ser removida ou deixe vazio para sair: "))

                    if remover == "":
                        break

                    if remover < 1 or remover > len(colunas_us):
                        raise ValueError("Valor fora do intervalo.")

                    colunas_us.pop(remover-1)

                return "Meta alterada com sucesso."

            case _:
                raise ValueError("Erro no index de alteração.")