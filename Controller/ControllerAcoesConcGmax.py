import datetime
from Generic import Utils
from Model import AcoesConcGmax
import pandas as pd

class ControllerAcoesConcGmax:
    def __init__(self, lista_pessoas : list, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self.lista_pessoas = lista_pessoas
        self.AcoesConcGmax = AcoesConcGmax(self.start_date, self.end_date)

    def gerar_producao(self):
        try:
            cols_soma = ["ACOES_QTD_US_INTERNA", "ACOES_QTD_US_TOP", "ACOES_QTD_US_PRJ", "ACOES_QTD_US_GEO"]

            def somase_por_ns(df):
                return (df.assign(_total=df[cols_soma].sum(axis=1, skipna=True))
                        .groupby("NOTAS_NUM_NS")["_total"]
                        .sum())

            def somase_de_lista(lista_acoes, getter):
                serie_total = None
                if isinstance(lista_acoes, str):
                    lista_acoes = [lista_acoes]
                lista_acoes = [a for a in (lista_acoes or []) if a]

                for acao in lista_acoes:
                    df_tmp = getter(acao)
                    if df_tmp is not None and not df_tmp.empty:
                        serie = somase_por_ns(df_tmp)
                        serie_total = serie if serie_total is None else serie_total.add(serie, fill_value=0)

                return serie_total

            # >>> NOVO: dicionário pessoa -> DataFrame (sheet do Excel)
            planilhas = {}

            for pessoa in self.lista_pessoas:
                df_src = self.AcoesConcGmax.dataframe
                dfs_por_atv = []

                if len(pessoa.lista_atividades) == 0:
                    continue

                for atv in pessoa.lista_atividades:

                    mask = (df_src["TACOES_DES"].eq(atv.acao)) & (df_src["USUARIOS_NOM"].eq(pessoa.nome))
                    df_atv = df_src[mask].copy()
                    if df_atv.empty:
                        continue

                    serie_comp = somase_de_lista(
                        getattr(atv, "acao_comparar", []),
                        self.AcoesConcGmax.get_df_acao_comparar
                    )
                    serie_red = somase_de_lista(
                        getattr(atv, "acao_reduzir", []),
                        self.AcoesConcGmax.get_df_acao_reduzir
                    )

                    if serie_comp is not None:
                        df_atv["SOMA_ACOES_COMPARAR"] = df_atv["NOTAS_NUM_NS"].map(serie_comp).fillna(0)

                    if serie_red is not None:
                        df_atv["SOMA_ACOES_REDUZIR"] = df_atv["NOTAS_NUM_NS"].map(serie_red).fillna(0)

                    cols_base = ["NOTAS_NUM_NS", "TSERVICOS_CT_COD", "TACOES_DES", "ACOES_DAT_CONCLUSAO",
                                 atv.coluna_referencia]
                    cols_extra = []
                    if "SOMA_ACOES_COMPARAR" in df_atv.columns:
                        cols_extra.append("SOMA_ACOES_COMPARAR")
                    if "SOMA_ACOES_REDUZIR" in df_atv.columns:
                        cols_extra.append("SOMA_ACOES_REDUZIR")

                    df_atv = df_atv[cols_base + cols_extra]
                    columns = {"NOTAS_NUM_NS": "NS", "TSERVICOS_CT_COD": "Serviço", "TACOES_DES": "Ação",
                               "ACOES_DAT_CONCLUSAO": "Conclusão", atv.coluna_referencia: "US",
                               "SOMA_ACOES_REDUZIR": "Redução", "SOMA_ACOES_COMPARAR": "Comparação"}
                    df_atv = df_atv.rename(columns=columns)

                    # Metadados para o PDF
                    df_atv.attrs["reduzir"] = list(getattr(atv, "acao_reduzir", []) or [])
                    df_atv.attrs["comparar"] = list(getattr(atv, "acao_comparar", []) or [])
                    df_atv.attrs["valor_unidade"] = float(getattr(atv, "valor_unidade", 0) or 0)
                    df_atv.attrs["unidade_pagamento"] = str(getattr(atv, "unidade_pagamento", "") or "")

                    # Valor a Pagar (permitindo negativo se Redução > US)
                    if atv.unidade_pagamento == "US":
                        base_us = pd.to_numeric(df_atv["US"], errors="coerce").fillna(0)
                        redu = pd.to_numeric(df_atv.get("Redução"), errors="coerce").fillna(
                            0) if "Redução" in df_atv.columns else 0
                        df_atv["Valor a Pagar"] = (base_us - redu) * float(atv.valor_unidade)
                    elif atv.unidade_pagamento == "NS":
                        df_atv["Valor a Pagar"] = float(atv.valor_unidade)

                    dfs_por_atv.append(df_atv)

                if dfs_por_atv:
                    # PDF por pessoa
                    Utils._exportar_pdf_pessoa(pessoa, dfs_por_atv, self.start_date, self.end_date,
                                               pasta_out=".\\exported_data")

                    # >>> NOVO: montar DataFrame único da pessoa para o Excel
                    planilhas[pessoa.nome] = Utils._unir_dfs_para_excel(dfs_por_atv)

            # >>> NOVO: Excel com uma aba por pessoa
            if planilhas:
                Utils._exportar_xlsx(planilhas, self.start_date, self.end_date, pasta_out=".\\exported_data")

            return "Relação exportada com sucesso."

        except Exception as e:
            return f"Erro ao exportar relação. {str(e)}"



