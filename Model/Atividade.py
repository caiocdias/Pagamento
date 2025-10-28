class Atividade:
    def __init__(self, acao: str, unidade_pagamento: str, valor_unidade: float, coluna_referencia: str, acao_reduzir: list, acao_comparar: list):
        self.acao = None
        self.unidade_pagamento = None
        self.valor_unidade = None
        self.coluna_referencia = None
        self.acao_reduzir = None
        self.acao_comparar = None

        self.set_acao(acao)
        self.set_unidade_pagamento(unidade_pagamento)
        self.set_valor_unidade(valor_unidade)
        self.set_coluna_referencia(coluna_referencia)
        self.set_acao_reduzir(acao_reduzir)
        self.set_acao_comparar(acao_comparar)

    def __eq__(self, other):
        if not isinstance(other, Atividade):
            return NotImplemented

        return ((self.acao, self.unidade_pagamento, self.valor_unidade, self.coluna_referencia, self.acao_reduzir, self.acao_comparar)
                == (other.acao, other.unidade_pagamento, other.valor_unidade, other.coluna_referencia, other.acao_reduzir, other.acao_comparar))

    def __str__(self):
        return f"{self.acao} - {self.valor_unidade} por {self.unidade_pagamento} em {self.coluna_referencia}" + f" Reducão: {self.acao_reduzir}" + f" Comparar: {self.acao_comparar}"

    def set_acao(self, acao: str):
        self.acao = acao

    def set_unidade_pagamento(self, unidade_pagamento: str):
        if unidade_pagamento not in ['NS', 'US']:
            raise ValueError("Unidade de pagamento deve ser NS ou US.")

        self.unidade_pagamento = unidade_pagamento

    def set_valor_unidade(self, valor_unidade: float):
        self.valor_unidade = valor_unidade

    def set_coluna_referencia(self, coluna_referencia: str):
        self.coluna_referencia = coluna_referencia

    def set_acao_reduzir(self, acao_reduzir: list):
        self.acao_reduzir = acao_reduzir

    def set_acao_comparar(self, acao_comparar: list):
        self.acao_comparar = acao_comparar