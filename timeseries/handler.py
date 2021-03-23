#  -*- coding:utf-8 -*- 

import abc
from datetime import datetime

class TimeSeriesHandler(metaclass=abc.ABCMeta):
    """
    Implements the time series handler interface.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_series') and
            callable(subclass.get_series))
    
    @abc.abstractmethod
    def get_series(self, series_code: str, date: datetime):
        """Load time series data from a data source."""
        raise NotImplementedError