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
import random, math



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
points.Graph()

Y=np.zeros((2,N))
for i in range(N):
    a=np.random.randint(50,200)
    #b=random.gauss(0,1)
    Y[0,i]=a
    Y[1,i]=a
plt.scatter(Y[0,:],Y[1,:], c='r', marker='.', label= 'valeur avec rotation')  
plt.title('Distribution de départ') 
#%%
#Y=M_rotate(90).T@pts
   
points.make_mean()
points.make_echelle()
points.Graph()
pts=points.make_array_list()
    
    
moy=np.mean(Y, axis=1)
Y=Y.T-moy
Y=Y.T
    
# echelle
Y=Y/Y.std()

plt.scatter(Y[0,:],Y[1,:], c='r', marker='.', label= 'valeur avec rotation')  
plt.title('Distributions de départ centrées et mise à l echelle')  
#%% Procust
_,U1=LA.eig(Y@Y.T)
_,U2=LA.eig(pts@pts.T)

newY  = U2@U1.T@Y
plt.figure()
plt.scatter(pts[0,:], pts[1,:], c='b', marker='.', label='X')
plt.scatter(newY[0,:], newY[1,:], c='R', marker='.', label='newY')
#plt.scatter(Y[0,:], Y[1,:], c='r', marker='x', label='Y')
plt.legend()
plt.title('Distributions retrait rotation')  

#%%
list_point=points.make_point_list()
# Calcule de la quadtree
tree=qd.QTree(4, list_point, 8, -2)
tree.get_node()
ct=tree.subdivide_qad()

# liste de pt de quadtree
node=tree.get_node()
ind=tree.get_indice(node)

# centrage de la distribution
#pt=np.array(points)

# affichage de la quadtree
tree.graph()
plt.scatter(newY[0,:], newY[1,:], c='b', marker='.', label='newY')
#%%
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
    #print(n[0],n[1])
    if pt_range != None: # si il il y a des pts dans la racines
       for p in pt_range: 
           # recupération des indices des noeuds dans la mat_quas
           i=get_indec(n[0],n[1],mat_quad) #Ok
           j= get_indec(n[0]+node[n],n[1],mat_quad) #Ok'
           k= get_indec(n[0],n[1]+node[n],mat_quad) #Ok''
           # affectation des poids à la matrice de tansition correspondantes
           print(p.x, p.y)
           Tx[j,ct]=(p.x)/( node[n]+n[0] )
           if math.isinf(Tx[j,ct])== True:
               Tx[j,ct]=1
           Ty[k,ct]=(p.y)/( node[n]+n[1] )
           if math.isinf(Ty[k,ct])== True:
               Ty[k,ct]=1
           X[0,ct]=p.x
           X[1,ct]=p.y
           ct+=1 # mise à jours du compteurs de pts


# vérification des valeurs
coorX=mat_quad[0,:]@Tx
coorY=mat_quad[1,:]@Ty



#%% Rotation de la quadtree
mat_quad2=np.zeros((2,len(node)))
# Fonction de couts
def func_cout_x(delta_T):
    A=(Y[0,:]-mat_quad[0,:]@Tx)
    A=A.reshape(A.shape[0],1)
    Bx=mat_quad[0,:]*delta_T
    Bx=Bx.reshape(Bx.shape[0],1)
    alpha=1*10e-5
    res=LA.norm((A.T-Bx), None)+alpha*LA.norm(delta_T,None)
    return(res)

def func_cout_y(delta_T):
    A=(Y[1,:]-mat_quad[1,:]@Ty)
    A=A.reshape(A.shape[0],1)
    By=mat_quad[1,:]*delta_T
    By=By.reshape(By.shape[0],1)
    alpha=1*10e-5
    res=LA.norm((A.T-By), 'fro')+alpha*LA.norm(delta_T, 'fro')
    return(res)
    
    
def func_cout(delta_t):
    Ax=(newY[0,:]-mat_quad[0,:]@Tx)
    Ay=(newY[1,:]-mat_quad[1,:]@Ty)
    A=np.hstack((Ax,Ay))
    A=A.reshape(A.shape[0],1)   
    Bx=mat_quad[0,:]
    By=mat_quad[1,:]
    B=np.hstack((Bx,By))*delta_t
    B=B.reshape(B.shape[0],1)
    alpha=1e-8
    res=LA.norm((A.T-B), None)+alpha*LA.norm(delta_t,None)
    return(res)
    


#%%

t=np.zeros((len(node)*2))
res_1=least_squares(func_cout,t)
rx=res_1.x


#%%
mat_quad2=np.copy(mat_quad)
n=len(node)
mat_quad2[0,:]=mat_quad2[0,:]+rx[0:n].T
mat_quad2[1,:]=mat_quad2[1,:]+rx[n-1:(n*2)-1].T


plt.figure()
plt.scatter(mat_quad2[0,:], mat_quad2[1,:], c='black', marker='x', label='new quadtree')
plt.scatter(mat_quad[0,:], mat_quad[1,:], c='red', marker='x', label='old quadtree')
plt.scatter(newY[0,:],newY[1,:], c='b', marker='.', label= 'valeur avec rotation')     
p#lt.scatter(X[0,:],X[1,:], c='r', marker='.', label='vrai valeur ') 
plt.legend()
plt.title('déplacement pour rotation de 95° du nuage de points')



#%% Etablir le voisinage
from scipy.spatial import KDTree


def find_neighbors(c,indices):
    if c not in indices:
        return('noeuds pas dans la listes')
    else:
        i=indices[c][0]
        j=indices[c][1]
        neigh=[]
    
    for pt, ind in indices.items():
        if (ind[0]==i and ind[1]==j+1) or (ind[0]==i and ind[1]==j-1):
            neigh.append(pt)
        if (ind[1]==j and ind[0]==i+1) or (ind[1]==j and ind[0]==i-1):
            neigh.append(pt)
        
        #cas spéciaux
    if ( c!=(0,0) and c!=(0,101) and c!=(101,0) and c!=(101,101)  and len(neigh)<=2):
        for pt, ind in indices.items():
            if (ind[0]==i and ind[1]==j+2) or (ind[0]==i and ind[1]==j-2):
                neigh.append(pt)
            if (ind[1]==j and ind[0]==i+2) or (ind[1]==j and ind[0]==i-2):
                neigh.append(pt)
       
    #check extrema    
    if ( (c==(0,0) or c==(0,101) or c==(101,0) or c==(101,101))  and (len(neigh)>2)):
        for pt, ind in indices.items():
            if (ind[0]==i and ind[1]==j+2) or (ind[0]==i and ind[1]==j-2):
                neigh.append(pt)
            if (ind[1]==j and ind[0]==i+2) or (ind[1]==j and ind[0]==i-2):
                    neigh.append(pt) 
                    
    #check nb neiborg
    
    
    return(neigh)
    
pt=(25.25,25.25)
a=find_neighbors(pt, ind)
tree.graph()
plt.scatter(pt[0],pt[1], c='green')
for n in a:
    plt.scatter(n[0],n[1], c='b')
