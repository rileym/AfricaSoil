## 
## Elastic Net. Predict Test Set
##

import pandas as pd
import numpy as np
import sklearn.linear_model as lm
import sklearn.cross_validation as cv
import sklearn.preprocessing as pp
import soilCleanTools as clean
import time
import StandardAxisScaler


##
## Read in and perform basic transformations of the data
##

# Read in data
train_df = pd.read_csv('./Data/training.csv', index_col='PIDN')
test_df = pd.read_csv('./Data/sorted_test.csv', index_col='PIDN')

# Clean and split for readability
train_data_dict = clean.clean_data(train_df)
test_data_dict = clean.clean_data(test_df)
wave, spatial, targets = train_data_dict['wave'], train_data_dict['spatial'], train_data_dict['targets']
wave_test, spatial_test, targets_test = test_Data_dict['wave'], test_Data_dict['spatial'], test_Data_dict['targets']


# Model and specifications
model_name = 'ElNet'
l1_ratios = [.001, .05,.1,.3,.5,.7,.9,.95,.99,1]
n_alphas = 1000
eps=0.0001
alphas = np.logspace(-14,3,num=n_alphas,base=2)
elNet_obj = lm.ElasticNetCV(l1_ratio=l1_rations, alphas=alphas, eps=eps, cv=5)

# Enumerate the different preprocessing protocols for iteration below.
preprocesses = {'Identity':(StandardAxisScaler,{'with_mean':False, 'with_std':False}),
                'Column Scale':(StandardAxisScaler,{'with_mean':True, 'with_std':True, 'axis':0})
                'Row Scale':(StandardAxisScaler,{'with_mean':True, 'with_std':True, 'axis':1})} #What should the row scaling be? 



#Build DataFrame to record predictions
preds_cols = pd.MultiIndex.from_product(iterables=[preprocesses.iterkeys(),targets.columns], names=('Preprocess', 'Target'))
preds = pd.DataFrame(index=test_df.index, columns=preds_cols)

#Iterate through the preprocesses, and fit the model to each transformed data.
for (scale_type, (scaler_obj, kwargs)) in preprocesses.iteritems():
    
    # Scale the data according to given protocol.
    scaler = scaler_obj(kwargs)
    X_train = scaler.fit_transform(wave)

    # Fit model to the data (and perform CV to choose optimal meta-parameters) against each target variable and predict the test set.
    for (target_name, y) in targets.iteritems():

        elNet_obj.fit(X = X_train, y=y)
        X_test = scaler.transform(wave_test)
        preds[(scale_type, target_name)] = elNet_obj.predict(X=X_test)

    # Save predictions with this preprocessing protol to disk.
    path = './Data/Preds/'+model_name+'-'+scale_type.replace(" ", "")+'-'+time.strftime("%m-%d")+'.csv' #model-preprocess-date
    preds[scale_type].to_csv(path_or_buf= path)
    #model-preprocess-date








