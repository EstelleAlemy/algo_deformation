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
#%%
# Génération des matrices de point 2D en colonnes
x=np.random.randint(101, size=(2,200))
#x =  x - x.mean(axis=1)[:,np.newaxis]
#Orientation des données de 45° et -45°
R1=M_rotate(20)
R2=M_rotate(-45)

X1=R1@x
X2=R2@x

plt.figure()
plt.scatter(X1[0,:], X1[1,:], c='b', marker='x')
plt.scatter(X2[0,:], X2[1,:], c='r', marker='v')
plt.show()

#%%
#centrage de la matricce
x =  x - x.mean(axis=1)[:,np.newaxis]

X1=R1@x
X2=R2@x

plt.figure()
plt.scatter(X1[0,:], X1[1,:], c='b', marker='x')
plt.scatter(X2[0,:], X2[1,:], c='r', marker='v')
plt.show()
#%%
#Calcule des vecteurr propre des matrice de covariance de X1 et X2
_,U1=LA.eig(X1@X1.T)
_,U2=LA.eig(X2@X2.T)

#newX  = U1@X1
#plt.scatter(newX[0,:], newX[1,:], c='y', marker='p')

#newX  = U2.T@U1@X1
#plt.scatter(newX[0,:], newX[1,:], c='m', marker='p')

newX  = U2@U1.T@X1
plt.figure()
plt.scatter(X1[0,:], X1[1,:], c='b', marker='x')
plt.scatter(X2[0,:], X2[1,:], c='r', marker='v')
plt.scatter(newX[0,:], newX[1,:], c='k', marker='p')
plt.show()


















