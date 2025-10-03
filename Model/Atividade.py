class Atividade:
    def __init__(self, acao: str, origem: str, unidade_pagamento: str, valor_unidade: float):
        self.acao = acao
        self.origem = origem
        self.unidade_pagamento = unidade_pagamento
        self.valor_unidade = valor_unidade

    def __str__(self):
        return f"{self.acao}, {self.origem} - {self.valor_unidade} por {self.unidade_pagamento}"