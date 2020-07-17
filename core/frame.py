# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:20:34 2020

@author: sixingliu, yaruchen
"""

from pandas.core.indexes.numeric import (NumericIndex, Float64Index,
                                         Int64Index, UInt64Index)
from pandas.core.indexes.datetimes import DatetimeIndex
from sensorpowa.core.base import BaseSensorSeries
from sensorpowa.core.base import BaseSensorFrame
import sensorpowa.plotting.core as spc
from sensorpowa.filtering.outlier import SensorSeriesOutlier
from sensorpowa.sliding.slicing import (DatetimeIndexSlidingWindow,
                                        NumericIndexSlidingWindow)

class SensorFrame(BaseSensorFrame):
    
    def splot(self, kind='line', fig=None, ax=None, **kwargs):
        return spc.plot(self, kind='line', fig=None, ax=None, **kwargs)
        
    def sliding(self, **epoch):
        if isinstance(self.index, DatetimeIndex):
            return DatetimeIndexSlidingWindow(**epoch).transform(self)
        else:
            return NumericIndexSlidingWindow(**epoch).transform(self)


