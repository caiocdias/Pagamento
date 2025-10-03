from Model import Atividade

class Pessoa:
    def __init__(self, nome: str, matricula: str, chave_pix: str, email: str):
        self.nome = None
        self.matricula = None
        self.chave_pix = None
        self.email = None
        self.atividades = []

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