import os.path
import pickle
from Model import Pessoa
from View import MenuSimples
from Controller.ControllerMeta import ControllerMeta


class ControllerPessoa:
    def __init__(self, lista_pessoas: list, lista_atividades: list):
        self.lista_pessoas = lista_pessoas
        self.lista_atividades = lista_atividades

    def menu_principal(self):
        opcoes = ["Cadastrar Pessoa", "Remover Pessoa", "Alterar Pessoa", "Listar Pessoas"]
        return MenuSimples("Menu de Gerenciamento de Pessoas", opcoes).choose(include_exit=True)

    def cadastrar(self):
        # ========== Cadastro da Pessoa ==========
        nome = input("Digite o nome da pessoa: ")
        matricula = input("Digite a mátricula: ")
        chave_pix = input("Digite a chave pix: ")
        email = input("Digite o email: ")
        pessoa = Pessoa(nome, matricula, chave_pix, email)

        # ========== Atribuição de Atividade ==========
        idx = MenuSimples("Deseja cadastrar atividades (FH e Freelancer) para a pessoa?", options=["Sim", "Não"]).choose(include_exit=False)
        if idx == 0:
            opcoes_atividade = [str(atv) for atv in self.lista_atividades]
            atividades = []
            while True:
                opcao_selecionada = MenuSimples("Atividade para Atribuir", opcoes_atividade).choose(include_exit=True)

                if opcao_selecionada is None:
                    break

                if self.lista_atividades[opcao_selecionada] not in atividades:
                    atividades.append(self.lista_atividades[opcao_selecionada])
                else:
                    print("Essa atividade já está na lista para cadastro.")
                    input()

            for atv in atividades:
                pessoa.atribuir_atividade(atv)

        # ========== Atribuição de Meta ==========
        idx = MenuSimples("Deseja cadastrar uma meta para a pessoa?", options=["Sim", "Não"]).choose(include_exit=False)
        if idx == 0:
            meta = ControllerMeta.cadastrar()
            if meta is not None:
                pessoa.set_meta(meta)

        self.lista_pessoas.append(pessoa)
        return "Pessoa cadastrada com sucesso."
    
    def remover(self):
        if len(self.lista_pessoas) == 0:
            raise Exception("Não há pessoas cadastradas.")

        pessoa_selecionada = self.listar("Selecionae a pessoa para remover", choose_flag=True)

        if pessoa_selecionada is None:
            return "Nenhuma pessoa foi removida."

        confirmar = input("Tem certeza que deseja remover a pessoa? (y): ").lower()
        if confirmar != 'y':
            return "Nenhuma pessoa foi removida."

        self.lista_pessoas.pop(pessoa_selecionada)

        return "Pessoa removida com sucesso."

    def alterar(self):
        if len(self.lista_pessoas) == 0:
            raise Exception("Não há pessoas cadastradas.")

        pessoa_selecionada = self.listar("Selecione a pessoa para alterar", choose_flag=True)

        if pessoa_selecionada is None:
            return "Nenhuma pessoa foi alterada."

        confirmar = input("Tem certeza que deseja alterar a pessoa? (y): ").lower()
        if confirmar != 'y':
            return "Nenhuma pessoa foi alterada."

        opcoes = ["Alterar nome", "Alterar matricula", "Alterar chave pix", "Alterar email", "Alterar atividades", "Alterar meta", "Remover meta"]
        opcao_selecionada = MenuSimples("Selecione o atributo para alterar", opcoes).choose(include_exit=True)

        match opcao_selecionada:
            case 0:
                nome = input("Digite o novo nome: ")
                self.lista_pessoas[pessoa_selecionada].set_nome(nome)
            case 1:
                matricula = input("Digite a nova mátricula: ")
                self.lista_pessoas[pessoa_selecionada].set_matricula(matricula)
            case 2:
                chave_pix = input("Digite a nova chave pix: ")
                self.lista_pessoas[pessoa_selecionada].set_chave_pix(chave_pix)
            case 3:
                email = input("Digite o novo email: ")
                self.lista_pessoas[pessoa_selecionada].set_email(email)
            case 4:
                self._alterar_atividade(pessoa_selecionada)
            case 5:
                print(ControllerMeta.alterar(self.lista_pessoas[pessoa_selecionada].meta))
            case 6:
                self.lista_pessoas[pessoa_selecionada].meta = None
            case _:
                raise ValueError("Erro no atributo selecionado")
        return "Pessoa alterada com sucesso."

    def listar(self, title: str, choose_flag: bool = False):
        if len(self.lista_pessoas) == 0:
            raise Exception("Não há pessoas cadastradas.")

        menu = MenuSimples(title, [str(pessoa) for pessoa in self.lista_pessoas])
        if choose_flag:
            return menu.choose(include_exit=True)

        menu.show(include_exit=False)
        return None

    def salvar(self):
        try:
            path = ".\\compressed_data\\lista_pessoas.pkl"
            with open(path, 'wb') as file:
                pickle.dump(self.lista_pessoas, file)
            return "Arquivo de pessoas salvo sucesso."
        except Exception as e:
            return f"Erro ao salvar arquivo. {str(e)}"

    def carregar(self):
        try:
            if os.path.isfile(".\\compressed_data\\lista_pessoas.pkl"):
                path = ".\\compressed_data\\lista_pessoas.pkl"
                with open(path, 'rb') as file:
                    self.lista_pessoas = pickle.load(file)
                return "Arquivo de pessoas carregado com sucesso"
            raise FileNotFoundError("O arquivo não existe.")
        except Exception as e:
            return f"Erro ao carregar arquivo. {str(e)}"


    def _alterar_atividade(self, pessoa_selecionada):
        while True:
            opcoes = ["Adicionar Atividade", "Remover Atividade"]
            opcao_selecionada = MenuSimples("Selecione o que fazer com atividades", opcoes).choose(include_exit=True)

            if opcao_selecionada is None :
                return True

            opcoes_atividade = [str(atv) for atv in self.lista_atividades]

            match opcao_selecionada:
                case 0:
                    while True:
                        atividade_selecionada = MenuSimples("Selecione a atividade", opcoes_atividade).choose(include_exit=True)

                        if atividade_selecionada is None:
                            break

                        if self.lista_atividades[atividade_selecionada] in self.lista_pessoas[pessoa_selecionada].lista_atividades:
                            print("Este usuário já possui essa atividade.")
                            input()
                        else:
                            self.lista_pessoas[pessoa_selecionada].atribuir_atividade(self.lista_atividades[atividade_selecionada])
                            print("Atividade atribuída com sucesso.")
                            input()
                case 1:
                    if len(self.lista_pessoas[pessoa_selecionada].lista_atividades) == 0:
                        raise ValueError("Não há mais atividades cadastradas nesta pessoa.")
                        break
                    while True:
                        atividade_para_remover = MenuSimples("Selecione a atividade para remover", [str(atv) for atv in self.lista_pessoas[pessoa_selecionada].lista_atividades]).choose(include_exit=False)

                        if atividade_para_remover is None:
                            break

                        self.lista_pessoas[pessoa_selecionada].remover_atividade(atividade_para_remover)
                        print("Atividade removida com sucesso.")
                case _:
                    raise ValueError("Erro no atributo selecionado")

    def reconciliar_atividades(self):
        def _key(atv):
            return (
                atv.acao,
                atv.unidade_pagamento,
                atv.valor_unidade,
                atv.coluna_referencia,
                tuple(atv.acao_reduzir or []),
                tuple(atv.acao_comparar or []),
            )

        mapa = {_key(a): a for a in self.lista_atividades}  # MASTER: atividades válidas

        for pessoa in self.lista_pessoas:
            novas = []
            for atv in pessoa.lista_atividades:
                ref = mapa.get(_key(atv))
                if ref is not None:  # mantém só quem existe no master
                    novas.append(ref)
            pessoa.lista_atividades = novas
