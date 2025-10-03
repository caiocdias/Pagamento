class Atividade:
    def __init__(self, acao: str, origem: str, unidade_pagamento: str, valor_unidade: float):
        self.acao = None
        self.origem = None
        self.unidade_pagamento = None
        self.valor_unidade = None

        self.set_acao(acao)
        self.set_origem(origem)
        self.set_unidade_pagamento(unidade_pagamento)
        self.set_valor_unidade(valor_unidade)

    def __str__(self):
        return f"{self.acao}, {self.origem} - {self.valor_unidade} por {self.unidade_pagamento}"

    def set_acao(self, acao: str):
        self.acao = acao
    
    def set_origem(self, origem: str):
        if origem not in ["AcoesConcGmax", "AcoesConcSap"]:
            raise ValueError("Origem deve ser AcoesConcGmax ou AcoesConcSap.")

        self.origem = origem

    def set_unidade_pagamento(self, unidade_pagamento: str):
        if unidade_pagamento not in ['NS', 'US']:
            raise ValueError("Origem deve ser NS ou US.")

        self.unidade_pagamento = unidade_pagamento

    def set_valor_unidade(self, valor_unidade: float):
        self.valor_unidade = valor_unidade