from View import MenuSimples
from Model import Meta
from Generic import Utils, read_float


class ControllerMeta:
    def __init__(self):
        pass

    @staticmethod
    def cadastrar():
        try:
            acoes = []
            while True:
                acao = input("Digite uma ação para adicionar a meta, deixe vazio para sair: ")
                if acao == "":
                    break
                acoes.append(acao)

            meta = read_float("Entre com o valor da meta: ", min_=0)
            opcoes_unidade = ["NS", "US"]
            opcao_unidade_selecionada = MenuSimples("Unidade de Pagamento", opcoes_unidade).choose(include_exit=False)
            unidade = opcoes_unidade[opcao_unidade_selecionada]

            colunas = []
            if unidade == "US":
                while True:
                    coluna = input("Digite a coluna para , deixe vazio para sair: ")
                    if coluna == "":
                        break
                    colunas.append(coluna)

            opcoes_forma_pagamento = ["Fixo", "Excedente", "Fixo+Excedente", "ProducaoTotal"]
            opcao_forma_pagamento_selecionada = MenuSimples("Forma de Pagamento", opcoes_forma_pagamento).choose(include_exit=False)
            forma_pagamento = opcoes_forma_pagamento[opcao_forma_pagamento_selecionada]

            fator_excedente = None
            if forma_pagamento in ("Excedente", "Fixo+Excedente"):
                fator_excedente = Utils.read_float("Fator a ser pago por undiade excedente: ",0)

            valor_fixo = None
            if forma_pagamento in ("Fixo", "Fixo+Excedente"):
                valor_fixo = Utils.read_float("Valor fixo a ser pago", 0)

            fator_producao_total = None
            if forma_pagamento == "ProducaoTotal":
                fator_producao_total = Utils.read_float("Fator a ser pago pela produção total: ",0)

            meta = Meta(meta, unidade, forma_pagamento, fator_excedente, valor_fixo, fator_producao_total, acoes, colunas)
            return meta
        except Exception as e:
            return f"Erro ao cadastrar Meta. {str(e)}"

    @staticmethod
    def alterar(meta: Meta):
        try:
            if not isinstance(meta, Meta):
                raise TypeError(f"Objeto meta é do tipo [{type(meta).__name__}] e não uma instância de Meta.")

            opcoes_alterar = ["Meta", "Unidade", "Acoes", "Forma Pagamento"]
            if meta.forma_pagamento in ("Excedente", "Fixo+Excedente"): opcoes_alterar.append("Fator Excedente")
            if meta.forma_pagamento in ("Fixo", "Fixo+Excedente"): opcoes_alterar.append("Valor Fixo")
            if meta.forma_pagamento == "ProducaoTotal": opcoes_alterar.append("Valor Produção Total")

            # TODO: Implementar a lógica de alteração
        except Exception as e:
            return f"Erro ao alterar Meta. {str(e)}"
