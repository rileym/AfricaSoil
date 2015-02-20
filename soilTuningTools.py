import pandas as pd
import numpy as np
import sklearn.grid_search as grid_search
import sklearn.cross_validation as cv
import sklearn.preprocessing as pp
import sklearn.metrics as metrics
import time
import timeit

def rmse(y_pred, y_true):
    return np.sqrt(metrics.mean_squared_error(y_pred, y_true))

def sumsq(y_pred, y_true):
    return np.sum((y_pred - y_true)**2)

def trans_then_rmse(y_pred, y_true, trans_func):
    return rmse(trans_func(y_pred), trans_func(y_true))

def trans_then_sumsq(y_pred, y_true, trans_func):
    return sumsq(trans_func(y_pred), trans_func(y_true))

def retrieve_cv_scores(grid_scores, target_dict):

    for cvTuple in grid_scores:
    
        if cvTuple[0] == target_dict:
            return cvTuple[2]



def soilTune(gs_obj, X, Y, X_test = None,  \
            tasks = ['evaluate'], p = .9, scaler_dict = None, y_trans_func = None, y_inv_trans = None,\
            model_name = None, output_base_path = './'):         #score = 'rmse')
    '''
    '''

    if scaler_dict is None:
        scaler_dict = {'Identity' : pp.StandardScaler(with_mean = False, with_std = False)} 

    if (y_trans_func is None) or (y_inv_trans is None):
        identity = lambda x : x
        y_trans_func = y_inv_trans = identity
    
    if 'evaluate' in tasks:
        
        return _evaluate(gs_obj, X, Y, p, scaler_dict, y_trans_func, y_inv_trans, model_name, output_base_path)

        
    if ('predict' in tasks) & (X_test is not None):
        
        return _predict(gs_obj, X, Y, X_test, scaler_dict, y_trans_func, y_inv_trans, model_name, output_base_path)
        
        
        
def _evaluate(gs_obj, X, Y, p, scaler_dict, y_trans_func, y_inv_trans, model_name, output_base_path):
    '''
    '''

    # Build DataFrame to record results
    
    results_columns = pd.MultiIndex.from_product([Y.columns,['RMSE MEAN','RMSE STD']], names = ['Target', 'Statistic'])
    results_index = pd.Index(list(scaler_dict), name='Feature Scaling')
    results = pd.DataFrame(index = results_index, columns=results_columns) 
    
    # Seperate out validation set.
    validate = p < 1
    if validate:
        (train_idx, val_idx) = cv.train_test_split(X.index, train_size = p)
    else :
        train_idx = X.index
    #Scorer Object
    
    print('Beginning Evaluation...')
    start_time = timeit.default_timer()
    
    for (scaler_name, scaler) in scaler_dict.iteritems():
        
        # X_scld = scaler.fit_transform(X.loc[train_idx,:]) 
        # X_val_scld = scaler.transform(X.loc[val_idx,:])
        print('\nScale type: ' + scaler_name + ':')

        # Fit model to the data (and perform CV to choose optimal meta-parameters) 
        for (target_name, y) in Y.iteritems() :

            y = y_trans_func(y)
            # Scale according to 'scaler'
            X_scld = scaler.fit_transform(X.loc[train_idx,:], y[train_idx])

            gs_obj.fit(X = X_scld, y = y.loc[train_idx])

            best_scores_array = retrieve_cv_scores(gs_obj.grid_scores_, gs_obj.best_params_)
            results.loc[scaler_name, (target_name, 'RMSE MEAN')] = np.sqrt(np.sum(best_scores_array**2)/len(best_scores_array))
            results.loc[scaler_name, (target_name, 'RMSE STD')] = best_scores_array.std()
            print_params(target_name, gs_obj.best_params_)
            print('Internal CV RMSE: ' + str((np.sqrt(np.sum(best_scores_array**2)/len(best_scores_array)))))
            print('Internal CV SDev:' + str(best_scores_array.std()))

            if validate:

                X_val_scld = scaler.transform(X.loc[val_idx,:])
                y_pred = gs_obj.predict(X = X_val_scld)
                val_rmse = rmse(y_pred=y_pred, y_true=y.loc[val_idx]) #generalize
                print('Validation RMSE: ' + str(val_rmse))

    # 
    # Capture elapsed time
    elapsed = timeit.default_timer() - start_time
    print('Time elapsed in main loop: ' + str(elapsed))
    nperms = len(scaler_dict)*len(grid_search.ParameterGrid(gs_obj.param_grid))
    print('On ' + str(nperms) + ' parameter/scaling permutations.')
    
    # Write to disk.
    path = output_base_path+model_name+'-results-'+time.strftime("%m-%d")+'.csv'
    results.to_csv(path_or_buf = path)
    return results


def _predict(gs_obj, X, Y, X_test, scaler_dict, model_name, output_base_path):
    '''
    '''

    #Build DataFrame to record results

    results_cols = pd.MultiIndex.from_product((list(scaler_dict), Y.columns), names=('Scaling','Target'))
    results = pd.DataFrame(index=X_test.index, columns=results_cols)
    
    print('\nBeginning Prediction...')
    start_time = timeit.default_timer()
    for (scaler_name, scaler) in scaler_dict.iteritems():
        
        # Scale according to 'scaler'
        # X_scld = scaler.fit_transform(X)
        # X_test_scld = scaler.transform(X_test)
        print('\nScale type: ' + scaler_name + ':')
        # Fit model to the data 
        for (target_name, y) in Y.iteritems():

            # Scale according to 'scaler'
            X_scld = scaler.fit_transform(X, y)
            X_val_scld = scaler.transform(X_test)

            gs_obj.fit(X = X_scld, y = y)
            y_pred = gs_obj.predict(X = X_test_scld)
            results[(scaler_name, target_name)] = y_pred

            print_params(target_name, gs_obj.best_params_)


    # Capture elapsed time

    elapsed = timeit.default_timer() - start_time
    print('Time elapsed in main loop: ' + str(elapsed))
    nperms = len(scaler_dict)*len(grid_search.ParameterGrid(gs_obj.param_grid))
    print('On ' + str(nperms) + ' parameter/scaling permutations.')

    # Write to disk.

    path = output_base_path+model_name+'-preds-'+time.strftime("%m-%d")+'.csv'
    results.to_csv(path_or_buf = path)
    return results

def print_params(target_name, param_dict):
    '''
    '''
    
    print('\n' + target_name + ':')
    for (parameter, value) in param_dict.iteritems():
        print(parameter.title()+': ' + str(value))






        