## 
## Elastic Net. Estimate preformance.
##

import pandas as pd
import numpy as np
import sklearn.linear_model as lm
import sklearn.cross_validation as cv
import sklearn.preprocessing as pp
import sklearn.metrics as metrics
import soilCleanTools as clean
import time
import StandardAxisScaler


##
## Read in and perform basic transformations of the data
##

# Read in data
train_df = pd.read_csv('./Data/training.csv', index_col='PIDN')

# Clean and split for readability
train_data_dict = clean.clean_data(train_df)
wave, spatial, targets = train_data_dict['wave'], train_data_dict['spatial'], train_data_dict['targets']


# Model and specifications 
model_name = 'ElNet'
l1_ratios = [.001, .05,.1,.3,.5,.7,.9,.95,.99,1]
n_alphas = 1000
eps=0.0001
alphas = np.logspace(-14,3,num=n_alphas,base=2)
elNet_obj = lm.ElasticNetCV(l1_ratio=l1_ratios, alphas=alphas, eps=eps, cv=5) #This will be argument into more general functino

# Enumerate the different preprocessing protocols for iteration below.
preprocesses = {'Identity':(StandardAxisScaler,{'with_mean':False, 'with_std':False}), #This will be other argument.
                'Column Scale':(StandardAxisScaler,{'with_mean':True, 'with_std':True, 'axis':0}),
                'Row Scale':(StandardAxisScaler,{'with_mean':False, 'with_std':True, 'axis':1})} #What should the row scaling be? 


# Streamline this and the prediction script
#Input: model_obj, preprocess


#Build DataFrame to record results #Abstractly: build record object
results_cols = pd.Index(targets.columns, name='Target')
results_idx = pd.Index(preprocesses.iterkeys(), name='Preprocess')
results = pd.DataFrame(index=results_idx, columns=results_cols)

##
(train_idx, val_idx) = cv.train_test_split(wave.index, train_size=.9)

#Iterate through the preprocesses, and fit the model to each transformed data.
for (scale_type, (scaler_obj, kwargs)) in preprocesses.iteritems():
    
    # Scale the (partial) data according to given protocol
    scaler = scaler_obj(kwargs)
    X_train = scaler.fit_transform(wave.loc[train_idx,:])
    X_val = scaler.transform(wave.loc[val_idx])

    # Fit model to the data (and perform CV to choose optimal meta-parameters) against each target variable, (perform prediction, perf. measurement) and record in recoding obj
    for (target_name, y) in targets.iteritems():

        elNet_obj.fit(X = X_train, y=y.loc[train_idx,:])
        y_pred = elNet_obj.predict(X=X_val)
        mse = metrics.mean_squared_error(y_pred=y_pred, y_true=y.loc[val_idx,:])
        results.loc[scale_type, target_name] = mse

    # Save predictions with this preprocessing protol to disk. #Abstractly, save record object to disk.
    path = './Data/Preds/results-'+model_name+'-'+time.strftime("%m-%d")+'.csv' #model-preprocess-date
    results.to_csv(path_or_buf= path)
    #model-preprocess-date








