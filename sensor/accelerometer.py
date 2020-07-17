# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:49:42 2020

@author: sixingliu, yaruchen
"""


from sensorpowa.core.frame import SensorFrame
from sensorpowa.core.series import SensorSeries
import numpy as np

class _SensorACM(SensorFrame):
    """
     The biosensor module also contains a three dimensional accelerometer 
     for measurements of physical activity. A microcontroller digitizes the 
     analog signals via a 12-bit A-D and the data is written to an onboard 
     microSD card. 
     # TODO: move to clinlic module
     - Seizure:
         Generalized tonic-clonic (GTC) seizures are composed of two primary phases
         -- the tonic phase and the clonic phase. 
         The tonic phase involves stiffening of the limbs and flexion or extension of 
         the neck, back and extremities. During the clonic phase, muscles of the entire
         body start to contract and relax rapidly. These convulsions are manifest in the
         ACM signal as rhythmic activity typically above 2 Hz.
         Thus, each epoch was evaluated for important periods using an algorithm by 
         Vlachos and colleagues (Vlachos et al., 2004). The underlying assumption is 
         that the magnitudes of the coefficients of the DFT of a non-periodic time 
         series are distributed according to an exponential distribution.  
    """

    def to_magnitude(self):
        """
         Combined information from all three axes of the accelerometer to 
         calculate the magnitude of the net acceleration

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        data = np.mat(self.vals)
        magnitude = np.linalg.norm(data, ord=2, axis=1, keepdims=True)
        return SensorSeries(magnitude)
    
    def pipeline(self, frequency, *pipe):
        """
        
        Parameters
        ----------
        frequency : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        for filter_pipe in pipe:
            self = filter_pipe.transform(self)
        return self
    
    def indicator_activate(self, window=None):
        """
        

        Returns
        -------
        bool
            DESCRIPTION.

        """
        indicator = np.std
        if indicator > 0.1:
            return True
        else:
            return False
        
    def feature_timedomain(self, window=None):
        pass
    
    def feature_freqdomain(self, window=None):
        pass
    
    def feature_nonlinear(self, window=None):
        pass