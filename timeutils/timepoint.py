# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:14:17 2020

@author: sixingliu, yaruchen
"""
import datetime as dt
import time

class TimePoint(dt.datetime):
    ## TODO: add completed notation
    """
    TimePoint 
    """
    def __init__(self, timepoint):
        super(TimePoint, self).__init__(timepoint)
        self.timepoint = timepoint
        self._valid = self._is_valid()
    
    def _ts_to_dt(self):
        """
        Convert UNIX time to datetime
        """
        if isinstance(self.timepoint, int) and self._valid:
            timepoint = dt.datetime.fromtimestamp(self.timepoint)
        else:
            raise ValueError('Invalid Time Point Type')
        return timepoint
           
    def _str_to_dt(self):
        """
        Convert str to datetime
        """
        if isinstance(self.timepoint, str) and self._valid:
            timepoint = time.strftime('%Y-%m-% %H:%M:%S', self.timepoint)
        else:
            raise ValueError('Invalid Time Point Type')
        return timepoint
                        
    def _is_valid(self):
        if isinstance(self.timepoint, dt.datetime):
            return True
        elif isinstance(self.timepoint, int):
            if len(self.timepoint) == 13:
                return True
            else:
                return False
        elif isinstance(self.timepoint, str):
            # TODO: Add str valid rule
            return True
        else:
            return False
    
    def to_timepoint(self):
        self._valid = self._is_valid()
        if not self._valid:
            raise ValueError('Invalid Time Point Type')
        if isinstance(self.timepoint, str):
            self.timepoint = self._str_to_dt()
        if isinstance(self.timepoint, int):
            self.timepoint = self._ts_to_dt()
            
    def to_rollback(self, tm='min'):
        ## TODO: rollback to End tm (completed Notation)
        """
        """
        ## TODO: add other level
        self.to_timepoint()
        self.timepoint = dt.datetime(year=self.timepoint.year,
                                     month=self.timepoint.month,
                                     day=self.timepoint.day,
                                     hour=self.timepoint.hour,
                                     minute=self.timepoint.minute,
                                     second=0)  
        return self.timepoint
        
    def to_rollforword(self, tm='min'):
        ## TODO: rollforword to End tm (completed Notation)
        """
        """
        ## TODO: add other level
        self.to_timepoint()
        self.timepoint = self.timepoint + dt.timedelta(minutes=1)
        self.to_timepoint()        
        return self.timepoint    
        

def rollback_minute(tpoint):
    ## TODO: add more level
    if isinstance(tpoint, dt.datetime):
        tpoint_ = dt.datetime(year=tpoint.year,
                              month=tpoint.month,
                              day=tpoint.day,
                              hour=tpoint.hour,
                              minute=tpoint.minute,
                              second=0)
    else:
        tpoint_ = tpoint
    return tpoint_

def rollforword_minute(tpoint):
    ## TODO: add more level
    if isinstance(tpoint, dt.datetime):
        tpoint_ = dt.datetime(year=tpoint.year,
                              month=tpoint.month,
                              day=tpoint.day,
                              hour=tpoint.hour,
                              minute=tpoint.minute+1,
                              second=0)
    else:
        tpoint_ = tpoint
    return tpoint_