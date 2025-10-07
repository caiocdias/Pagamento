﻿from datetime import datetime
import sys

from Controller import ControllerAtividade, ControllerPessoa
from Controller.ControllerAcoesConcGmax import ControllerAcoesConcGmax
from View import MenuSimples


lista_atividades = []
lista_pessoas = []


controller_atividades = ControllerAtividade(lista_atividades)
print(controller_atividades.carregar())

controller_pessoas = ControllerPessoa(lista_pessoas, controller_atividades.lista_atividades)
print(controller_pessoas.carregar())


while True:
    try:
        opcoes = ["Menu de Atividades", "Menu de Pessoas", "Gerar Relação Gmax", "Salvar e Sair", "Sair sem Salvar"]
        opcao_selecionada = MenuSimples("Menu Principal", opcoes).choose(include_exit=False)

        match opcao_selecionada:
            case 0:
                while True:
                    opcao_menu = controller_atividades.menu_principal()
                    match opcao_menu:
                        case 0:
                            print(controller_atividades.cadastrar())
                            input()
                        case 1:
                            print(controller_atividades.remover())
                            input()
                        case 2:
                            print(controller_atividades.alterar())
                            input()
                        case 3:
                            controller_atividades.listar("Atividades cadastradas", choose_flag=False)
                            input()
                        case None:
                            print("Retornando ao menu principal.")
                            input()
                            break
                        case _:
                            raise ValueError("Erro no atributo selecionado")

            case 1:
                while True:
                    opcao_menu = controller_pessoas.menu_principal()
                    match opcao_menu:
                        case 0:
                            print(controller_pessoas.cadastrar())
                            input()
                        case 1:
                            print(controller_pessoas.remover())
                            input()
                        case 2:
                            print(controller_pessoas.alterar())
                            input()
                        case 3:
                            controller_pessoas.listar("Pessoas cadastradas", choose_flag=False)
                            input()
                        case None:
                            print("Retornando ao menu principal.")
                            input()
                            break
                        case _:
                            raise ValueError("Erro no atributo selecionado")
            case 2:
                start_date = datetime.strptime(input("Entre com a data inicial (dd/mm/aaaa): "), "%d/%m/%Y")
                end_date = datetime.strptime(input("Entre com a data final (dd/mm/aaaa): "), "%d/%m/%Y")
                controller_acoes_conc_gmax = ControllerAcoesConcGmax(controller_pessoas.lista_pessoas, start_date, end_date)
                print(controller_acoes_conc_gmax.gerar_producao())
            case 3:
                retorno_salvar_atividades = controller_atividades.salvar()
                retorno_salvar_pessoas = controller_pessoas.salvar()

                print(retorno_salvar_atividades)
                print(retorno_salvar_pessoas)

                if retorno_salvar_atividades == "Arquivo de atividades salvo com sucesso." and retorno_salvar_pessoas == "Arquivo de pessoas salvo sucesso.":
                    input("\nObrigado por utilizar o programa.\nAutor: Caio Cezar Dias\nContato: caiocd007@gmail.com\n\nPressione ENTER para fechar.")
                    sys.exit()

                print("Não foi possível salvar e sair.")

            case 4:
                input("\nObrigado por utilizar o programa.\nAutor: Caio Cezar Dias\nContato: caiocd007@gmail.com\n\nPressione ENTER para fechar.")
                sys.exit()
            case _:
                input("A opções selecionada foi inválida")

    except Exception as e:
        print(f"Erro na iteração principal. {str(e)}")