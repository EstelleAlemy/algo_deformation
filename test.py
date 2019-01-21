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

points=qd.Nuage(100)
list_point=points.make_point_list()
points.Graph()
tree=qd.QTree(2,list_point, 8)
tree.get_node()
ct=tree.subdivide_qad()
tree.get_node()

tree.graph()

#tree2=qd.QTree(2,list_point)
#tree2.subdivide_oct()
#tree2.graph()



#%%% Essaie de la forme 3D
points=qd.Nuage3D(10)
list_point=points.make_point_list()
points.Graph()

tree=qd.QTree3D(3,list_point, 8)

ct=tree.subdivide_oct()
tree.get_node()

tree.graph()
tree.graph3D_line()

