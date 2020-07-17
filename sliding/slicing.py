#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:11:06 2019

@author: sixingliu, yaruchen
"""

import numpy as np
import pandas as pd
from pandas.tseries.offsets import Hour, Minute, Second, DateOffset
import sensorpowa.timeutils.timepoint as stp
from pandas.core.indexes.numeric import (NumericIndex, Float64Index,
                                         Int64Index, UInt64Index)
from pandas.core.indexes.datetimes import DatetimeIndex
#from collections import deque
    
class BaseSlidingWindow(object):
    
    def __init__(self, length, overlap, min_size, 
                 normalize, closed, label=None):
        self.length = length
        self.overlap = overlap
        self.min_size = min_size
        self.normalize = normalize
        self.closed = closed
        self.label = label
        
    def _get_slice_index(self):
        return NotImplementedError
    
    def _to_slice_windows(self):
        return NotImplementedError
    
    def transform(self, measurement, index=False):
        return NotImplementedError


  
class DatetimeIndexSlidingWindow(BaseSlidingWindow):
    
    def __init__(self, length, overlap, min_size, 
                 normalize, closed, label=None):
        self.length = length
        self.overlap = overlap
        self.min_size = min_size
        self.normalize = normalize
        self.closed = closed
        self.label = label
                
    def _get_slice_index(self, start=None, end=None, periods=None, **kwargs):
        """
        Time Array
        """
        if not periods:
            periods = None    
        
        if self.normalize:
            start = stp.rollback_minute(start)
            end = stp.rollforword_minute(end)
        
        freq = round(self.length * (1-self.overlap))
        freq = str(freq) + 's'
        
        # TODO: Here we use datetime array to get every 
        # start points and end points of windows during whole timeline 
        dtarr = pd.date_range(start=start, end=end, 
                              periods=periods,
                              freq=freq, **kwargs) # generate datetime array
        dtarr_start = dtarr[:-1]
        dtarr_end = dtarr_start + Second(self.length)
        
        if self.closed == 'right':
            dtarr_start = dtarr_start - Second(1)
            
        if self.closed == 'left':
            dtarr_end = dtarr_end - Second(1) 
    
        _index = range(len(dtarr_start))
        # merge start times list and end times list           
        dt_index = list(map(lambda i: (dtarr_start[i], dtarr_end[i]), _index))
        return dt_index        
    
    def _to_slice_windows(self, measurement, slice_index, time_index=True):
        """
            slice_index: [0] start [1] end
        """
        if time_index:
            windows = list(map(lambda idx: measurement.loc[idx[0]: idx[1], :].reset_index(drop=False), slice_index))
        else:
            windows = list(map(lambda idx: measurement.loc[idx[0]: idx[1], :], slice_index))
        return windows
        
    def _get_label(df):
        pass
        
    def transform(self, measurement, time_index=True):
        """
        """
        def _drop_windows(windows, min_size):
            windows_ = list()
            for window in windows:
                if len(window) >= min_size:
                    windows_.append(window)
            return windows_
                      
        start = measurement.index[0]
        end = measurement.index[-1]
        slice_index = self._get_slice_index(start, end)
        windows = self._to_slice_windows(measurement, slice_index, time_index=time_index)
        windows = _drop_windows(windows, self.min_size)
        self.windows = list(windows)
        return list(windows)        
        
        

class NumericIndexSlidingWindow(BaseSlidingWindow):
    
    def __init__(self, length, overlap, min_size, 
                 normalize=True, closed=True, label=None):
        self.length = length
        self.overlap = overlap
        self.min_size = min_size
        self.normalize = normalize
        self.closed = closed
        self.label = label
                
    def _get_slice_index(self, start=None, end=None, periods=None, **kwargs):
        """
        Index Array
        """
        if not periods:
            periods = None    
        
        if self.normalize:
            start = stp.rollback_minute(start)
            end = stp.rollforword_minute(end)
        
        freq = round(self.length * (1-self.overlap))
        
        # TODO: Here we use datetime array to get every 
        # start points and end points of windows during whole timeline 
        intarr = np.arange(start, end, freq)
        intarr_start = intarr[:-1]
        intarr_end = intarr_start + self.length
    
        _index = range(len(intarr_start))  
        # merge start times list and end times list          
        int_index = list(map(lambda i: (intarr_start[i], intarr_end[i]), _index))
        return int_index        
    
    def _to_slice_windows(self, measurement, slice_index, int_index=True):
        """
            slice_index: [0] start [1] end
        """
        if int_index:
            windows = list(map(lambda idx: measurement[idx[0]: idx[1]].reset_index(drop=False), slice_index))
        else:
            windows = list(map(lambda idx: measurement[idx[0]: idx[1]], slice_index))
        return windows
        
    def _get_label(df):
        pass
        
    def transform(self, measurement, int_index=False):
        """
        """
        def _drop_windows(windows, min_size):
            windows_ = list()
            for window in windows:
                if len(window) >= min_size:
                    windows_.append(window)
            return windows_
                      
        start = measurement.index[0]
        end = measurement.index[-1]
        slice_index = self._get_slice_index(start, end)
        print(slice_index)
        windows = self._to_slice_windows(measurement, slice_index, int_index=int_index)
        windows = _drop_windows(windows, self.min_size)
        self.windows = list(windows)
        return list(windows)
    
    

    
    
    
    
    
    