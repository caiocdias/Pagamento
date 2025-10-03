from Model import Atividade

class Pessoa:
    def __init__(self, nome: str, matricula: str, chave_pix: str, email: str):
        self.nome = nome
        self.matricula = matricula
        self.chave_pix = chave_pix
        self.email = email
        self.atividades = list[Atividade]
