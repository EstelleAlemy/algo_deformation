#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:22:01 2019

@author: estelle
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
#Algorithme de procrust


#Fonction

# Matrice de rotation
def M_rotate(teta):
    R=np.array([[np.cos(teta), -np.sin(teta)],
                [np.sin(teta), np.cos(teta)]])
    return(R)
 
    
def mypca(X):
    mean_vect=np.mean(X, axis=0)
    C=(X-mean_vect)
    cov=C.T@C
    val,vect=LA.eig(cov)
    V=-np.sort(-vect)  
    
    P=V.T@C.T
    
    return(P,V,C)
    
    



#%%
# Génération des matrices de point 2D
x=np.random.randint(101, size=(200,2))

#Orientation des données de 45° et -45°
R1=M_rotate(45)
R2=M_rotate(-45)

X1=x@R1
X2=x@R2

plt.figure()
plt.scatter(X1[:,0], X1[:,1], c='b', marker='x')
plt.scatter(X2[:,0], X2[:,1], c='r', marker='v')
plt.show()





#%%
# sur Application de la PCA X1
P1,V1,C1=mypca(X1)
plt.figure()
plt.scatter(P1[0,:],P1[1,:])
plt.title('PCA sur X1')
#%%%
# verification de ma fct PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X1proj=pca.fit_transform(X1)

plt.figure()
plt.scatter(X1proj[:,0],X1proj[:,1])

# On obtient pas exactement les mêmes valeurs que avec la mypca

#%%
# Application de la PCA X2
P2,V2,C2=mypca(X2)
plt.figure()
plt.scatter(P2[0,:],P2[1,:])
plt.title('PCA sur x2')
#%% Transformation de X2 vers X1
newP=V1.T@C2.T

plt.figure()
plt.scatter(newP[0,:],newP[1,:], c='b', marker='x')
plt.scatter(P1[0,:],P1[1,:], c='r', marker='x')




















