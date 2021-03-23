#  -*- coding:utf-8 -*-

from timeseries import bcb
from datetime import datetime, timedelta

if __name__ == "__main__":
    ts = bcb.BCBTimeSeriesHandler()  
    
    print(ts.get_last_series(1)) # Dólar comerical venda
    print(ts.get_last_series(10813)) # Dólar comercial compra
    print(ts.selic()) # Taxa Selic
    print(ts.get_last_series(12)) # CDI
    print(ts.get_last_series(189)) # IGP-M
    print(ts.get_last_series(190)) # IGP-DI
    print(ts.get_last_series(7453)) # IPC-M
    print(ts.get_last_series(7809)) # Dow Jones
    print(ts.get_last_series(7810)) # Nasdaq

    # Getting an interval
    print(ts.get_series(10813, datetime.today() - timedelta(days=30), datetime.today()))

    # Get daily variation
    print(ts.quotation(10813))