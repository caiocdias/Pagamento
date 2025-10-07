import datetime

from Model import AcoesConcGmax

class ControllerAcoesConcGmax:
    def __init__(self, lista_pessoas : list, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self.lista_pessoas = lista_pessoas
        self.AcoesConcGmax = AcoesConcGmax(self.start_date, self.end_date)

    def gerar_producao(self):
        try:
            for pessoa in self.lista_pessoas:
                df_src = self.AcoesConcGmax.dataframe
                dfs_por_atv = []

                if len(pessoa.lista_atividades) == 0:
                    continue

                for atv in pessoa.lista_atividades:
                    if atv.origem != "AcoesConcGmax":
                        continue

                    mask = (df_src["TACOES_DES"].eq(atv.acao)) & (df_src["USUARIOS_NOM"].eq(pessoa.nome))
                    df_atv = df_src[mask].copy()
                    if df_atv.empty:
                        continue

                    df_atv = df_atv[["NOTAS_NUM_NS", "TSERVICOS_CT_COD", "TACOES_DES", "ACOES_DAT_CONCLUSAO", atv.coluna_referencia]]
                    dfs_por_atv.append(df_atv)

                if len(dfs_por_atv) != 0:
                    for df in dfs_por_atv:
                        df.to_excel(f".\\exported_data\\{pessoa.nome}_{df["TACOES_DES"].iloc[0]}.xlsx", index=None)
            return "Relação exportada com sucesso."

        except Exception as e:
            return f"Erro ao exportar relação. {str(e)}"
