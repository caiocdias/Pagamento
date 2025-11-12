from typing_extensions import override


class Meta:
    def __init__(self, meta: float ,unidade: str, forma_pagamento: str, fator_excedente: float, valor_fixo: float, fator_producao_total: float, acoes: list, colunas_us: list):
        self.meta = None
        self.unidade = None
        self.forma_pagamento = None
        self.fator_excedente = None
        self.valor_fixo = None
        self.fator_producao_total = None
        self.acoes = []
        self.colunas_us = []

        self.set_meta(meta)
        self.set_acoes(acoes)
        self.set_unidade(unidade)

        if self.unidade == "US":
            self.set_colunas_us(colunas_us)

        self.set_forma_pagamento(forma_pagamento)

        if self.forma_pagamento in ("Excedente", "Fixo+Excedente"):
            self.set_fator_excedente(fator_excedente)

        if self.forma_pagamento in ("Fixo", "Fixo+Excedente"):
            self.set_valor_fixo(valor_fixo)

        if self.forma_pagamento == "ProducaoTotal":
            self.set_fator_producao_total(fator_producao_total)

    def set_meta(self, meta: float):
        self.meta = meta

    def set_unidade(self, unidade: str):
        if unidade not in self.get_coluna_us_options():
            raise ValueError(f"Unidade de pagamento deve estar contida em {self.get_coluna_us_options()}.")
        self.unidade = unidade

    def set_forma_pagamento(self, forma_pagamento):
        if forma_pagamento not in self.get_forma_pagamento_options():
            raise ValueError(f"Forma de pagamento deve estar contida em {self.get_forma_pagamento_options()}.")
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

    @staticmethod
    def get_coluna_us_options():
        return ["NS", "US"]

    @staticmethod
    def get_forma_pagamento_options():
        return ["Fixo", "Excedente", "Fixo+Excedente", "ProducaoTotal"]

    def __str__(self):
        str1 = f"Meta: {self.meta} {self.unidade}. Forma de Pagamento: {self.forma_pagamento}"
        str2 = f", Fator excedente: {self.fator_excedente}" if self.forma_pagamento in ("Excedente", "Fixo+Excedente") else ""
        str3 = f", Valor fixo: {self.valor_fixo}" if self.forma_pagamento in ("Fixo", "Fixo+Excedente") else ""
        str4 = f", Acoes: {str(self.acoes)}"
        str5 = f", Colunas de US: {str(self.colunas_us)}" if self.unidade == "US" else ""

        return str1+str2+str3+str4+str5