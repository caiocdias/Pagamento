import os.path
from Model import Pessoa


class PastaInvalidaError(ValueError):
    """"O caminho fornecido é inválido"""

class Supervisor:
    def __init__(self):
        self.nome = None
        self.matricula = None
        self.email = None
        self.pasta = None
        self.lista_pessoas = []

    def set_nome(self, nome: str):
        self.nome = nome

    def set_matricula(self, matricula: str):
        self.matricula = matricula

    def set_email(self, email: str):
        self.email = email

    def set_pasta(self, pasta: str):
        if not os.path.isdir(pasta):
            raise PastaInvalidaError(f"Caminho {pasta} é inválido.")
        self.pasta = pasta

    def atribuir_pessoa(self, pessoa: Pessoa) -> bool:
        if pessoa is not None:
            self.lista_pessoas.append(pessoa)
            return True
        return False

    def remover_pessoa(self, index: int) -> bool:
        self.lista_pessoas.pop(index)
        return True