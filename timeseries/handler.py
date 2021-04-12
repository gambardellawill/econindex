#  -*- coding:utf-8 -*- 

import abc
from datetime import datetime

class TimeSeriesHandler(metaclass=abc.ABCMeta):
    """
    Implements a time series handler interface.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_series') and
            callable(subclass.get_series))
    
    @abc.abstractmethod
    def get_series(self, series_code: str, date: datetime):
        """
        Load time series data from a data source. For more information,
        refer to the documentation of the desired implementation for
        this function.

        Raises:
            NotImplementedError: method not implemented in inherited class.
        """

        raise NotImplementedError