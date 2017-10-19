#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
#sys.path.append("../tools/")
#from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
#features_train, features_test, labels_train, labels_test = preprocess()



#########################################################
### your code goes here ###

#########################################################

from sklearn import svm
import numpy as np
import csv

def getDataFeatures(data):
  ifile= open(data, 'rb') 
  dataSet = []
  a= b= 0
  for row in csv.reader(ifile, delimiter=','):
    dataSet.append([])
    b= 0
    #print len(row)
    #print (row)
    rowlen = len(row) - 1
    for col in range(0, 3):
      if( col != 0): 
        dataSet[a].append(float(row[col]))
      else: 
        dataSet[a].append( float(row[col]) )
    a+=1
   
  return dataSet

def getDataLabels(data):
  ifile= open(data, 'rb') 
  dataSet = []
  a= b= 0
  for row in csv.reader(ifile, delimiter=','):
    dataSet.append(float(row[3]))
 
  return dataSet


features_train = getDataFeatures("shot_data.csv")

labels_train = getDataLabels("shot_data.csv")

features_test =  getDataFeatures("testing.csv")
labels_test = getDataLabels("testing.csv")

clf = svm.SVC(kernel = 'sigmoid')
clf.fit(features_train, labels_train)



pred = clf.predict(features_test)

sum1 = 0.0 
tp =fp = fn =tn = 0

for x in range(0, len(pred) ):
  if pred[x] == labels_test[x]:
    sum1 = sum1 + 1 
    print "predict = " + str(pred[x]) + ", actual = " + str(labels_test[x])
  if pred[x] == 1 and labels_test[x] ==1:
    tp = tp + 1
  elif pred[x] == 0 and labels_test[x] == 1:
    fn = fn + 1
  elif pred[x] == 0 and labels_test[x] == 0: 
    tn = tn +1
  elif pred[x] == 1 and labels_test[x] == 0: 
    fp = fp +1
accuracy = 0.0
accuracy = sum1/ len(pred)

cm= [ [tp, fp], [tn, fn] ]

print cm

print "Num of testing cases " + str(len(pred))
print accuracy

