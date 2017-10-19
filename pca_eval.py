import numpy as np
from sklearn.decomposition import RandomizedPCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import csv
import matplotlib.pyplot as plt

#this code uses the PCA to reduce the data 
#kmeans library to cluster a dataset at several values of k 
#to be evaluated by the silheoutte analysis

def getData2(data):
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

data = np.array( getData2("shot_data.csv"))
n_components = 2

#pca = RandomizedPCA(n_components=n_components, whiten=True)
#default n_components=2 output didn't change much from 2 to 4
pca = RandomizedPCA(n_components=2) 
pca.fit(data)

print "Now printing the explained variance\n"
print(pca.explained_variance_)
print(pca.components_)
print len(pca.explained_variance_)

"""for x in pca.components_: 
 print x
"""

var = pca.explained_variance_





data2= pca.transform(data) 
print "pca fitted data"
print np.shape(data2)
 


fig = plt.figure() 
ax = fig.add_subplot(111)
ax.scatter(data2[:,0] , data2[:,1] )
plt.show()




