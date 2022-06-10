import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#Read data & Split it
df = pd.read_csv("data/train.csv")
#print(pd.DataFrame(df).head(3)) #The first three data
#print(df.columns) #data Index
'''
data Index
['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered', 'count'],
      dtype='object')
'''
x_df = pd.DataFrame(df, columns = ['season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered'])
y_df = pd.DataFrame(df, columns = ['count'])
x_train, x_valid, y_train, y_valid = train_test_split(x_df, y_df, train_size=0.6, random_state=0)
x_valid, x_test, y_valid, y_test = train_test_split(x_valid, y_valid, train_size=0.5, random_state=0)
#print(x_train, x_valid, x_test, y_train, y_valid, y_test)

#Standardization
sc = StandardScaler()
sc.fit(x_train)
x_train_std = sc.transform(x_train)
x_valid_std = sc.transform(x_valid)
x_test_std = sc.transform(x_test)

import xgboost as xgb
from sklearn.model_selection import GridSearchCV
n_estimators = [10,20,30,40,50,60,70,80,90,100]
max_depth = [1,2,3,4,5,6]
parameters_to_search = {'n_estimators': n_estimators, 
              'max_depth': max_depth}
xgbrModel=xgb.XGBRegressor(n_estimators = 100, max_depth = 6)
gb_model_CV = GridSearchCV(xgbrModel, parameters_to_search, cv=5)
gb_model_CV.fit(x_train, y_train)
knn_test_score=gb_model_CV.score(x_test, y_test)
print('Correct rate using XGBoost: {:.5f}'.format(knn_test_score))