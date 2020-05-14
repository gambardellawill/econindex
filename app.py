#  -*- coding:utf-8 -*-

from zeep import Client, exceptions
from datetime import date

def selic():
    return get_last_series(11)

def get_last_series(series_code):
    today = "13/05/2020"
    return get_series(series_code, today)

def get_series(series_code, date):
    client = Client('https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl')
    try:
        response = client.service.getValor(series_code, date)
        return response['_value_1']
    except:
        print("Nao rolou :/")

if __name__ == "__main__":
    print(selic())

