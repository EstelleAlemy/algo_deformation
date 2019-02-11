#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:31:27 2018

@author: estelle
"""

"""
    QuadTree data structure
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product, combinations


# Ficheri qui contient la listes des fonctions pour réaliser le codage d'un quadtree et 
# d'une octree (quadtree en 3D)


# Recusion subdivision pour un quadtree
def recursive_subdivide(node, k, depth, max_depth):
    if len(node.points)<=k or depth >= max_depth:
        return

    w_ = float(node.width/2)
    h_ = float(node.height/2)

    new_depth = depth + 1
    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p)
    recursive_subdivide(x1, k, new_depth, max_depth)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0+h_, w_, h_, p)
    recursive_subdivide(x2, k, new_depth, max_depth)
    
    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
    recursive_subdivide(x3, k, new_depth, max_depth)

    p = contains(node.x0+w_, node.y0+w_, w_, h_, node.points)
    x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p)
    recursive_subdivide(x4, k, new_depth, max_depth)

    node.children = [x1, x2, x3, x4]
    

# Récursion subdivision pour une octree   
def recursive_subdivide_oct(node, k, depth, max_depth):
    
    if len(node.points)<=k or depth >= max_depth:
        return

    w_ = float(node.width/2)
    h_ = float(node.height/2)
    a_ = float(node.alti/2)

    new_depth = depth + 1
    p = contains3D(node.x0, node.y0, node.z0,  w_, h_, a_, node.points)
    x1 = Node3D(node.x0, node.y0, node.z0,  w_, h_, a_, p)
    recursive_subdivide_oct(x1, k, new_depth, max_depth)

    p = contains3D(node.x0, node.y0+h_, node.z0, w_, h_,a_, node.points)
    x2 = Node3D(node.x0, node.y0+h_, node.z0, w_, h_, a_, p)
    recursive_subdivide_oct(x2, k, new_depth, max_depth)
    
    p = contains3D(node.x0+w_, node.y0, node.z0, w_, h_, a_, node.points)
    x3 = Node3D(node.x0 + w_, node.y0, node.z0, w_, h_, a_, p)
    recursive_subdivide_oct(x3, k, new_depth, max_depth)

    p = contains3D(node.x0+w_, node.y0+w_, node.z0, w_, h_, a_, node.points)
    x4 = Node3D(node.x0+w_, node.y0+h_, node.z0, w_, h_, a_, p)
    recursive_subdivide_oct(x4, k, new_depth, max_depth)
    
    p = contains3D(node.x0, node.y0, node.z0+a_, w_, h_, a_, node.points)
    x5 = Node3D(node.x0, node.y0,node.z0+a_, w_, h_, a_, p)
    recursive_subdivide_oct(x5, k, new_depth, max_depth)

    p = contains3D(node.x0, node.y0+h_, w_, node.z0+a_, h_, a_, node.points)
    x6 = Node3D(node.x0, node.y0+h_, node.z0+a_,  w_, h_, a_, p)
    recursive_subdivide_oct(x6, k, new_depth, max_depth)
    
    p = contains3D(node.x0+w_, node.y0, node.z0+a_, w_, h_, a_, node.points)
    x7 = Node3D(node.x0 + w_, node.y0, node.z0+a_, w_, h_, a_, p)
    recursive_subdivide_oct(x7, k, new_depth, max_depth)

    p = contains3D(node.x0+w_, node.y0+w_,node.z0+a_, w_, h_, a_, node.points)
    x8 = Node3D(node.x0+w_, node.y0+h_, node.z0+a_, w_, h_, a_, p)
    recursive_subdivide_oct(x8, k, new_depth, max_depth)

    node.children = [x1, x2, x3, x4, x5, x6, x7, x8]
    

# Rechcherche des points pour un quadtre
def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts

