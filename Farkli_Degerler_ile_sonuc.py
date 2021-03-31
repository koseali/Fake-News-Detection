# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 11:39:26 2021

@author: kosea
"""
""" Farklı etiketleme ile ilgili sonuclar degerlendirmek icin kullanılır."""
import pandas as pd

manuel_etiket = pd.read_csv('tweet_etiketlenmis.csv')
tahmin_etiket = pd.read_csv('tahmin_degerleri.csv')

y_test = manuel_etiket[['dogruluk']]

y_predict = tahmin_etiket[['tahmin']]


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