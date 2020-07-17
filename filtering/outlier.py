#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 09:59:52 2020

@author: chenyaru
"""

from sensorpowa.core.base import BaseSensorSeries
import numpy as np

class BaseOutlier(object):
   
    @property
    def _algorithm(self):
        """Specify kind str Must be overridden in child class"""
        raise NotImplementedError
        
    def __init__(self, data, **kwargs):
        self.data = data
        self.kwargs = kwargs
        self.outliersfilter = None
        
    # @property
    # def outliersfilter(self):
    #     # TODO rewrite
    #     """Specify scaling Must be overridden in child class"""
    #     return None 

    def fit(self):
        """Specify _plot function Must be overridden in child class"""
        raise NotImplementedError
        
    def transform(self):
        """Specify _plot function Must be overridden in child class"""
        raise NotImplementedError


       
class TransformerMixin(object):
    """Mixin class for all transformers in DropOutliers Methods"""
    
    def fit_transform(self, X, y=None, **fit_params):
        """Fit to data, then transform it.

        Fits transformer to X and y with optional parameters fit_params
        and returns a transformed version of X.

        Parameters
        ----------
        X : numpy array of shape [n_samples, n_features]
            Training set.

        y : numpy array of shape [n_samples]
            Target values.

        Returns
        -------
        X_new : numpy array of shape [n_samples, n_features_new]
            Transformed array.

        """
        if y is None:
            # fit method of arity 1 (unsupervised transformation)
            return self.fit(X, **fit_params).transform(X)
        else:
            # fit method of arity 2 (supervised transformation)
            return self.fit(X, y, **fit_params).transform(X)

        
class OutliersCI(BaseOutlier, TransformerMixin):
    ## TODO: Modifier notation
    """Scale features using statistics that are robust to outliers.

    This Scaler removes the median and scales the data according to
    the quantile range (defaults to IQR: Interquartile Range).
    The IQR is the range between the 1st quartile (25th quantile)
    and the 3rd quartile (75th quantile).

    Centering and scaling happen independently on each feature (or each
    sample, depending on the ``axis`` argument) by computing the relevant
    statistics on the samples in the training set. Median and  interquartile
    range are then stored to be used on later data using the ``transform``
    method.

    Standardization of a dataset is a common requirement for many
    machine learning estimators. Typically this is done by removing the mean
    and scaling to unit variance. However, outliers can often influence the
    sample mean / variance in a negative way. In such cases, the median and
    the interquartile range often give better results.

    .. versionadded:: 0.17

    Read more in the :ref:`User Guide <preprocessing_scaler>`.

    Parameters
    ----------
    with_centering : boolean, True by default
        If True, center the data before scaling.
        This will cause ``transform`` to raise an exception when attempted on
        sparse matrices, because centering them entails building a dense
        matrix which in common use cases is likely to be too large to fit in
        memory.

    with_scaling : boolean, True by default
        If True, scale the data to interquartile range.

    quantile_range : tuple (q_min, q_max), 0.0 < q_min < q_max < 100.0
        Default: (25.0, 75.0) = (1st quantile, 3rd quantile) = IQR
        Quantile range used to calculate ``scale_``.

        .. versionadded:: 0.18

    copy : boolean, optional, default is True
        If False, try to avoid a copy and do inplace scaling instead.
        This is not guaranteed to always work inplace; e.g. if the data is
        not a NumPy array or scipy.sparse CSR matrix, a copy may still be
        returned.

    Attributes
    ----------
    center_ : array of floats
        The median value for each feature in the training set.

    scale_ : array of floats
        The (scaled) interquartile range for each feature in the training set.

        .. versionadded:: 0.17
           *scale_* attribute.

    See also
    --------
    robust_scale: Equivalent function without the estimator API.

    :class:`sklearn.decomposition.PCA`
        Further removes the linear correlation across features with
        'whiten=True'.

    Notes
    -----
    For a comparison of the different scalers, transformers, and normalizers,
    see :ref:`examples/preprocessing/plot_all_scaling.py
    <sphx_glr_auto_examples_preprocessing_plot_all_scaling.py>`.

    https://en.wikipedia.org/wiki/Median_(statistics)
    https://en.wikipedia.org/wiki/Interquartile_range
    """  
    
    _algorithm = 'ci'
    
    def __init__(self, quantile_range=(5,95)):
        self.quantile_range = quantile_range

        
    def fit(self, X):
        min_outlier, max_outlier = np.percentile(X, self.quantile_range)
        self.outliersfilter = [min_outlier, max_outlier]
        return self
    
    def transform(self, X, keepdims=True,reset_index=True):
        min_outlier = self.outliersfilter[0]
        max_outlier = self.outliersfilter[1]
        index_min = X[X<=min_outlier].index
        index_max = X[X>=max_outlier].index
        for index in [index_min,index_max]:
            X[index] = None
        if not keepdims:
            X = X.dropna()
        if reset_index:
            X = X.reset_index(drop=True)
        return X

        
class OutliersQ(BaseOutlier, TransformerMixin):
    ## TODO: Modifier notation
    """Scale features using statistics that are robust to outliers.

    This Scaler removes the median and scales the data according to
    the quantile range (defaults to IQR: Interquartile Range).
    The IQR is the range between the 1st quartile (25th quantile)
    and the 3rd quartile (75th quantile).

    Centering and scaling happen independently on each feature (or each
    sample, depending on the ``axis`` argument) by computing the relevant
    statistics on the samples in the training set. Median and  interquartile
    range are then stored to be used on later data using the ``transform``
    method.

    Standardization of a dataset is a common requirement for many
    machine learning estimators. Typically this is done by removing the mean
    and scaling to unit variance. However, outliers can often influence the
    sample mean / variance in a negative way. In such cases, the median and
    the interquartile range often give better results.

    .. versionadded:: 0.17

    Read more in the :ref:`User Guide <preprocessing_scaler>`.

    Parameters
    ----------
    with_centering : boolean, True by default
        If True, center the data before scaling.
        This will cause ``transform`` to raise an exception when attempted on
        sparse matrices, because centering them entails building a dense
        matrix which in common use cases is likely to be too large to fit in
        memory.

    with_scaling : boolean, True by default
        If True, scale the data to interquartile range.

    quantile_range : tuple (q_min, q_max), 0.0 < q_min < q_max < 100.0
        Default: (25.0, 75.0) = (1st quantile, 3rd quantile) = IQR
        Quantile range used to calculate ``scale_``.

        .. versionadded:: 0.18

    copy : boolean, optional, default is True
        If False, try to avoid a copy and do inplace scaling instead.
        This is not guaranteed to always work inplace; e.g. if the data is
        not a NumPy array or scipy.sparse CSR matrix, a copy may still be
        returned.

    Attributes
    ----------
    center_ : array of floats
        The median value for each feature in the training set.

    scale_ : array of floats
        The (scaled) interquartile range for each feature in the training set.

        .. versionadded:: 0.17
           *scale_* attribute.

    See also
    --------
    robust_scale: Equivalent function without the estimator API.

    :class:`sklearn.decomposition.PCA`
        Further removes the linear correlation across features with
        'whiten=True'.

    Notes
    -----
    For a comparison of the different scalers, transformers, and normalizers,
    see :ref:`examples/preprocessing/plot_all_scaling.py
    <sphx_glr_auto_examples_preprocessing_plot_all_scaling.py>`.

    https://en.wikipedia.org/wiki/Median_(statistics)
    https://en.wikipedia.org/wiki/Interquartile_range
    """ 
    
    _algorithm = 'quan'
    
    def __init__(self, quantile_range=(25,75), keepdims=True,reset_index=True):
        self.quantile_range = quantile_range
        self.keepdims = True
        self.reset_index = True
        
    def fit(self, X):
        min_quantile, max_quantile = np.percentile(X, self.quantile_range)
        iqr = max_quantile - min_quantile
        iqr_outlier = 1.5 * iqr
        min_outlier = min_quantile - iqr_outlier
        max_outlier = max_quantile + iqr_outlier
        self.outliersfilter = [min_outlier, max_outlier]
        return self
    
    def transform(self, X, keepdims=True, reset_index=True):
        min_outlier = self.outliersfilter[0]
        max_outlier = self.outliersfilter[1]
        index_min = X[X<=min_outlier].index
        index_max = X[X>=max_outlier].index
        for index in [index_min,index_max]:
            X[index] = None
        if not keepdims:
            X = X.dropna()
        if reset_index:
            X = X.reset_index(drop=True)
        return X

_klasses = [OutliersCI, OutliersQ]
outliers_klass = {klass._algorithm: klass for klass in _klasses}

# def _outlierfit(data, algorithm, **kwargs):
#     klass = outliers_klass[algorithm]
#     fit_obj = klass(data, **kwargs)
#     return fit_obj.fit(data)

# def _outlierfilter(data, algorithm, **kwargs):
#     klass = outliers_klass[algorithm]
#     fit_obj = klass(data, **kwargs)
#     return fit_obj.fit_transform(data)
    
    
class SensorSeriesOutlier(BaseOutlier, TransformerMixin):
    
    def __init__(self, data, model=None, **kwargs):
        self.data = data
        self.kwargs = kwargs
        if isinstance(model, BaseOutlier):
            self.outliersmodel = model
        elif isinstance(model, str):
            outliersklass = outliers_klass[model]
            self.outliersmodel = outliersklass(**self.kwargs).fit(self.data)
            
    def transform(self, **kwargs):
        return self.outliersmodel.transform(self.data, **kwargs)
        
    
    
    
    
    
    
    