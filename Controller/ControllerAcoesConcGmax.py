from Model import AcoesConcGmax

class ControllerAcoesConcGmax:
    def __init__(self, lista_pessoas : list, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date

        self.AcoesConcGmax = AcoesConcGmax(self.start_date, self.end_date)

