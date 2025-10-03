import pickle
from Model import Atividade
from View import MenuSimples
from Generic import Utils

class ControllerAtividade:
    def __init__(self, lista_atividades: list):
        self.lista_atividades = lista_atividades

    def cadastrar_atividade(self):
        try:
            acao = input("\nDigite a ação da atividade: ")
            origens = ["AcoesConcGmax", "AcoesConcSap"]
            origem_selecionada = MenuSimples("Selecione a origem: ", origens).choose(include_exit=False)

            unidades_pagamento = ['NS', 'US']
            unidade_selecionada = MenuSimples("Seleciona a unidade de pagamento", unidades_pagamento).choose(include_exit=False)

            valor_unidade = Utils.read_float("\nSelecione o valor pago por unidade: ")

            atividade_criada = Atividade(acao, origens[origem_selecionada], unidades_pagamento[unidade_selecionada], valor_unidade)

            self.lista_atividades.append(atividade_criada)

            return "Atvidade criada com sucesso."
        except Exception as e:
            return f"\nErro ao criar atividade. {str(e)}"

    def remover_atividade(self):
        try:
            if len(self.lista_atividades) == 0:
                raise Exception("Não há ativiades cadastradas.")

            atividade_selecionada = self.listar_atividades("Selecionae a atividade para remover", choose_flag=True)

            if atividade_selecionada is None:
                return "Nenhuma atividade foi removida."

            confirmar = input("Tem certeza que deseja remover a atividade? (y): ").lower()
            if confirmar != 'y':
                return "Nenhuma atividade foi removida."

            self.lista_atividades.pop(atividade_selecionada)

            return "Atividade removida com sucesso"
        except Exception as e:
            return f"\nErro ao remover atividade. {str(e)}"

    def alterar_atividade(self):
        try:
            if len(self.lista_atividades) == 0:
                raise Exception("Não há atividades cadastradas.")

            atividade_selecionada = self.listar_atividades("Selecione a atividade para alterar", choose_flag=True)

            if atividade_selecionada is None:
                return "Nenhuma atividade foi alterada."

            confirmar = input("Tem certeza que deseja alterar a atividade? (y): ").lower()
            if confirmar != 'y':
                return "Nenhuma atividade foi alterada."

            opcoes = ["Alterar acao", "Alterar origem", "Alterar unidade de pagamento", "Alterar valor da unidade"]
            opcao_selecionada = MenuSimples("Selecione o atributo para alterar", opcoes).choose()

            match opcao_selecionada:
                case 0:
                    acao = input("Nova acao: ")
                    self.lista_atividades[atividade_selecionada].set_acao(acao)
                    pass
                case 1:
                    origens = ["AcoesConcGmax", "AcoesConcSap"]
                    origem_selecionada = MenuSimples("Selecione a origem: ", origens).choose(include_exit=False)
                    self.lista_atividades[atividade_selecionada].set_origem(origens[origem_selecionada])
                    pass
                case 2:
                    unidades_pagamento = ["NS", "US"]
                    unidade_selecionada = MenuSimples("Seleciona a unidade de pagamento", unidades_pagamento).choose(include_exit=False)
                    self.lista_atividades[atividade_selecionada].set_unidade_pagamento(unidades_pagamento[unidade_selecionada])
                    pass
                case 3:
                    valor = float(input("Novo valor de unidade: "))
                    self.lista_atividades[atividade_selecionada].set_valor_unidade(valor)
                    pass
                case _:
                    raise ValueError("Erro no atributo selecionado")

            return "Ativdade alterada com sucesso"
        except Exception as e:
            return f"\nErro ao alterar atividade. {str(e)}"

    def listar_atividades(self, title: str, choose_flag: bool = False):
        menu = MenuSimples(title, [str(atv) for atv in self.lista_atividades])
        if choose_flag:
            return menu.choose(include_exit=True)

        menu.show(include_exit=False)
        return None

    def salvar_lista(self):
        path = "..\\compressed_data\\listaAtividades.pkl"
        with open(path, 'wb') as file:
            pickle.dump(self.lista_atividades, file)

    def carregar_lista(self):
        path = "..\\compressed_data\\listaAtividades.pkl"
        with open(path, 'rb') as file:
            self.lista_atividades = pickle.load(file)

if __name__ == "__main__":

    atividades = []
    controladora = ControllerAtividade(atividades)

    print(controladora.cadastrar_atividade())
    input()
    print(controladora.cadastrar_atividade())
    input()
    controladora.listar_atividades("Atividades Cadastradas", choose_flag=False)
    while True:
        print(controladora.alterar_atividade())
        input()
        controladora.listar_atividades("Atividades Cadastradas", choose_flag=False)