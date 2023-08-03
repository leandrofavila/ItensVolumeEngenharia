import cx_Oracle
import pandas as pd


class DB:
    def __init__(self, carregamento, item):
        self.carregamento = carregamento
        self.item = item


    @staticmethod
    def connection():
        dsn = cx_Oracle.makedsn("10.40.3.10", 1521, service_name="f3ipro")
        connection = cx_Oracle.connect(user=r"focco_consulta", password=r'consulta3i08', dsn=dsn, encoding="UTF-8")
        cur = connection.cursor()
        return cur


    def vol_car(self):
        print(self.carregamento)
        cur = self.connection()
        cur.execute(
            r"SELECT CAR.CARREGAMENTO, VOL.CODIGO, COM.COD_ITEM, TIT.DESC_TECNICA, ITE.QTDE "
            r"FROM FOCCO3I.TSRENGENHARIA_VOLUMES VOL "
            r"INNER JOIN FOCCO3I.TSRENGENHARIA_CARREGAMENTOS CAR  ON CAR.ID = VOL.SR_CARREG_ID "
            r"INNER JOIN FOCCO3I.TSRENGENHARIA_VOL_ITE ITE        ON ITE.SR_VOL_ID = VOL.ID "
            r"INNER JOIN FOCCO3I.TITENS_PDV PDV                   ON PDV.ID = ITE.ITPDV_ID "
            r"INNER JOIN FOCCO3I.TITENS_COMERCIAL COM             ON COM.ID = PDV.ITCM_ID "
            r"INNER JOIN FOCCO3I.TITENS TIT                       ON TIT.COD_ITEM = COM.COD_ITEM "
            r"WHERE CAR.CARREGAMENTO = "+str(self.carregamento)+" "
            r"ORDER BY CAR.CARREGAMENTO DESC, VOL.CODIGO "
        )
        vol_car = cur.fetchall()
        vol_car = pd.DataFrame(vol_car, columns=['CARREGAMENTO', 'CODIGO_VOLUME', 'COD_ITEM', 'DESC_TECNICA', 'QTDE'])
        #vol_car = vol_car[vol_car['QTDE'].astype(int)]
        print(vol_car.to_string())
        return vol_car

