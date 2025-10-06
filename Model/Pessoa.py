from Model import Atividade

class Pessoa:
    def __init__(self, nome: str, matricula: str, chave_pix: str, email: str):
        self.nome = None
        self.matricula = None
        self.chave_pix = None
        self.email = None
        self.lista_atividades = []

        self.set_nome(nome)
        self.set_matricula(matricula)
        self.set_chave_pix(chave_pix)
        self.set_email(email)

    def set_nome(self, nome: str):
        self.nome = nome

    def set_matricula(self, matricula: str):
        self.matricula = matricula

    def set_chave_pix(self, chave_pix):
        self.chave_pix = chave_pix

    def set_email(self, email):
        self.email = email

    def atribuir_atividade(self, atividade: Atividade) -> bool:
        if atividade is not None:
            self.lista_atividades.append(atividade)
            return True
        return False

    def remover_atividade(self, index) -> bool:
        self.lista_atividades.pop(index)
        return True

    def __str__(self):
        atividades_fmt = " | ".join(
            f"{a.acao} : {a.valor_unidade} p/ {a.unidade_pagamento}"
            for a in self.lista_atividades
            if isinstance(a, Atividade)
        )
        return (
            f"{self.nome}, {self.matricula}, {self.chave_pix}, {self.email} Atividades: [{atividades_fmt}]"
        )