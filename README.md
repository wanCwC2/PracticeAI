可能會有中英交雜的情況，我覺得用英文打比較方便，但為了求快時就會用中文了。 <br>
`Main.py`是訓練KNN, Decision Tree, Random Forest: `Main2.py`是訓練XGBoost, Random Forest, SVR <br>
`Stacking.py`是調整三個模型合併之後，要使用驗證集調整參數。因為如果執行程式確認是否有bug，要重新跑過前面三個模型速度太慢了，所以才挪出一些程式碼，方便寫用驗證集調整參數的程式。 <br>
`Main2.py` 輸出結果：（因為這要跑一段時間，所以放上2022-06-13最後一次執行的狀況）
<img src="./image/main2Output.png" style="zoom:70%" />
<br>

# Data source
[Bike Sharing Demand - Kaggle](https://www.kaggle.com/competitions/bike-sharing-demand/overview) <br>
Downing the *.csv, and put them in data folder.

# KNN
`numpy.mean`: Must use `np.array`. Cause `array` not work to judge True or False. <br>
I used two method: `GridSearchCV` and `numpy.mean` to find k. GridSearchCV was successful, but numpy.mean wasn't.
Then, I though why not use `knn.score` to find the best corret rate.
Ha! Finally, two method found the same k. <br>
I found that the Method 1 only using train data, not using validation data. So, using Method 2 will be better. But, these two are almost same. <br>
在KNN中，我想要用物件導向。但是一直跳出`unhashable type: 'numpy.ndarray'`的錯誤，可以參考 [Python初學者之TypeError: unhashable type: 'list'問題分析](https://www.796t.com/content/1548405036.html)
大意上就是list或array不存在hash，無法用hash做為索引，必須要用`tuple()`，才有可能做物件導向。需要再研究吧，目前先用`Main.py`將就一下。
## 找到最佳k值
<img src="./image/findK.png" style="zoom:70%" />
<br>

### References
[機器學習 第5篇：knn迴歸 - iT人](https://iter01.com/549663.html) <br>
[Python機器學習筆記(五)：使用Scikit-Learn進行K-Nearest演算法](https://yanwei-liu.medium.com/python機器學習筆記-五-使用scikit-learn進行k-nearest演算法-1191ea94ecaf) <br>
[調參——得到更好的 kNN 模型](https://www.gushiciku.cn/pl/2DZ0/zh-tw)

# Decision Tree
我沒想到連這個Decision tree居然特別設置針對回歸分析的，不得不說sklearn模組做得真的很好。 <br>
### References
[資料視覺化之 Decision tree (決策樹)範例與 Machine Learning (機器學習) 概念簡單教學(入門)](https://tree.rocks/decision-tree-graphviz-contour-with-pandas-gen-train-test-dataset-for-beginner-9137b7c8416a) <br>

# Random Forest
### References
[[Python實作] 隨機森林模型 Random Forest](https://pyecontech.com/2019/11/03/python_random_forest/) <br>

# XGBoost
雖然這訓練出來的結果高達99%的正確率，但從訓練集和驗證集的MSE分別是3,15，看出有明顯overfitting的狀況。因此需要透過一些方式將弱訓練器集合成一個，可以讓訓練結果更為準確。這裡會使用Stacking。 <br>
### References
[[Day 15] 機器學習常勝軍-XGBoost -iT人](https://ithelp.ithome.com.tw/articles/10273094) <br>
[Using XGBoost with Scikit-learn -kaggle](https://www.kaggle.com/code/stuarthallows/using-xgboost-with-scikit-learn/notebook) <br>
[Scikit-Learn API -XGBoost](https://xgboost.readthedocs.io/en/stable/python/python_api.html#module-xgboost.sklearn) <br>
[[Day 16] 每個模型我全都要 - 堆疊法 (Stacking) -iT人](https://ithelp.ithome.com.tw/m/articles/10274009) <br>

# SVR
在調整SVR參數時，因為是搭配pipeline使用，沒辦法單獨寫 `SVR(調整參數)`，必須要再度使用pipeline且重新fit資料集。 <br>
### References
[SVR Scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html) <br>

# Note
## 2022-06-13
為了測驗最好的stacking，所以跑了約十小時的程式。雖然過程中有覺得應該要放棄，因為設定的值差異不大，而且有些warning，
但覺得都執行這麼久了，堅持下去直到結果⋯⋯於是在最關鍵的一刻，我後面要補上fit的程式，最關鍵的MSE沒測到。
但有記錄到最好的max_iter為90，random_state為20。(可是這不是重點啊！！！)
但我突然想到，正確率沒問題啊！重點是在MSE的結果有顯示出overfitting，我應該要不斷驗證，找出沒有overfitting不大的參數才對。我到底等這麼久是為了什麼啊⋯⋯ <br>
順便提一下，max_iter不能低於200，會有warning。 <br>
接著我重新驗證最佳參數，透過MSE來調整，看到結果後腦袋閃過目前最熱門的句子⋯⋯I'm try. I'm try. qwq <br>
<img src="./image/findStackParameter.png" style="zoom:70%" />
<br>
