import os.path
import pickle
from Model import Atividade
from View import MenuSimples
from Generic import Utils

class ControllerAtividade:
    def __init__(self, lista_atividades: list):
        self.lista_atividades = lista_atividades

    def menu_principal(self):
        opcoes = ["Cadastrar Atividade", "Remover Atividade", "Alterar Atividade", "Listar Atividades"]
        return MenuSimples("Menu de Gerenciamento de Atividades", opcoes).choose(include_exit=True)

    def cadastrar(self):
        try:
            acao = input("\nDigite a ação da atividade: ")
            origens = ["AcoesConcGmax", "AcoesConcSap"]
            origem_selecionada = MenuSimples("Selecione a origem: ", origens).choose(include_exit=False)

            unidades_pagamento = ['NS', 'US']
            unidade_selecionada = MenuSimples("Seleciona a unidade de pagamento", unidades_pagamento).choose(include_exit=False)

            valor_unidade = Utils.read_float("\nSelecione o valor pago por unidade: ")

            coluna_referencia = input("Digite coluna de referência: ")

            acao_reduzir = input("Digite a ação para reduzir ou deixe em vazio: ")
            acao_comparar = input("Digite a ação para comparar ou deixe em vazio: ")
            atividade_criada = Atividade(acao, origens[origem_selecionada], unidades_pagamento[unidade_selecionada], valor_unidade, coluna_referencia, acao_reduzir, acao_comparar)

            self.lista_atividades.append(atividade_criada)

            return "Atvidade cadastrada com sucesso."
        except Exception as e:
            return f"\nErro ao criar atividade. {str(e)}"

    def remover(self):
        try:
            if len(self.lista_atividades) == 0:
                raise Exception("Não há ativiades cadastradas.")

            atividade_selecionada = self.listar("Selecionae a atividade para remover", choose_flag=True)

            if atividade_selecionada is None:
                return "Nenhuma atividade foi removida."

            confirmar = input("Tem certeza que deseja remover a atividade? (y): ").lower()
            if confirmar != 'y':
                return "Nenhuma atividade foi removida."

            self.lista_atividades.pop(atividade_selecionada)

            return "Atividade removida com sucesso"
        except Exception as e:
            return f"\nErro ao remover atividade. {str(e)}"

    def alterar(self):
        try:
            if len(self.lista_atividades) == 0:
                raise Exception("Não há atividades cadastradas.")

            atividade_selecionada = self.listar("Selecione a atividade para alterar", choose_flag=True)

            if atividade_selecionada is None:
                return "Nenhuma atividade foi alterada."

            confirmar = input("Tem certeza que deseja alterar a atividade? (y): ").lower()
            if confirmar != 'y':
                return "Nenhuma atividade foi alterada."

            opcoes = ["Alterar acao", "Alterar origem", "Alterar unidade de pagamento", "Alterar valor da unidade", "Alterar coluna de referência", "Alterar ação para reduzir", "Alterar ação para comparar"]
            opcao_selecionada = MenuSimples("Selecione o atributo para alterar", opcoes).choose()

            match opcao_selecionada:
                case 0:
                    acao = input("Nova acao: ")
                    self.lista_atividades[atividade_selecionada].set_acao(acao)
                case 1:
                    origens = ["AcoesConcGmax", "AcoesConcSap"]
                    origem_selecionada = MenuSimples("Selecione a origem: ", origens).choose(include_exit=False)
                    self.lista_atividades[atividade_selecionada].set_origem(origens[origem_selecionada])
                case 2:
                    unidades_pagamento = ["NS", "US"]
                    unidade_selecionada = MenuSimples("Seleciona a unidade de pagamento", unidades_pagamento).choose(include_exit=False)
                    self.lista_atividades[atividade_selecionada].set_unidade_pagamento(unidades_pagamento[unidade_selecionada])
                case 3:
                    valor = float(input("Novo valor de unidade: "))
                    self.lista_atividades[atividade_selecionada].set_valor_unidade(valor)
                case 4:
                    referencia = input("Digite a nova coluna de referência: ")
                    self.lista_atividades[atividade_selecionada].set_coluna_referencia(referencia)
                case 5:
                    acao_reduzir = input("Digite a nova ação para reduzir: ")
                    self.lista_atividades[atividade_selecionada].set_acao_reduzir(acao_reduzir)
                case 6:
                    acao_comparar = input("Digite a nova ação para comparar: ")
                    self.lista_atividades[atividade_selecionada].set_acao_comparar(acao_comparar)
                case _:
                    raise ValueError("Erro no atributo selecionado")

            return "Ativdade alterada com sucesso"
        except Exception as e:
            return f"\nErro ao alterar atividade. {str(e)}"

    def listar(self, title: str, choose_flag: bool = False):
        if len(self.lista_atividades) == 0:
            raise Exception("Não há atividades cadastradas.")

        menu = MenuSimples(title, [str(atv) for atv in self.lista_atividades])
        if choose_flag:
            return menu.choose(include_exit=True)

        menu.show(include_exit=False)
        return None

    def salvar(self):
        try:
            path = ".\\compressed_data\\lista_atividades.pkl"
            with open(path, 'wb') as file:
                pickle.dump(self.lista_atividades, file)
            return "Arquivo de atividades salvo com sucesso."
        except Exception as e:
            return f"Erro ao savar o arquivo de atividades. {str(e)}"

    def carregar(self):
        try:
            if os.path.isfile(".\\compressed_data\\lista_atividades.pkl"):
                path = ".\\compressed_data\\lista_atividades.pkl"
                with open(path, 'rb') as file:
                    self.lista_atividades = pickle.load(file)
                return "Arquivo de atividades carregado com sucesso."
            raise FileNotFoundError("O arquivo não existe.")
        except Exception as e:
            return f"Erro ao carregar o arquivo de atividades. {str(e)}"