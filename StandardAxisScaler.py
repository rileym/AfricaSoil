import sklearn.preprocessing as pp    
import numpy as np


class StandardAxisScaler(pp.StandardScaler):
    '''StandardScaler with ability to scale across rows instead. No inverse transform. X must be a pandas DataFrame.
    '''
    def __init__(self, copy=True, with_mean=True, with_std=True, axis=0):
        
        self.flip = (axis == 1)
        super(StandardAxisScaler, self).__init__(copy, with_mean, with_std)
        
    def fit(self, X, y=None):
        
        if self.flip:
            X = X.T
            
        return super(StandardAxisScaler, self).fit(X, y)
    
    
    def transform(self, X, y=None, copy=None):
        
        if self.flip:
            X = X.T
            
        X_trans = super(StandardAxisScaler, self).transform(X, y, copy)
        
        return np.transpose(X_trans) if self.flip else X_trans
