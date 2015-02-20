import pandas as pd



## 
## Define some useful functions.
##

# Drop a range of entries using their labels.
def drop_labeled_range(df, from_label, to_label, axis=0, inplace = True):
    '''
    '''
    to_drop = df.ix[:,from_label:to_label].columns
    return df.drop(labels=to_drop, axis=axis, inplace = inplace)

# General function for encoding categorical data
def code_categorical(df, columns, drop_old=False):
    '''
    ''' 

    columns = [columns] if isinstance(columns, basestring) else columns 

    coded_transforms = []
    for column in columns:
        coded = pd.get_dummies(df[column],prefix=column)
        coded.drop(labels=coded.columns[-1],axis=1, inplace=True) #Last column is redundant information
        coded_transforms.append(coded)

    if drop_old:
        df = df.drop(columns, axis=1)

    return df.join(coded_transforms)


def clean_data(df):
    ''' 
    Drops the carbon columns, encodes the 'Depth' feature,
    and splits the data into the wave data, the sptial data, and the targets (if they are present)
    '''
    #Drop carbon columns
    df = drop_labeled_range(df, from_label='m2379.76', to_label='m2352.76',axis=1, inplace=False) 
    wave = df.ix[:,'m7497.96':'m599.76']
    spatial = df.ix[:,'BSAN':'Depth']
    spatial = code_categorical(spatial, ['Depth'], drop_old = True)
    data_dict = {'wave':wave, 'spatial':spatial}

    if set(['Ca', 'P', 'pH', 'SOC', 'Sand']).issubset(df.columns):
        data_dict['targets'] = df.loc[:,'Ca':'Sand']

    return data_dict

        

