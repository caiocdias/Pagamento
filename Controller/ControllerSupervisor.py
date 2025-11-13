from Model import Supervisor
from View import MenuSimples
import pickle
import os

class ControllerSupervisor:
    def __init__(self, lista_supervisores: list, lista_pessoas: list):
        self.lista_supervisores = lista_supervisores
        self.lista_pessoas = lista_pessoas
    def menu_principal(self):
        opcoes = ["Cadastrar Supervisor", "Remover Supervisor", "Alterar Supervisor", "Listar Supervisor"]
        return MenuSimples("Menu de Gerenciamento de Supervisores", opcoes).choose(include_exit=True)

    def cadastrar(self):
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

    def remover(self):
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

    def alterar(self):
        if len(self.lista_supervisores) == 0:
            raise Exception("Não há supervisores cadastradas.")

        supervisor_selecionado = self.listar("Selecione o supervisor para alterar", choose_flag=True)

        if supervisor_selecionado is None:
            return "Nenhuma supervisor foi alterado."

        confirmar = input("Tem certeza que deseja alterar a supervisor? (y): ").lower()
        if confirmar != 'y':
            return "Nenhuma supervisor foi alterado."

        opcoes = ["Alterar nome", "Alterar matricula", "Alterar email", "Alterar pasta","Alterar pessoas."]
        opcao_selecionada = MenuSimples("Selecione o atributo para alterar", opcoes).choose(include_exit=True)

        match opcao_selecionada:
            case 0:
                nome = input("Digite o novo nome: ")
                self.lista_supervisores[supervisor_selecionado].set_nome(nome)
            case 1:
                matricula = input("Digite a nova mátricula: ")
                self.lista_supervisores[supervisor_selecionado].set_matricula(matricula)
            case 2:
                email = input("Digite o novo email: ")
                self.lista_supervisores[supervisor_selecionado].set_email(email)
            case 3:
                pasta = input("Digite a nova pasta: ")
                self.lista_supervisores[supervisor_selecionado].set_pasta(pasta)
            case 4:
                self._alterar_pessoas(supervisor_selecionado)
            case _:
                raise ValueError("Erro no atributo selecionado")
        return "Supervisor alterada com sucesso."

    def _alterar_pessoas(self, supervisor_selecionado):
        while True:
            opcoes = ["Adicionar Pessoas", "Remover Pessoas"]
            opcao_selecionada = MenuSimples("Selecione o que fazer com a lista de pessoas", opcoes).choose(include_exit=True)

            if opcao_selecionada is None :
                return True

            opcoes_pessoas = [str(pessoa) for pessoa in self.lista_pessoas]

            match opcao_selecionada:
                case 0:
                    while True:
                        pessoa_selecionada = MenuSimples("Selecione a pessoa", opcoes_pessoas).choose(include_exit=True)

                        if pessoa_selecionada is None:
                            break

                        if self.lista_pessoas[pessoa_selecionada] in self.lista_supervisores[supervisor_selecionado].lista_pessoas:
                            print("Este supervisor já está associado a essa pessoa.")
                            input()
                        else:
                            self.lista_supervisores[supervisor_selecionado].atribuir_pessoa(self.lista_pessoas[pessoa_selecionada])
                            print("Pessoa atribuída com sucesso.")
                            input()
                case 1:
                    if len(self.lista_supervisores[supervisor_selecionado].lista_pessoas) == 0:
                        raise ValueError("Não há mais pessoas associadas a este supervisor.")
                    while True:
                        pessoa_para_remover = MenuSimples("Selecione a pessoa para remover", [str(pessoa) for pessoa in self.lista_supervisores[supervisor_selecionado].lista_pessoas]).choose(include_exit=False)

                        if pessoa_para_remover is None:
                            break

                        self.lista_supervisores[supervisor_selecionado].remover_pessoa(pessoa_para_remover)
                        print("Pessoa removida com sucesso.")
                case _:
                    raise ValueError("Erro no atributo selecionado")

    def salvar(self):
        try:
            path = ".\\compressed_data\\lista_supervisores.pkl"
            with open(path, 'wb') as file:
                pickle.dump(self.lista_supervisores, file)
            return "Arquivo de supervisores salvo sucesso."
        except Exception as e:
            return f"Erro ao salvar arquivo. {str(e)}"

    def carregar(self):
        try:
            if os.path.isfile(".\\compressed_data\\lista_supervisores.pkl"):
                path = ".\\compressed_data\\lista_supervisores.pkl"
                with open(path, 'rb') as file:
                    self.lista_supervisores = pickle.load(file)
                return "Arquivo de supervisores carregado com sucesso"
            raise FileNotFoundError("O arquivo não existe.")
        except Exception as e:
            return f"Erro ao carregar arquivo. {str(e)}"

    def listar(self, title: str, choose_flag: bool = False):
        if len(self.lista_supervisores) == 0:
            raise Exception("Não há supervisores cadastrados.")

        menu = MenuSimples(title, [str(supervisor) for supervisor in self.lista_supervisores])
        if choose_flag:
            return menu.choose(include_exit=True)

        menu.show(include_exit=False)
        return None

    def reconciliar_pessoas(self):
        def _key(p):
            return (p.nome, p.matricula, p.chave_pix, p.email)

        mapa = {_key(p): p for p in self.lista_pessoas}  # master

        for sup in self.lista_supervisores:
            novas = []
            for p in sup.lista_pessoas:
                ref = mapa.get(_key(p))
                if ref is not None:  # mantém só quem existe no master
                    novas.append(ref)
            sup.lista_pessoas = novas