import traceback
from datetime import datetime
from Controller import ControllerAtividade, ControllerPessoa, ControllerSupervisor
from Controller.ControllerAcoesConcGmax import ControllerAcoesConcGmax
import sys
from View import MenuSimples


lista_atividades = []
lista_pessoas = []
lista_supervisores = []

controller_atividades = ControllerAtividade(lista_atividades)
print(controller_atividades.carregar())
controller_pessoas = ControllerPessoa(lista_pessoas, controller_atividades.lista_atividades)
print(controller_pessoas.carregar())

controller_pessoas.reconciliar_atividades()

controller_supervisores = ControllerSupervisor(lista_supervisores, controller_pessoas.lista_pessoas)
print(controller_supervisores.carregar())

controller_supervisores.reconciliar_pessoas()

while True:
    try:
        opcoes = ["Menu de Atividades", "Menu de Pessoas", "Menu de Supervisores", "Gerar Relação Gmax", "Gerar Metas", "Salvar e Sair", "Sair sem Salvar"]
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
                            controller_pessoas.reconciliar_atividades()
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
                            msg = controller_pessoas.remover()
                            print(msg)
                            controller_supervisores.reconciliar_pessoas()
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
                while True:
                    opcao_menu = controller_supervisores.menu_principal()
                    match opcao_menu:
                        case 0:
                            print(controller_supervisores.cadastrar())
                            input()
                        case 1:
                            print(controller_supervisores.remover())
                            input()
                        case 2:
                            print(controller_supervisores.alterar())
                            input()
                        case 3:
                            controller_supervisores.listar("Pessoas cadastradas", choose_flag=False)
                            input()
                        case None:
                            print("Retornando ao menu principal.")
                            input()
                            break
                        case _:
                            raise ValueError("Erro no atributo selecionado")

            case 3:
                start_date = datetime.strptime(input("Entre com a data inicial (dd/mm/aaaa): "), "%d/%m/%Y")
                end_date = datetime.strptime(input("Entre com a data final (dd/mm/aaaa): "), "%d/%m/%Y")

                if start_date > end_date:
                    raise ValueError("Data de início deve ser anterior à data final.")

                controller_acoes_conc_gmax = ControllerAcoesConcGmax(controller_pessoas.lista_pessoas, start_date, end_date)
                print(controller_acoes_conc_gmax.gerar_producao_por_supervisor(controller_supervisores.lista_supervisores))

            case 4:
                start_date = datetime.strptime(input("Entre com a data inicial (dd/mm/aaaa): "), "%d/%m/%Y")
                end_date = datetime.strptime(input("Entre com a data final (dd/mm/aaaa): "), "%d/%m/%Y")

                if start_date > end_date:
                    raise ValueError("Data de início deve ser anterior à data final.")

                controller_acoes_conc_gmax = ControllerAcoesConcGmax(controller_pessoas.lista_pessoas, start_date, end_date)
                print(controller_acoes_conc_gmax.gerar_pagamento_metas(controller_supervisores.lista_supervisores))

            case 5:
                retorno_salvar_atividades = controller_atividades.salvar()
                retorno_salvar_pessoas = controller_pessoas.salvar()
                retorno_salvar_supervisores = controller_supervisores.salvar()

                print(retorno_salvar_atividades)
                print(retorno_salvar_pessoas)
                print(retorno_salvar_supervisores)

                if (retorno_salvar_atividades == "Arquivo de atividades salvo com sucesso." and retorno_salvar_pessoas == "Arquivo de pessoas salvo sucesso."
                        and retorno_salvar_supervisores == "Arquivo de supervisores salvo sucesso."):
                    input("\nObrigado por utilizar o programa.\nAutor: Caio Cezar Dias\nContato: caiocd007@gmail.com\n\nPressione ENTER para fechar.")
                    sys.exit()

                print("Não foi possível salvar e sair.")

            case 6:
                input("\nObrigado por utilizar o programa.\nAutor: Caio Cezar Dias\nContato: caiocd007@gmail.com\n\nPressione ENTER para fechar.")
                sys.exit()
            case _:
                input("A opções selecionada foi inválida")

    except Exception as e:
        print(f"Erro na iteração principal. {str(e)}")
        traceback.print_exc()
        input()