# Recherche des points pour une octree
def contains3D(x, y, z,  w, h, a, points):
    pts = []
    for point in points:
        if (point.x3 >= x and point.x3 <= x+w and point.y3>=y and 
        point.y3<=y+h and point.z3 >= z and point.z3 <= z+a):
            pts.append(point)
    return pts


#Recherche des enfants
def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += (find_children(child))
    return children

#%%
# Pout un point 2D => octree
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def rep(self):
        print('(',self.x, self.y,')')
        return
    
# Pour un point 3D => Octree
class Point3D():
    def __init__(self, x, y, z):
        self.x3 = x
        self.y3 = y
        self.z3 = z
        
    def rep(self):
        print('(',self.x3, self.y3, self.z3,')')
        return
        
# Définition d'un noeud  
class Node():
    def __init__(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []
        

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points
 
# Node 3D => octree
class Node3D():
    def __init__(self, x0, y0, z0, w, h, z, points):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.width = w
        self.height = h
        self.alti= z
        self.points = points
        self.children = []
        

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_alti(self):
        return self.alti
    
    def get_points(self):
        return self.points
    
# Création d'un nuage de point 2D  
class Nuage():
    def __init__(self, N):
        self.x1 =list( np.random.randint(101, size=N) )
        self.y1 = list(np.random.randint(101, size=N) )
        self.N=N
        
    def add_point(self, Point):
        self.x1.append(Point.x)
        self.y1.append(Point.y)
        self.N += 1
        
    def get_nuage(self):
        return(self.x1, self.y1)
        
    def taille(self):
        return(self.N)
        
    def make_point_list(self):
        self.point_list=[]
        for i in range(self.taille()):
             self.point_list.append(Point(self.x1[i],self.y1[i]))
        return(self.point_list)
        
    def Graph(self):
        x = [point for point in self.x1]
        y = [point for point in self.y1]
        plt.figure()
        plt.scatter(x, y,  marker=".")
        plt.show()
        return
  
# Création d'un nuage de points 3D
class Nuage3D():
    def __init__(self, N):
        self.x1 =list( np.random.randint(101, size=N) )
        self.y1 = list(np.random.randint(101, size=N) )
        self.z1 = list(np.random.randint(101, size=N) )
        self.N=N
        
    def add_point(self, Point):
        self.x1.append(Point.x3)
        self.y1.append(Point.y3)
        self.z1.append(Point.z3)
        self.N += 1
        
    def get_nuage(self):
        return(self.x1, self.y1, self.z1)
        
    def taille(self):
        return(self.N)
        
    def make_point_list(self):
        self.point_list=[]
        for i in range(self.taille()):
             self.point_list.append(Point3D(self.x1[i],self.y1[i], self.z1[i]))
        return(self.point_list)
        
    def Graph(self):
        x = [point for point in self.x1]
        y = [point for point in self.y1]
        z = [point for point in self.z1]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z)
        # Make legend, set axes limits and labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
        return

# Calculer le quadtree d'un nuage de point    
class QTree():
    def __init__(self, k, points, max_depth, _depth=0):
        self.max_depth=10
        self.threshold = k
        self.points = points
        self.root = Node(0, 0, 101, 101, self.points)
        self.max_depth = max_depth
        self._depth = _depth
        
    def add_point(self,x, y):
        self.points.append(Point(x, y))
    
    def get_points(self):
        return self.points
    
    def subdivide_qad(self):
        recursive_subdivide(self.root, self.threshold, self._depth, self.max_depth)
        
    def get_node(self):
        c = find_children(self.root)
        node_list={}
        for n in c:
            node_list[(n.x0, n.y0)]=[n.height]
        return(node_list)
        
    def range_query(self,x, y):
        c = find_children(self.root)
        for n in c:
            if n.x0==x and n.y0==y:
                return n.points
            
    def tree_query(self,x,y,a,pts):
        k=a[x,y][0]
        neighbors=[]
        pts=pts.make_point_list()
        X = [point.x for point in pts]
        Y = [point.y for point in pts]
        for i in range(len(X)):
            if (x<X[i]<=x+k) and (y<Y[i]<=y+k):
                neighbors.append(Point(X[i],Y[i]))
        return (neighbors)
    # Graphique du quadtree
    def graph(self):
        fig = plt.figure()
        plt.title("Quadtree")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.scatter(x, y, c='r', marker=".")
        plt.show()
        return
    
    def add_graph(self, news):
        fig = plt.figure()
        plt.title("Quadtree")
        new=news.make_point_list()
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        x2 = [point.x for point in new]
        y2 = [point.y for point in new]
        plt.scatter(x, y, c='r', marker=".")
        plt.scatter(x2, y2, c='b', marker=".")
        plt.show()
        return
    

