import pandas as pd
import numpy as np
import sklearn.base as base


class CorrelationGrouper(base.BaseEstimator, base.TransformerMixin):
    '''
    '''

    def __init__(self, alpha = .95):
        
        self.alpha = alpha
    

    def fit(self, X, y):
        '''
        X must be a DataFrame with shape (n_samples, n_features).
        y must be an array, Series, or DataFrame of length n_samples.
        '''
        
        (___, _grouping_key) = self._autocorr_grouping(X, y)
        self._grouping_key = _grouping_key
        self._n_groups = len(_grouping_key.unique())
        return self
    

    def fit_transform(self, X, y):
        
        self.fit(X, y)
        return self.transform(X, y)
       

    def transform(self, X, y = None):
        
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        if hasattr(self, '_grouping_key'):
            
            return X.groupby(by = self._grouping_key, axis = 1).mean()
               
        else:
            
            raise AttributeError('No \'_grouping_key\' attribute. \'fit(_tranfrom)\' must be called before \'transform\'.')
    

    def get_keys(self):

        if hasattr(self, '_grouping_key'):
            
            return self._grouping_key.copy()
               
        else:
            
            raise AttributeError('No \'_grouping_key\' attribute. \'fit(_tranfrom)\' must be called.')

    def get_num_groups(self):

        if hasattr(self, '_n_groups'):
            
            return self._n_groups
               
        else:
            
            raise AttributeError('No \'_n_groups\' attribute. \'fit(_tranfrom)\' must be called.')


    
    def _autocorr_grouping(self, df, target):
        
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)
        n = df.shape[1]
        sorted_corrs = np.abs(df.corrwith(target)).reset_index(drop = True).sort(inplace = False, ascending = False)
        mapping = {}

        for (idx, corr) in sorted_corrs.iteritems():

            if idx not in mapping:

                mapping[idx] = idx
                autocorr  = df.corrwith(df.iloc[:,idx])
                for i in xrange(idx+1, n):
                    if autocorr[i] < self.alpha:
                        break
                    mapping[i] = idx

                for i in xrange(idx-1, -1, -1):
                    if autocorr[i] < self.alpha:
                        break
                    mapping[i] = idx

        #A little awkward becuase I couldn't find a one-step way to convert the integer index to the label index
        lab_idx = 'Wave Numbers' 
        df_mapping = pd.DataFrame(pd.Series(mapping))
        df_mapping[lab_idx] = df.columns
        series_mapping = df_mapping.set_index(lab_idx, drop = True).squeeze()

        return (mapping, series_mapping)

    
