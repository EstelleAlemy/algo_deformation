#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:15:03 2018

@author: estelle

test de la fonction quadtree pour implementer un qdtree

"""


# test

import qdree_struct as qd
import  matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA
#%%
np.random.seed(seed=1)

points=qd.Nuage(20)
list_point=points.make_point_list()
#points.Graph()
tree=qd.QTree(4,list_point, 8)
tree.get_node()
ct=tree.subdivide_qad()
a=tree.get_node()

#print(a[(50.5,0)])
tree.graph()

b=tree.range_query(50.5,0)

#tree2=qd.QTree(2,list_point)
#tree2.subdivide_oct()
#tree2.graph()

#tree.add_graph(pts)
mat_quad=np.zeros((2,len(a)))
for i,n in enumerate(a .keys()):
    mat_quad[0][i]=n[0] #x
    mat_quad[1][i]=n[1] #y
    
# construction de la matrice des X

def get_indec(a,b,mat):
    ar1=np.where(mat[0,:]==a)
    ar2=np.where(mat[1,:]==b)
    return(int(np.intersect1d(ar1, ar2)))
    
c=tree.get_c()
T=np.zeros((len(a),20))
ct=0
x=np.zeros((2,20))
for n in a.keys():
    pt_range=tree.range_query(n[0],n[1])
    print(n[0],n[1])
    if pt_range != None:
       for p in pt_range: 
           i=get_indec(n[0],n[1],mat_quad)
           j= get_indec(n[0]+a[n],n[1],mat_quad)
           k= get_indec(n[0],n[1]+a[n],mat_quad)
           T[i,ct]=1/a[n]
           T[j,ct]=(p.x-n[0])/a[n]
           T[k,ct]=(p.y-n[1])/a[n]
           x[0,ct]=p.x
           x[1,ct]=p.y
           ct+=1
       
def M_rotate(teta):
     R=np.array([[np.cos(teta), -np.sin(teta)],
                 [np.sin(teta), np.cos(teta)]])
     return(R)
rot=M_rotate(45)
Y=(x.T@rot).T           
Tr=mat_quad@T

plt.figure()
plt.scatter(x[0,:],x[1,:], c='r', marker='.')
plt.scatter(Y[0,:],Y[1,:], c='b', marker='.')
#%% Search a translation of the octree
# Calcule des coeff c de chaque points
#c={}
#for n in a.keys():
    # find point of the distribution in a case
#    pt=tree.range_query(n[0], n[1])
#    if len(pt)!=0:
#        x_c=[]
#        y_c=[]
#        for p in pt:
#            x_c.append(float((p.x-n[0])/a[n]))
#            y_c.append(float((p.y-n[1])/a[n]))
#            c[n]=[x_c,y_c]
#        c[n]=np.array(c[n]).T

#%%   Minimisation pour une seul case de l'octree     
from scipy.optimize import least_squares

def func_cout(delta_T):
    A=(Y-mat_quad@T)
    Bx=mat_quad@delta_T
    alpha=100
    res=LA.norm((A.T-Bx), None)+alpha*LA.norm(delta_T,None)
    return(res)
    
t=np.zeros((len(a)))
res_2=least_squares(func_cout,t)
l=res_2.x
#%%% Essaie de la forme 3D
points=qd.Nuage3D(25)
list_point=points.make_point_list()
points.Graph()

tree=qd.QTree3D(4,list_point, 8)

ct=tree.subdivide_oct()
tree.get_node()

tree.graph()
tree.graph3D_line()

