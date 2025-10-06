import pandas as pd

from Data import DatabaseHandler

class AcoesConcGmax:
    def __init__(self, start_date: str, end_date: str):
        self.dataframe = None
        self.start_date = start_date
        self.end_date = end_date

    def load_dataframe(self):
        query = f"SELECT * FROM vBIAcoes WHERE ACOES_DAT_CONCLUSAO BETWEEN cast('{self.start_date}' as datetime) AND cast('{self.end_date}' as datetime)"
        db = DatabaseHandler('192.168.10.250', 'GMAX', 'U_PBI_READ', 'GMaxWebBI#2025')

        self.dataframe = pd.read_sql(query, db.get_sqlalchemy_engine())