import pandas as pd

from Data import DatabaseHandler

class AcoesConcGmax:
    def __init__(self, start_date, end_date):
        self.dataframe = None
        self.start_date = start_date
        self.end_date = end_date

        self._carregar_dataframe()
        self._tratar_dataframe()

    def _carregar_dataframe(self):
        query = f"SELECT * FROM vBIAcoes WHERE ACOES_DAT_CONCLUSAO BETWEEN cast('{self.start_date.strftime("%Y-%m-%d")}' as datetime) AND cast('{self.end_date.strftime("%Y-%m-%d")}' as datetime)"
        db = DatabaseHandler('192.168.10.250', 'GMAX', 'U_PBI_READ', 'GMaxWebBI#2025')

        self.dataframe = pd.read_sql(query, db.get_sqlalchemy_engine())

    def _tratar_dataframe(self):
        self.dataframe["ACOES_QTD_US_INTERNA"] = self.dataframe["ACOES_QTD_US_INTERNA"].replace(0.001, 0)
        self.dataframe["ACOES_QTD_US_GEO"] = self.dataframe["ACOES_QTD_US_GEO"].replace(0.001, 0)
        self.dataframe["ACOES_QTD_US_PRJ"] = self.dataframe["ACOES_QTD_US_PRJ"].replace(0.001, 0)
        self.dataframe["ACOES_QTD_US_TOP"] = self.dataframe["ACOES_QTD_US_TOP"].replace(0.001, 0)