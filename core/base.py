# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:20:34 2020

@author: sixingliu, yaruchen
"""
import pandas as pd
import numpy as np
#from pandas.core.indexes.numeric import (NumericIndex, Float64Index,  # noqa
#                                    Int64Index, UInt64Index)
#from pandas.core.indexes.datetimes import DatetimeIndex
        


class BaseSensorSeries(pd.Series):

    @property
    def _constructor(self):
        return BaseSensorSeries

    @property
    def _constructor_expanddim(self):
        return BaseSensorFrame

    @property
    def time(self):
        return self.index
    
    @time.setter
    def time(self, time):
        # TODO: add index validtion function
        time = np.array(time)
        self.index = time
        
    @property
    def sigs(self):
        return self.values
    
    @sigs.setter
    def sigs(self, sigs):
        # TODO: add signal validtion function
        sigs = np.array(sigs)
        self.values = sigs
    
    _frequency = None

    @property
    def frequency(self):
        return self._frequency
    
    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency
        


class BaseSensorFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return BaseSensorFrame

    @property
    def _constructor_sliced(self):
        return BaseSensorSeries

    @property
    def time(self):
        return self.index
    
    @time.setter
    def time(self, time):
        # TODO: add index validtion function
        time = np.array(time)
        self.index = time
        
    @property
    def sigs(self):
        return self.values
    
    @sigs.setter
    def sigs(self, sigs):
        # TODO: add signal validtion function
        sigs = np.array(sigs)
        self.values = sigs
    
    _frequency = None

    @property
    def frequency(self):
        return self._frequency
    
    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency

    
    
@pd.api.extensions.register_series_accessor("freq")
@pd.api.extensions.register_dataframe_accessor("freq")
class FreqAccessor:
    
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
      pass
    
    @property
    def frequency(self):
        return self._obj.frequency
    
    @frequency.setter
    def frequency(self, frequency):
        self._obj.frequency = frequency    
    
    def to_freqindex(self, frequency=None):
        if not frequency:
            frequency = self.frequency
        self._obj.index = self._obj.index / frequency

