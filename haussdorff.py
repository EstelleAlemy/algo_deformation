#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:28:11 2018

@author: estelle

 Distance de Hausdorff
"""
import numpy as np
from scipy.spatial.distance import directed_hausdorff
# Compute the eculidean distan
def euclidean(a,b):
    return (np.sqrt((a-b)**2))

def euclidean_pt(a,b):
    e=np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return(e)    

def mat_distance(u,v):
    L=u.shape[0]
    C=v.shape[0]
    mat_dist=np.zeros((L,C))
    for i in range(L):
        for j in range(C):
            mat_dist[i,j]=euclidean(u[i],v[j])
    return(mat_dist)
    
def haussdorf(u,v):
    mat_dist=mat_distance(u,v)
    h1=max(np.amin(mat_dist, axis=0))
    h2=max(np.amin(mat_dist, axis=1))
    return (max(h1,h2))
 
N=5
b=np.random.randint(1,10, size=N)
a=np.random.randint(1,10, size=N)

a=a.reshape(N,1)
b=b.reshape(N,1)
c=haussdorf(a,b)
d=max(directed_hausdorff(a, b)[0], directed_hausdorff(b, a)[0])

