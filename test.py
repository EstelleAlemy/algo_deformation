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

#%%
np.random.seed(seed=1)

points=qd.Nuage(20)
list_point=points.make_point_list()
#points.Graph()
tree=qd.QTree(4,list_point, 8)
tree.get_node()
ct=tree.subdivide_qad()
a=tree.get_node()

print(a[(50.5,0)])

tree.graph()
b=tree.range_query(50.5,0)
for p in b:
    p.rep()
#tree2=qd.QTree(2,list_point)
#tree2.subdivide_oct()
#tree2.graph()
pts=qd.Nuage(20)
pts.Graph()

tree.add_graph(pts)

#%% Search a translation of the octree
# Calcule des coeff c de chaque points
c={}
for n in a.keys():
    pt=tree.range_query(n[0], n[1])
    if len(pt)!=0:
        x_c=[]
        y_c=[]
        for p in pt:
            x_c.append(float((p.x-n[0])/a[n]))
            y_c.append(float((p.y-n[1])/a[n]))
            c[n]=[x_c,y_c]
        c[n]=np.array(c[n]).T

#%%        
#search neighbord of a case
rep= tree.tree_query(0,0,a,pts)

#%%% Essaie de la forme 3D
points=qd.Nuage3D(25)
list_point=points.make_point_list()
points.Graph()

tree=qd.QTree3D(4,list_point, 8)

ct=tree.subdivide_oct()
tree.get_node()

tree.graph()
tree.graph3D_line()

