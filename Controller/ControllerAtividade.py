from Model import Atividade
from View import MenuSimples
from Generic import Utils


class ControllerAtividade:
    def __init__(self, list_atividades: list):
        self.list_atividades = list_atividades

    def cadastrar_atividade(self):
        try:
            acao = input("\nDigite a ação da atividade: ")
            origens = ["AcoesConcGmax", "AcoesConcSap"]
            origem_selecionada = MenuSimples("Selecione a origem: ", origens).choose(include_exit=False)

            unidades_pagamento = ["NS", "US"]
            unidade_selecionada = MenuSimples("Seleciona a unidade de pagamento", unidades_pagamento).choose(include_exit=False)

            valor_unidade = Utils.read_float("\nSelecione o valor pago por unidade: ")

            atividade_criada = Atividade(acao, origens[origem_selecionada], unidades_pagamento[unidade_selecionada], valor_unidade)

            self.list_atividades.append(atividade_criada)

            return "Atvidade criada com sucesso."
        except Exception as e:
            return f"\nErro ao criar atividade. {str(e)}"

if __name__ == "__main__":
    lista = []
    controller = ControllerAtividade(lista)
    controller.cadastrar_atividade()
    print(str(lista[0]))