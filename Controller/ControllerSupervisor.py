from Model import Supervisor
from View import MenuSimples


class ControllerSupervisor:
    def __init__(self, lista_supervisores: list, lista_pessoas: list):
        self.lista_supervisores = lista_supervisores
        self.lista_pessoas = lista_pessoas
    def menu_principal(self):
        opcoes = ["Cadastrar Supervisor", "Remover Supervisor", "Alterar Supervisor", "Listar Supervisor"]
        return MenuSimples("Menu de Gerenciamento de Supervisores", opcoes).choose(include_exit=True)

    def cadastrar(self):
        try:
            nome = input("Digite o nome do supervisor: ")
            matricula = input("Digite a mátricula: ")
            email = input("Digite o email: ")
            pasta = input("Digite o caminho da pasta do supervisor: ")

            opcoes_pessoas = [str(pessoa) for pessoa in self.lista_pessoas]
            pessoas = []

            while True:
                opcao_selecionada = MenuSimples("Pessoa para atribuir", opcoes_pessoas).choose(include_exit=True)

                if opcao_selecionada is None:
                    break

                if self.lista_pessoas[opcao_selecionada] not in pessoas:
                    pessoas.append(self.lista_pessoas[opcao_selecionada])
                else:
                    print("Essa pessoa já está na lista para associação.")
                    input()

            supervisor = Supervisor(nome, matricula, email, pasta)
            for pessoa in pessoas:
                supervisor.atribuir_pessoa(pessoa)

            self.lista_supervisores.append(supervisor)
            return "Supervisor cadastrado com sucesso."

        except Exception as e:
            return f"Erro ao cadastrar supervisor. {str(e)}"

    def remover(self):
        try:
            if len(self.lista_supervisores) == 0:
                raise Exception("Não há supervisores cadastrados.")

            supervisor_selecionado = self.listar("Selecione o supervisor para remover", choose_flag=True)

            if supervisor_selecionado is None:
                return "Nenhum supervisor foi removido."

            confirmar = input("Tem certeza que deseja remover o supervisor? (y): ").lower()

            if confirmar != 'y':
                return "Nenhum supervisor foi removido."

            self.lista_supervisores.pop(supervisor_selecionado)

            return "Supervisor removido com sucesso."
        except Exception as e:
            return f"Erro ao remover Supervisor."


    def listar(self, title: str, choose_flag: bool = False):
        if len(self.lista_supervisores) == 0:
            raise Exception("Não há supervisores cadastrados.")

        menu = MenuSimples(title, [str(supervisor) for supervisor in self.lista_supervisores])
        if choose_flag:
            return menu.choose(include_exit=True)

        menu.show(include_exit=False)
        return None