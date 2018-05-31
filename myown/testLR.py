# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 14:44:25 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 08:42:39 2017

@author: John
"""

import ann
import logRegres as LR
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import StratifiedKFold
from imblearn.over_sampling import RandomOverSampler

import  pandas as  pd#python data analysis
import  matplotlib.pyplot as plt

#####加载全部78个特征值
import  global_list as gl
# dataset=gl.dataSet
# dataset=np.array(dataset)
# dataMat=dataset[:,0:62]
# labelMat=dataset[:,62]

###################遗传算法降维后的特征值#################
# dataset=pd.read_csv("LR10.csv")
# dataset=dataset.fillna(np.mean(dataset))
# dataset=np.array(dataset)
# dataMat=dataset[:, 0:10]
# dataMat=ann.preprocess(dataMat)
# dataMat=ann.preprocess1(dataMat)
# labelMat=dataset[:,10]

# ######加载遗传算法降维后的31个特征值，归一化之后的
# dataset=pd.read_csv("GA31.csv")
# dataset=np.array(dataset)
# dataMat=dataset[:, 0:31]
# labelMat=dataset[:,31]

# # ######MIV将为后的30个特征值（MIV降维后的时eigen_MIV，34个），归一化之后的
# dataset=pd.read_csv("MIV30.csv")
# dataset=np.array(dataset)
# dataMat=dataset[:, 0:30]
# labelMat=dataset[:,30]

# for i in range(len(labelMat)):
#     if labelMat[i] == -1:
#         labelMat[i] = 0;  # adaboost只能区分-1和1的标签

data=pd.read_csv('sortedFeature.csv')
labelMat=data['classlabel']
dataMat=data.ix[:,0:67]


evaluate_train = []
evaluate_test = []
prenum_train = []
prenum_test  = []


# num_sample=np.shape(dataMat1)[0]
data01=ann.preprocess(dataMat)
dataMat1=ann.preprocess1(data01)

addones=np.ones((1293,1))
dataMat=np.c_[addones,dataMat1]

#dataMat=dataMat1[:,0:78]
#dataMat=dataMat[:,0:44]

#==============================================================================
# for i in range(len(labelMat)):
#     if labelMat[i]==2:
#         labelMat[i]=0;#adaboost只能区分-1和1的标签
#==============================================================================

evaluate_train=[]
evaluate_test=[]
prenum_train=[]
prenum_test=[]

skf=StratifiedKFold(n_splits=10)
for train,test in skf.split(dataMat,labelMat):
#==============================================================================
# skf=StratifiedShuffleSplit(n_splits=10)
# for train,test in skf.split(dataMat,labelMat):
#==============================================================================
    print("%s %s" % (train,test))
    train_in=dataMat[train]
    test_in=dataMat[test]
    train_out=labelMat[train]
    test_out=labelMat[test]
    train_in, train_out = RandomOverSampler().fit_sample(train_in, train_out)
    trainWeights=LR.stocGradAscent1(train_in,train_out,500)
    
    len_train=np.shape(train_in)[0]
    len_test=np.shape(test_in)[0]
    test_predict=[]
    proba_test=[]
    for i in range(len_test):
        test_predict_tmp=LR.classifyVector(test_in[i,:], trainWeights)
        test_predict.append(test_predict_tmp)
        proba_test_tmp=LR.classifyProb(test_in[i,:], trainWeights)
        proba_test.append(proba_test_tmp)
     
        
    train_predict=[]
    proba_train=[]
    for i in range(len_train):
        train_predict_tmp=LR.classifyVector(train_in[i,:], trainWeights)
        train_predict.append(train_predict_tmp)
        proba_train_tmp=LR.classifyProb(train_in[i,:], trainWeights)
        proba_train.append(proba_train_tmp)
  
    test1,test2=ann.evaluatemodel(train_out,train_predict,proba_train)#test model with trainset
    evaluate_train.extend(test1)
    prenum_train.extend(test2)
    
    test3,test4=ann.evaluatemodel(test_out,test_predict,proba_test)#test model with testset
    evaluate_test.extend(test3)
    prenum_test.extend(test4)

Result_test=pd.DataFrame(evaluate_test,columns=['TPR','SPC','PPV','NPV','ACC','AUC','BER'])
Result_test.to_csv('BER/BER_LR.csv')
Result_test.boxplot()
plt.show()

mean_train=np.mean(evaluate_train,axis=0)
std_train=np.std(evaluate_train,axis=0)
evaluate_train.append(mean_train)
evaluate_train.append(std_train)

mean_test=np.mean(evaluate_test,axis=0)
std_test=np.std(evaluate_test,axis=0)
evaluate_test.append(mean_test)
evaluate_test.append(std_test)
    
evaluate_train=np.array(evaluate_train)
evaluate_test=np.array(evaluate_test)
prenum_train=np.array(prenum_train)
prenum_test=np.array(prenum_test)

evaluate_train_mean=np.mean(evaluate_test,axis=0)


print(evaluate_test)