# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:31:21 2020

@author: sixingliu, yaruchen
"""

from sensorpowa.core.series import SensorSeries

class _SensorHR(SensorSeries):
    
    def to_rri(self):
        pass
    
    def bandpass(self, frequency):
        super(_SensorHR, self).bandpass(frequency)
        pass
