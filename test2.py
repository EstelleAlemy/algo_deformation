#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 23:31:48 2019

@author: estelle
"""

# Fichier de rotation de ma quadtree

import qdree_struct as qd
import  matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA
from scipy.optimize import least_squares




def M_rotate(teta):
     R=np.array([[np.cos(teta), -np.sin(teta)],
                 [np.sin(teta), np.cos(teta)]])
     return(R)
     
def get_indec(a,b,mat):
    ar1=np.where(mat[0,:]==a)
    ar2=np.where(mat[1,:]==b)
    return(int(np.intersect1d(ar1, ar2)))
#%%
# on fixe l'aléatoire
np.random.seed(seed=1)

N=50 #nb de pts
points=qd.Nuage(N)
list_point=points.make_point_list()

# Calcule de la quadtree
tree=qd.QTree(5,list_point, 8)
tree.get_node()
ct=tree.subdivide_qad()

# liste de pt de quadtree
node=tree.get_node()

# affichage de la quadtree
tree.graph()

#Calcule de la matrice des noeuds
mat_quad=np.zeros((2,len(node)))
for i,n in enumerate(node.keys()):
    mat_quad[0][i]=n[0] #x
    mat_quad[1][i]=n[1] #y



Tx=np.zeros((len(node),N)) # mat de transistion node pts selon x
Ty=np.zeros((len(node),N)) # mat de transition node pts selon y

ct=0 # compteur de pts

# liste de pts
X=np.zeros((2,N))
for n in node.keys():
    # pour chque noeud definir si il est un noeud racine
    pt_range=tree.range_query(n[0],n[1]) # recupération des pts dans une racine
    print(n[0],n[1])
    if pt_range != None: # si il il y a des pts dans la racines
       for p in pt_range: 
           # recupération des indices des noeuds dans la mat_quas
           i=get_indec(n[0],n[1],mat_quad) #Ok
           j= get_indec(n[0]+node[n],n[1],mat_quad) #Ok'
           k= get_indec(n[0],n[1]+node[n],mat_quad) #Ok''
           # affectation des poids à la matrice de tansition correspondantes
           Tx[j,ct]=(p.x)/(n[0]+node[n])
           Ty[k,ct]=(p.y)/(n[1]+node[n])
           X[0,ct]=p.x # affectatioin de chaque valeur de x => coordonnnées x
           X[1,ct]=p.y  # affectation de chaque valeur de y => coordonnés y
           ct+=1 # mise à jours du compteurs de pts

# vérification des valeurs
coorX=mat_quad[0,:]@Tx
coorY=mat_quad[1,:]@Ty

# Création de Y
rot=M_rotate(45)
Y=(X.T@rot).T 

# Affichage des pts
plt.figure()
plt.scatter(X[0,:],X[1,:], c='r', marker='.')
plt.scatter(Y[0,:],Y[1,:], c='b', marker='.')     

#%% Rotation de la quadtree
mat_quad2=np.zeros((2,len(node)))
# Fonction de couts
def func_cout_x(delta_T):
    A=(Y[0,:]-mat_quad[0,:]@Tx)
    A=A.reshape(A.shape[0],1)
    Bx=mat_quad[0,:]*delta_T
    Bx=Bx.reshape(Bx.shape[0],1)
    alpha=0.5
    res=LA.norm((A.T-Bx), None)+alpha*LA.norm(delta_T,None)
    return(res)

def func_cout_y(delta_T):
    A=(Y[1,:]-mat_quad[1,:]@Ty)
    A=A.reshape(A.shape[0],1)
    Bx=mat_quad[0,:]*delta_T
    Bx=Bx.reshape(Bx.shape[0],1)
    alpha=0.5
    res=LA.norm((A.T-Bx), None)+alpha*LA.norm(delta_T,None)
    return(res)
# definition de la rotation des X
t=np.ones((len(node)))*-10
res_1=least_squares(func_cout_x,t)
rx=res_1.x

# modification des noeuds en fonction des 
mat_quad2[0,:]=mat_quad[0,:]+rx

# definition rotation selon Y
res_2=least_squares(func_cout_y,t)
ry=res_2.x

# modification des noeuds en fonction des 
mat_quad2[1,:]=mat_quad[1,:]+ry


#%%
plt.figure()
plt.scatter(mat_quad2[0,:], mat_quad2[1,:], c='black', marker='x')
plt.scatter(Y[0,:],Y[1,:], c='b', marker='.')     
plt.scatter(X[0,:],X[1,:], c='r', marker='.') 






plt.figure()
plt.scatter(mat_quad[0,:], mat_quad2[1,:], c='black', marker='x')
plt.scatter(Y[0,:],Y[1,:], c='b', marker='.')     
plt.scatter(X[0,:],X[1,:], c='r', marker='.') 











