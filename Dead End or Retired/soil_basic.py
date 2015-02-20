## Ridge Regression
##


import pandas as pd
import numpy as np
import sklearn.linear_model as lm
import sklearn.cross_validation as cv


# Read in data
df = pd.read_csv('./Data/training.csv',index_col='PIDN')
# Drop carbon columns

carbon_cols = df.columns[(df.columns >= 'm2379.76') & (df.columns <= 'm2352.76')] #Drop the irrelvant columns.
df.drop(labels=carbon_cols, axis=1, inplace = True)

# 
wave_df = df.ix[:,'m7497.96':'m599.76']
spacial_df = df.ix[:,'BSAN':'Depth']
targets = df.ix[:,'Ca':'Sand']


# Split index into test and validation
(train_idx, val_idx) = cv.train_test_split(df.index, train_size=.9)


n_alphas = 1000
alphas = np.logspace(-14,2,n_alphas, base=2)
rr_obj = lm.RidgeCV(alphas=alphas, scoring='mean_squared_error')

results = {}
for (name, y) in targets.iteritems():

    rr_obj.fit(X=wave_df.ix[train_idx,:].values, y=y[train_idx].values)
    mse = metrics.mean_squared_error(y_pred=rr_obj.decision_function(wave_df.ix[val_idx,:].values), y_true=y[val_idx].values)
    results[name] = np.sqrt(mse)

print('###### Results ######\n')
for (name, rmse) in results.iteritems():
    print name, ':\t', str(rmse)

pd.Series(results)
print('\nMean: '+ str(pd.Series(results).mean()))

