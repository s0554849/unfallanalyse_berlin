import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN

X = pd.read_csv(r"01_Source/apriori_data_final_extended.csv", sep = ";")
X = X.drop(['ID'], axis=1)

# redundant columns
redunt_cols = ['Dezember', 'Januar', 'Februar','März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
       'November', '0 Uhr', '1 Uhr', '2 Uhr', '3 Uhr', '4 Uhr',
       '5 Uhr', '6 Uhr', '7 Uhr', '8 Uhr', '9 Uhr', '10 Uhr',
       '11 Uhr',  '12 Uhr', '13 Uhr', '14 Uhr', '15 Uhr',
       '16 Uhr', '17 Uhr', '18 Uhr', '19 Uhr', '20 Uhr', '21 Uhr', '22 Uhr',
       '23 Uhr', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag',
       'Freitag', 'Samstag', 'Sonntag']

X = X.drop(redunt_cols, axis = 1)
model = DBSCAN(eps=1, min_samples=100, n_jobs=-1)
       #X = X.drop(['CLUSTER'], axis = 1)
clusters = model.fit_predict(X)
#X = load_iris().data
X['CLUSTER'] = clusters
X['CLUSTER'] = X['CLUSTER'].astype('category')
Y= pd.get_dummies(X)
# setting distance_threshold=0 ensures we compute the full tree.
#eps=3.5, n_jobs=-1) #AgglomerativeClustering(distance_threshold=0, n_clusters=None)

print(len(np.unique(clusters)))

len(X.columns)
plt.plot(clusters)
plt.show()
#Y.to_csv("01_Source/apriori_geclustert.csv")

Y[Y['CLUSTER_2']==1].head()