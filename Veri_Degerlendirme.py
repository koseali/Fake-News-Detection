# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 01:36:20 2021

@author: kosea
"""
"""VERİLERİN DEGERLENDİRİLMESİ"""
import pandas as pd 

data = pd.read_csv('Son_veri_ve_Sonuc.csv')

y_test = data[['dogruluk']]
y_predict = data[['tahmin']]
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_predict,y_test)
print(cm)

from sklearn.metrics import classification_report

class_report = classification_report(y_predict,y_test)

print(class_report)

import sklearn.metrics as mtc

fpr,tpr,threshold = mtc.roc_curve(y_predict, y_test)
roc_auc = mtc.auc(fpr, tpr)

from sklearn.metrics import accuracy_score
score = accuracy_score(y_test, y_predict)
print("accuracy:   %0.3f" % (score*100))


import matplotlib.pyplot as plt
plt.title('ROC Egrisi')
plt.plot(fpr, tpr,'b',label = 'AUC = %0.2f' % roc_auc)
plt.plot([0,1],[0,1], 'r--')
plt.xlim([0,1])
plt.ylim([0,1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()