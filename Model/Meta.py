class Meta:
    def __init__(self, unidade: str, forma_pagamento: str, fator_excedente: float, valor_fixo: float, fator_producao_total: float, acoes: list, colunas_us: list):
        self.unidade = None
        self.forma_pagamento = None
        self.fator_excedente = None
        self.valor_fixo = None
        self.fator_producao_total = None
        self.acoes = []
        self.colunas_us = []

        self.set_acoes(acoes)
        self.set_unidade(unidade)
        self.set_colunas_us(colunas_us)
        self.set_forma_pagamento(forma_pagamento)

        if self.forma_pagamento in ("Excedente", "Fixo+Excedente"):
            self.set_fator_excedente(fator_excedente)

        if self.valor_fixo in ("Fixa", "Fixo+Excedente"):
            self.set_valor_fixo(valor_fixo)

        self.set_fator_producao_total(fator_producao_total)


    def set_unidade(self, unidade):
        if unidade not in ["NS", "US"]:
            raise ValueError("Unidade de pagamento deve ser NS ou US.")
        self.unidade = unidade

    def set_forma_pagamento(self, forma_pagamento):
        if forma_pagamento not in ["Fixo", "Excedente", "Fixo+Excedente", "ProducaoTotal"]:
            raise ValueError("Forma de pagamento deve ser Fixo, Excedente, Fixo + Excedente ou sobre a Produção Total.")
        self.forma_pagamento = forma_pagamento

    def set_fator_excedente(self, fator_excedente: float):
        self.fator_excedente = fator_excedente

    def set_valor_fixo(self, valor_fixo: float):
        self.valor_fixo = valor_fixo

    def set_fator_producao_total(self, fator_producao_total: float):
        self.fator_producao_total = fator_producao_total

    def set_acoes(self, acoes: list):
        if len(acoes) < self.get_min_acoes():
            raise ValueError(f"A lista de acoes deve conter pelo menos {self.get_min_acoes()} elemento(s).")

        for i in acoes:
            if not isinstance(i, str):
                raise ValueError(f"Ação {i} deve der uma string.")

        self.acoes = acoes

    def set_colunas_us(self, colunas_us: list):
        if len(colunas_us) < self.get_min_colunas_us():
            raise ValueError(f"A lista de colunas deve conter pelo menos {self.get_min_colunas_us()} elemento(s).")

        for i in colunas_us:
            if not isinstance(i, str):
                raise ValueError(f"Coluna de us {i} deve der uma string.")

        self.colunas_us = colunas_us

    @staticmethod
    def get_min_colunas_us():
        min_colunas_us = 1
        return min_colunas_us

    @staticmethod
    def get_min_acoes():
        min_acoes = 1
        return min_acoes