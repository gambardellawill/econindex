#  -*- coding:utf-8 -*-
import abc
import json
from timeseries import handler
from datetime import *
from zeep import Client, exceptions

class BCBTimeSeriesHandler(handler.TimeSeriesHandler):
    """
    Downloads time series data from the BCB.
    """

    def __init__(self):
        self.client = Client('https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl')

    def get_series(self, series_code, initial_date: date, final_date: date):
        arrayOfLong = self.client.get_type('{http://DefaultNamespace}ArrayOfflong')
        data_points = []

        if (final_date.date() == initial_date.date()):
            initial_date -= timedelta(days=1)
       
        final_date = final_date - timedelta(days=1)*(final_date.weekday() == 5) - timedelta(days=2)*(final_date.weekday() == 6)
        initial_date = initial_date - timedelta(days=1)*((initial_date.weekday() == 5)) - timedelta(days=2)*(initial_date.weekday() == 6)
        
        try:
            response = self.client.service.getValoresSeriesVO(
                arrayOfLong([series_code]),
                initial_date.strftime("%d/%m/%Y"),
                final_date.strftime("%d/%m/%Y")) 
            for entry in response[0]['valores']:
                data_points.append(float(entry['valor']['_value_1']))
            return { "index": response[0]['nomeAbreviado']['_value_1'], "rates": data_points }
        except:
            print("Unable to get response :/")

    def get_last_series(self, series_code):
        try:
            response = self.client.service.getUltimoValorVO(series_code)
            return { "index" : response['nomeAbreviado']['_value_1'],
                "rate" : float(response['ultimoValor']['valor']['_value_1']) }
        except:
            print("Unable to get response :/")

    def quotation(self, series_code):
        prices= self.get_series(series_code, datetime.today() - timedelta(days=2), datetime.today())

        variation = ((prices['rates'][1] - prices['rates'][0])/prices['rates'][0])
        return { "index": prices['index'],
            "price" : prices['rates'][1] ,
            "variation" : variation }
    
    def selic(self):
        return self.get_last_series(11)