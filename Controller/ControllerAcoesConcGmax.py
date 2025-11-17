# ControllerAcoesConcGmax.py

import datetime
from Generic import Utils
from Model import AcoesConcGmax
import pandas as pd
import os


class ControllerAcoesConcGmax:
    def __init__(self, lista_pessoas: list, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.lista_pessoas = lista_pessoas
        self.AcoesConcGmax = AcoesConcGmax(self.start_date, self.end_date)

    def gerar_producao(self):
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

        planilhas = {}
        df_src = self.AcoesConcGmax.dataframe

        for pessoa in self.lista_pessoas:
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

                df_atv.attrs["reduzir"] = list(getattr(atv, "acao_reduzir", []) or [])
                df_atv.attrs["comparar"] = list(getattr(atv, "acao_comparar", []) or [])
                df_atv.attrs["valor_unidade"] = float(getattr(atv, "valor_unidade", 0) or 0)
                df_atv.attrs["unidade_pagamento"] = str(getattr(atv, "unidade_pagamento", "") or "")

                if atv.unidade_pagamento == "US":
                    base_us = pd.to_numeric(df_atv["US"], errors="coerce").fillna(0)
                    redu = pd.to_numeric(df_atv.get("Redução"), errors="coerce").fillna(
                        0) if "Redução" in df_atv.columns else 0
                    df_atv["Valor a Pagar"] = (base_us - redu) * float(atv.valor_unidade)
                elif atv.unidade_pagamento == "NS":
                    df_atv["Valor a Pagar"] = float(atv.valor_unidade)

                dfs_por_atv.append(df_atv)

            if dfs_por_atv:
                Utils._exportar_pdf_pessoa(pessoa, dfs_por_atv, self.start_date, self.end_date,
                                           pasta_out=".\\exported_data")

                planilhas[pessoa.nome] = Utils._unir_dfs_para_excel(dfs_por_atv)

        if planilhas:
            Utils._exportar_xlsx(planilhas, self.start_date, self.end_date, pasta_out=".\\exported_data")

        return "Relação exportada com sucesso."

    def gerar_producao_por_supervisor(self, lista_supervisores: list):
        cols_soma = ["ACOES_QTD_US_INTERNA", "ACOES_QTD_US_TOP", "ACOES_QTD_US_PRJ", "ACOES_QTD_US_GEO"]

        def somase_por_ns(df):
            return (df.assign(_total=df[cols_soma].sum(axis=1, skipna=True))
                    .groupby("NOTAS_NUM_NS")["_total"].sum())

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

        df_src = self.AcoesConcGmax.dataframe

        for supervisor in (lista_supervisores or []):
            # monta subpasta do período
            periodo = f"{self.start_date:%Y-%m-%d}_a_{self.end_date:%Y-%m-%d}"
            pasta_out = os.path.join(supervisor.pasta, periodo)
            os.makedirs(pasta_out, exist_ok=True)

            planilhas = {}

            # percorre pessoas associadas ao supervisor
            for pessoa in getattr(supervisor, "lista_pessoas", []) or []:
                if not getattr(pessoa, "lista_atividades", []):
                    continue

                dfs_por_atv = []

                for atv in pessoa.lista_atividades:
                    mask = (df_src["TACOES_DES"].eq(atv.acao)) & (df_src["USUARIOS_NOM"].eq(pessoa.nome))
                    df_atv = df_src[mask].copy()
                    if df_atv.empty:
                        continue

                    serie_comp = somase_de_lista(getattr(atv, "acao_comparar", []), self.AcoesConcGmax.get_df_acao_comparar)
                    serie_red  = somase_de_lista(getattr(atv, "acao_reduzir",  []), self.AcoesConcGmax.get_df_acao_reduzir)

                    if serie_comp is not None:
                        df_atv["SOMA_ACOES_COMPARAR"] = df_atv["NOTAS_NUM_NS"].map(serie_comp).fillna(0)
                    if serie_red is not None:
                        df_atv["SOMA_ACOES_REDUZIR"]  = df_atv["NOTAS_NUM_NS"].map(serie_red).fillna(0)

                    cols_base = ["NOTAS_NUM_NS", "TSERVICOS_CT_COD", "TACOES_DES", "ACOES_DAT_CONCLUSAO", atv.coluna_referencia]
                    cols_extra = []
                    if "SOMA_ACOES_COMPARAR" in df_atv.columns:
                        cols_extra.append("SOMA_ACOES_COMPARAR")
                    if "SOMA_ACOES_REDUZIR" in df_atv.columns:
                        cols_extra.append("SOMA_ACOES_REDUZIR")

                    df_atv = df_atv[cols_base + cols_extra]
                    columns = {
                        "NOTAS_NUM_NS": "NS",
                        "TSERVICOS_CT_COD": "Serviço",
                        "TACOES_DES": "Ação",
                        "ACOES_DAT_CONCLUSAO": "Conclusão",
                        atv.coluna_referencia: "US",
                        "SOMA_ACOES_REDUZIR": "Redução",
                        "SOMA_ACOES_COMPARAR": "Comparação",
                    }
                    df_atv = df_atv.rename(columns=columns)

                    # metadados para PDF
                    df_atv.attrs["reduzir"] = list(getattr(atv, "acao_reduzir", []) or [])
                    df_atv.attrs["comparar"] = list(getattr(atv, "acao_comparar", []) or [])
                    df_atv.attrs["valor_unidade"] = float(getattr(atv, "valor_unidade", 0) or 0)
                    df_atv.attrs["unidade_pagamento"] = str(getattr(atv, "unidade_pagamento", "") or "")

                    # valor a pagar
                    if atv.unidade_pagamento == "US":
                        base_us = pd.to_numeric(df_atv["US"], errors="coerce").fillna(0)
                        redu = pd.to_numeric(df_atv.get("Redução"), errors="coerce").fillna(0) if "Redução" in df_atv.columns else 0
                        df_atv["Valor a Pagar"] = (base_us - redu) * float(atv.valor_unidade)
                    elif atv.unidade_pagamento == "NS":
                        df_atv["Valor a Pagar"] = float(atv.valor_unidade)

                    dfs_por_atv.append(df_atv)

                if dfs_por_atv:
                    # PDF da pessoa dentro da pasta do supervisor/período
                    Utils._exportar_pdf_pessoa(pessoa, dfs_por_atv, self.start_date, self.end_date, pasta_out=pasta_out)
                    # sheet dessa pessoa para o Excel do supervisor
                    planilhas[pessoa.nome] = Utils._unir_dfs_para_excel(dfs_por_atv)

            # Excel do supervisor (uma aba por pessoa do supervisor)
            if planilhas:
                Utils._exportar_xlsx(planilhas, self.start_date, self.end_date, pasta_out=pasta_out)

        return "Relação por supervisor exportada com sucesso."

# ControllerAcoesConcGmax.py

    def gerar_pagamento_metas(self, lista_supervisores=None):
        df_src = self.AcoesConcGmax.dataframe

        # Mapa: matricula da pessoa -> [supervisores]
        mapa_pessoa_sup = {}
        if lista_supervisores:
            for supervisor in (lista_supervisores or []):
                for pessoa_sup in getattr(supervisor, "lista_pessoas", []) or []:
                    mat = getattr(pessoa_sup, "matricula", None)
                    if mat:
                        mapa_pessoa_sup.setdefault(mat, []).append(supervisor)

        for pessoa in self.lista_pessoas:
            meta = getattr(pessoa, "meta", None)
            if meta is None:
                continue

            # Filtra ações da meta para a pessoa
            df_pessoa = df_src[
                (df_src["USUARIOS_NOM"].eq(pessoa.nome)) &
                (df_src["TACOES_DES"].isin(meta.acoes))
            ].copy()

            if df_pessoa.empty:
                continue

            # DataFrame de detalhamento da produção (por extenso)
            cols_base = ["NOTAS_NUM_NS", "TSERVICOS_CT_COD", "TACOES_DES", "ACOES_DAT_CONCLUSAO"]
            cols_extra = []

            # Se a unidade da meta for US, utilizamos as colunas de US configuradas na meta
            for col in getattr(meta, "colunas_us", []) or []:
                if col in df_pessoa.columns:
                    cols_extra.append(col)

            df_detalhe = df_pessoa[cols_base + cols_extra].copy()

            rename_cols = {
                "NOTAS_NUM_NS": "NS",
                "TSERVICOS_CT_COD": "Serviço",
                "TACOES_DES": "Ação",
                "ACOES_DAT_CONCLUSAO": "Conclusão",
            }
            df_detalhe = df_detalhe.rename(columns=rename_cols)

            # Produção em função da unidade da meta
            if meta.unidade == "NS":
                # quantidade de registros (cada ação nas ações da meta)
                producao_total = float(len(df_pessoa))
            elif meta.unidade == "US":
                producao_total = 0.0
                for col in getattr(meta, "colunas_us", []) or []:
                    if col in df_pessoa.columns:
                        producao_total += (
                            pd.to_numeric(df_pessoa[col], errors="coerce")
                            .fillna(0)
                            .sum()
                        )
            else:
                # Unidade inválida (não deve acontecer, é validada em Meta)
                continue

            # Calcula valor a pagar conforme forma de pagamento
            valor_pagamento = meta.calcular_pagamento(producao_total)

            # 1) PDF geral na pasta padrão
            Utils._exportar_pdf_meta(
                pessoa,
                meta,
                producao_total,
                valor_pagamento,
                self.start_date,
                self.end_date,
                df_producao=df_detalhe,
                pasta_out=".\\exported_data"
            )

            # 2) PDF na(s) pasta(s) do(s) supervisor(es) da pessoa, por período
            mat = getattr(pessoa, "matricula", None)
            supervisores_pessoa = mapa_pessoa_sup.get(mat, [])
            for supervisor in supervisores_pessoa:
                periodo = f"{self.start_date:%Y-%m-%d}_a_{self.end_date:%Y-%m-%d}"
                pasta_out_sup = os.path.join(supervisor.pasta, periodo)
                os.makedirs(pasta_out_sup, exist_ok=True)

                Utils._exportar_pdf_meta(
                    pessoa,
                    meta,
                    producao_total,
                    valor_pagamento,
                    self.start_date,
                    self.end_date,
                    df_producao=df_detalhe,
                    pasta_out=pasta_out_sup
                )

        return "Relatórios de metas exportados com sucesso."

