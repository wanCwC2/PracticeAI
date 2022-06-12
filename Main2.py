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
X_df = pd.DataFrame(df, columns = ['season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered'])
y_df = pd.DataFrame(df, columns = ['count'])
X_train, X_valid, y_train, y_valid = train_test_split(X_df, y_df, train_size=0.6, random_state=0)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid, y_valid, train_size=0.5, random_state=0)
#print(X_train, X_valid, X_test, y_train, y_valid, y_test)

#Standardization
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_valid_std = sc.transform(X_valid)
X_test_std = sc.transform(X_test)

#XGBoost
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
n_estimators = [10,20,30,40,50,60,70,80,90,100]
max_depth = [1,2,3,4,5,6]
parameters_to_search = {'n_estimators': n_estimators, 
              'max_depth': max_depth} #設定要訓練的值
xgbrModel=xgb.XGBRegressor(n_estimators = 100, max_depth = 6)
gb_model_CV = GridSearchCV(xgbrModel, parameters_to_search, cv=5) #可以直接找出最佳的訓練值
gb_model_CV.fit(X_train, y_train)
knn_test_score=gb_model_CV.score(X_test, y_test)
print('Correct rate using XGBoost: {:.5f}'.format(knn_test_score))

#Use MSE sure whether it has overfitting.
from sklearn import metrics
train_pred = gb_model_CV.predict(X_train)
mse = metrics.mean_squared_error(y_train, train_pred)
print('train data MSE: ', mse)
valid_pred = gb_model_CV.predict(X_valid)
mse = metrics.mean_squared_error(y_valid, valid_pred)
print('valid data MSE: ', mse)


#SVR
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
import numpy as np
maxRate = 0 #驗證及訓練結果的最高正確率
cRate = 2 #最適合用在此的SVR參數
epsilonRate = 0.5 #最適合用在此的SVR參數
rng = np.random.RandomState(0)
regr = make_pipeline(StandardScaler(), SVR(C=cRate, epsilon=epsilonRate))
regr.fit(X_train_std, y_train.values.ravel())
for i in range(1, 5):
    for j in range(0, 5):
        regr = make_pipeline(StandardScaler(), SVR(C=i, epsilon = j/10))
        regr.fit(X_train_std, y_train.values.ravel())
        if maxRate < regr.score(X_valid_std, y_valid.values.ravel()):
            maxRate = regr.score(X_valid_std, y_valid.values.ravel())
            indexRate = i
            epsilonRate = j/10
regr = make_pipeline(StandardScaler(), SVR(C = cRate, epsilon = epsilonRate))
regr.fit(X_train_std, y_train.values.ravel())
svr_test_score = regr.score(X_test_std,y_test.values.ravel())
print('Correct rate using SVR: {:.5f}'.format(svr_test_score))

# Random Forest
from sklearn.ensemble import RandomForestRegressor
maxRate = 0
indexRate = 0
for i in range (1,10):
    rfc = RandomForestRegressor(random_state = i)
    rfc.fit(X_train, y_train.values.ravel())
    if maxRate < rfc.score(X_valid, y_valid.values.ravel()):
        maxRate = rfc.score(X_valid, y_valid.values.ravel())
        indexRate = i
RandomForestRegressor(random_state = indexRate)
print("Correct rate using Random Forest: ", round(rfc.score(X_test, y_test.values.ravel()),5))
