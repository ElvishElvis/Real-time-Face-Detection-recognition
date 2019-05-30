import pandas as pd
from sklearn.linear_model import LogisticRegression


def output(row):
    row = pd.DataFrame(row).T.astype(int)
    train = pd.read_csv('emotions.csv', engine = 'python', error_bad_lines = False,
    warn_bad_lines = False, header = None)
    train = train[train[136].isna()==False]
    diction = {'neutral':0, 'surprise':1, 'disgust':2, 'anger':3, 'happy':4}
    train[136]=train[136].replace(diction)
    train = train.apply(lambda x: x.astype(int),axis=1)
    x = train[[i for i in range(136) if i%2 == 0]]
    y = train[[i for i in range(137) if i%2 == 1]]
    x_row = row[[i for i in range(136) if i % 2 == 0]]
    y_row = row[[i for i in range(136) if i % 2 == 1]]
    x = x.subtract(x.apply(lambda i: min(i),axis=1),axis=0)
    y = y.subtract(y.apply(lambda i: min(i),axis=1),axis=0)
    x_row = x_row.subtract(x_row.apply(lambda i: min(i), axis=1), axis=0)
    y_row = y_row.subtract(y_row.apply(lambda i: min(i), axis=1), axis=0)
    train = pd.concat([x,y,train[136]],axis=1).T.sort_index().T
    row = pd.concat([x_row, y_row], axis=1).T.sort_index().T
    train = train.apply(lambda x: x.apply(lambda y: int(y)),axis=1)
    X_train = train.drop(136,axis=1)
    y_train = train[136]
    mult = LogisticRegression()
    mult.fit(X_train,y_train)
    back = {0:'neutral', 1:'surprise', 2:'disgust', 3:'anger', 4:'happy'}
    return pd.DataFrame(mult.predict(row)).replace(back).loc[0][0]