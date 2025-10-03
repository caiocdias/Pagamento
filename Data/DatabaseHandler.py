import pyodbc
from sqlalchemy import create_engine

class DatabaseHandler:
    def __init__(self, server: str, database: str, username: str, password: str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def get_pyodbc_connection(self):
        connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=yes;TrustServerCertificate=yes"
        return pyodbc.connect(connection_string)

    def get_sqlalchemy_engine(self):
        connection_url = (
            f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?"
            f"driver=ODBC+Driver+18+for+SQL+Server"
            f"&Encrypt=yes"
            f"&TrustServerCertificate=yes"
        )
        return create_engine(connection_url)