## Classe de l'arbre 3D pour l'octree    

class QTree3D():
    def __init__(self, k, points, max_depth, _depth=0):
        self.max_depth=10
        self.threshold = k
        self.points = points
        self.root = Node3D(0, 0, 0, 101, 101, 101, self.points)
        self.max_depth = max_depth
        self._depth = _depth
        
    def add_point(self,x, y, z):
        self.points.append(Point3D(x, y, z))
    
    def get_points(self):
        return self.points
    
    def subdivide_oct(self):
        recursive_subdivide_oct(self.root, self.threshold, self._depth, self.max_depth)
        
    def get_node(self):
        c = find_children(self.root)
        compte=0
        for n in c:
            compte+=1
            print(n.x0, n.y0, n.z0)
            print(n.width, n.height, n.alti)
            for p in n.points:
                p.rep()
            print()
            if (compte%8)== 0:
                print('compte : ', compte)
        return
    
    # Graph e
    def graph(self):
        fig = plt.figure()
        plt.title("octree")
        ax = fig.add_subplot(1,3,1)
        ax2 = fig.add_subplot(1,3,2)
        ax3=    fig.add_subplot(1,3,3)
        c = find_children(self.root)
        print ("Number of segments: %d" %len(c))
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        print ("Minimum segment area: %.3f units" %min(areas))
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
            ax2.add_patch(patches.Rectangle((n.x0, n.z0), n.width, n.alti, fill=False))
            ax3.add_patch(patches.Rectangle((n.y0, n.z0), n.height, n.alti, fill=False))
        x = [point.x3 for point in self.points]
        y = [point.y3 for point in self.points]
        z = [point.z3 for point in self.points]
        ax.scatter(x, y, c='r', marker=".")
        ax2.scatter(x, z, c='r', marker=".")
        ax3.scatter(y, z, c='r', marker=".")
        plt.show()
        return
    
    def graph3D_line(self):
        ax = plt.figure().gca(projection='3d')
        
        #c = find_children(self.root)
        x = [point.x3 for point in self.points]
        y = [point.y3 for point in self.points]
        z = [point.z3 for point in self.points]
        ax.scatter(x, y, z, color='black', marker='s')
        # Drawing the basic cube
    
        r = [0, 100]
        for s, e in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                ax.plot3D(*zip(s, e), color="b")
        c = find_children(self.root)
        
        for n in c:
            r1=[n.x0, n.width]
            r2=[n.y0, n.height]
            r3=[n.z0, n.alti]
            for s, e in combinations(np.array(list(product(r1, r, r))), 2):
                if np.sum(np.abs(s-e)) == r[1]-r[0]:
                    ax.plot3D(*zip(s, e), color="b")
                    
            for s, e in combinations(np.array(list(product(r, r2, r))), 2):
                if np.sum(np.abs(s-e)) == r[1]-r[0]:
                    ax.plot3D(*zip(s, e), color="b")
                    
            for s, e in combinations(np.array(list(product(r, r, r3))), 2):
                if np.sum(np.abs(s-e)) == r[1]-r[0]:
                    ax.plot3D(*zip(s, e), color="b")
                    
         
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')                   
        plt.show()
        return
        
    
