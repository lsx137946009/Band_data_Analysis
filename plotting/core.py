# -*- coding: utf-8 -*-
# from sensorpowa.core.base import BaseSensorSeries
# from sensorpowa.core.base import BaseSensorFrame
import matplotlib.pyplot as plt

class BasePlot(object):
   
    @property
    def _kind(self):
        """Specify kind str Must be overridden in child class"""
        raise NotImplementedError
        
    def __init__(self, data, ax=None, fig=None, **kwargs):
        self.data = data
        self.ax = ax
        self.fig = fig
        self.kwargs = kwargs
        
    def _plot(self):
        """Specify _plot function Must be overridden in child class"""
        raise NotImplementedError
        

class LinePlot(BasePlot):
    _kind = 'line'
    
    def __init__(self, data, ax=None, fig=None, **kwargs):
        self.data = data
        self.ax = ax
        self.fig = fig
        self.kwargs = kwargs
              
    def _plot(self, **kwargs):      
        kwgs_setscatter = {'s':16,
                            'marker':'*',
                            'edgecolor':[0,0,1], 
                            'facecolor':[0,0,1], 
                            'linewidth':1}
        kwgs_setplot = {'linestyle':'--',
                        'color':[0,0,1],
                        'linewidth':1}
        x = self.data.time
        y = self.data.sigs
        plt.scatter(x, y, **kwgs_setscatter)
        plt.plot(x, y, **kwgs_setplot)

        
class BarPlot(BasePlot):
    _kind = 'bar'
    
    def __init__(self, data, ax=None, fig=None, **kwargs):
        self.data = data
        self.ax = ax
        self.fig = fig
        self.kwargs = kwargs
              
    def _plot(self):
        print('plot bar')


class HistPlot(BasePlot):
    _kind = 'hist'
    
    def __init__(self, data, ax=None, fig=None, **kwargs):
        self.data = data
        self.ax = ax
        self.fig = fig
        self.kwargs = kwargs
              
    def _plot(self):
        print('plot hist')


class BoxPlot(BasePlot):
    _kind = 'box'
    
    def __init__(self, data, ax=None, fig=None, **kwargs):
        self.data = data
        self.ax = ax
        self.fig = fig
        self.kwargs = kwargs
              
    def _plot(self):
        print('plot box')


class ScatterPlot(BasePlot):
    _kind = 'scatter'
    
    def __init__(self, data, ax=None, fig=None, **kwargs):
        self.data = data
        self.ax = ax
        self.fig = fig
        self.kwargs = kwargs
              
    def _plot(self):
        print('plot scatter')


_klasses = [LinePlot, BarPlot, HistPlot, BoxPlot, ScatterPlot]
plot_klass = {klass._kind: klass for klass in _klasses}

def plot(data, kind, ax=None, fig=None, **kwargs):
    klass = plot_klass[kind]
    plot_obj = klass(data, ax, fig, **kwargs)
    return plot_obj._plot()
    
    

#class dataPlot(Basedata):
#    
#    def __init__(self, ax=None, fig=None):
#        super(dataPlot, self).__init__(ax, fig)
#        self.ax = ax
#        self.fig = fig
#        
#        
#    def mplot(self, **kwargs):
#        kind = 'line'
#        return _plot(self, kind, self.ax, self.fig, **kwargs)
#    
#    def mhist(self, **kwargs):
#        kind = 'hist'
#        return _plot(self, kind, self.ax, self.fig, **kwargs)
#    
#    def mboxplot(self, **kwargs):
#        kind = 'boxplot'
#        return _plot(self, kind, self.ax, self.fig, **kwargs)
#    
#    def mscatter(self, **kwargs):
#        kind = 'scatter'
#        return _plot(self, kind, self.ax, self.fig, **kwargs)
#    
#    def mbar(self, **kwargs):
#        kind = 'bar'
#        return _plot(self, kind, self.ax, self.fig, **kwargs)


