#  -*- coding:utf-8 -*-
import abc
import json
from timeseries import handler
from datetime import *
from zeep import Client, exceptions

class BCBTimeSeriesHandler(handler.TimeSeriesHandler):
    """
    Handles the download and formatting of time series data from the BCB.

    Attributes:
        client: A Zeep Client object that connects to BCB's time series SOAP webservice.
    """

    def __init__(self):
        self.client = Client('https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl')

    def get_series(self, series_code, initial_date: date, final_date: date):
        """
        Returns the values for a time series index according to a set date interval.

        Args:
            series_code (str): Code for the timeseries according to the Brazilian Central Bank's (BCB) webservice spec.
            initial_date (date): Start of the date interval.
            final_date (date): End of the date interval.
        
        Returns:
            dict: a dictionary containing the name for the index series and all data points ranging from the beginning 
            to the end of the set interval. For example:

            {
                "index" : "SELIC",
                "rates" : [0.345, 0.336, 0.309, 0.317]
            }
        """

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
        """
        Returns the latest value for that series index.

        Args:
            series_code (str): Code for the timeseries according to the Brazilian Central Bank's (BCB) webservice spec.
        
        Returns:
            dict: a dictionary containing the name for the index series and its latest value. For example:

            {
                "index" : "SELIC",
                "rate"  : 0.345
            }
        """

        try:
            response = self.client.service.getUltimoValorVO(series_code)
            return { "index" : response['nomeAbreviado']['_value_1'],
                "rate" : float(response['ultimoValor']['valor']['_value_1']) }
        except:
            print("Unable to get response :/")

    def quotation(self, series_code):
        """
        Returns the latest value for that series index and the variation from
        the previous value. Used for displaying data in a similar way as stock prices.

        Args:
            series_code (str): Code for the timeseries according to the Brazilian Central Bank's (BCB) webservice spec.
        
        Returns:
            dict: a dictionary containing the name for the index series, current value and the variation percentage.
            Example:

            {
                "index"     : "SELIC",
                "price"     : 0.345,
                "variation" : 0.02678
            }
        """
        
        prices= self.get_series(series_code, datetime.today() - timedelta(days=2), datetime.today())

        variation = ((prices['rates'][1] - prices['rates'][0])/prices['rates'][0])
        return { "index": prices['index'],
            "price" : prices['rates'][1] ,
            "variation" : variation }
    
    def selic(self):
        return self.get_last_series(11)