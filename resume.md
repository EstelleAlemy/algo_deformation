# Rapport algorithme de déformation non rigide

**Objectif:** Déterminer une transformation spatial qui relie les positions dans une image aux positions correspondantes dans une ou plusieurs autres images. Puis appliquer cette transformation à des données 3D.

Que l'on peut formuler comme ci-dessous:

<img src="https://latex.codecogs.com/svg.latex?\Large&space;\min{f(I1,t(I2))}_{t\in{T}}"/>

- I1 et I2 images à recaler ou information extraites de ces images
- t: transformation
- T ensemble de des transformation admissible
- f critère de dissimilarité ou de similarité

3 critères pour composer un algorithme de déformation/recalage :

*  La mesure de similarité(distance) qui définit la concordance de deux images.
*  Le modèle de transformation, qui spécifie la manière de l’image source peut être modifiée pour correspondre à la cible.
*  Le processus d'optimisation qui fait varier les paramètres du modèle de transformation pour maximiser l'appariement critère.

Dans les partie suivantes on va voir les blocs de fonctions de bases que l'on a implémenté dans l'objectif de compser un algoritme de recalage. 

## 1) La distance de Hausdorff (Mesure de similarité)

### définition théorique
La distance de Hausdorff est un outil mathématique permettant  mesure l’éloignement entre deux ensembles de point. Pour mesurer celle-ci, on prend la plus grandes de toutes les distances d’un ensemble, au point le plus proches dans un autres ensemble, ce qui se traduit par cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;h(A,B)=\max{({\min{{d(a,b)}})}" title="\Large x=\max_{A,B}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;a\in{A}"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;b\in{B}"/>
avec A et B deux sous ensemble distinct et d une mesure de distance entre 2 points (exemple la distance euclienne).


On note que la distance de Hausdorff est asymétrique c’est à dire que h(A,B) n’est pas égale à h(B,A), ceci est une propriété des fonction de types maxmin, donc on généralise la distance de Hausdorff avec cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;H(A,B)=\max({h(A,B),h(B,A)})"/>

On peut dire que A et B sont proches si tous les point de A sont proches d’un ou plusieurs points de B.

<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/hausdorff.png"/>

### Application

Le fichier **haussdorff.py**, est la définition de notre fonction qui calcule la distance de hausdorff pour des nuages de points 2D créés artificiellement.
Pour définir cette fonction  on suit 3 étapes:

- Matrice euclidienne: on calcule une matrice qui contient les distances euclidiennes entres tous les points de 2 ensemble A et B
- On calcule h1 et h2 qui corresponde à l'équation 1
- On choisit le max entre h1 et h2

```
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
```


On a comparé notre résultat à la fonction **directed_hausdorff** de **_scipy.spatial.distance_** et on obtient les mêmes résultats.
```
d=max(directed_hausdorff(a, b)[0], directed_hausdorff(b, a)[0])
```

## 2) Implémentation Octree

Une octree est une structure de type arbre dans laquelle chaque noeud possède huit enfant. Dans notre cas l'octree correspond à l'application d'une quadtree en trois dimension. L'octree est utilisé pour réduire les dimensions, plutôt que de servir de l'ensemble des points on va appliquer la transformation sur les points noeuds de l'octree.


### a) Quadtree

Une quadtree est une structure arbre où chaque noeud possèdent quatre enfant. On l'utilise pour partitionner un espace bidimensionnel en le subdivisent récursivement en quatre noeuds.

<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/quadtree.png"/>

On a commencé par travaillé sur des nuage de points en 2D dimensions et donc implémenter une quadtree dans ce cas. 
L'ensemble des implémentations pour la quadtree sont définit dans le fichier **qdree_struct.py** qui implémente des objet de type octree et quadtree.

**Implémentation :**
Pour implémenter on a suivit 4 étapes:

1. Nuage de points

 On creer un nuage de points aléatoires(valeur entre 0 et 100) de taille N, contients une liste de N points 2D ayant une coordonnées x et y.
```
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
```
2. Initialisation

Notre structure va prendre un premier noeud racine qui contient les position x et y minimum (0,0) et les positions x,y maximal(101, 101), ainsi que l'ensemble des points du nuage de points et n'a pas d'enfants. 

On définit aussi le treshold qui est le nombre de points maximale que l'on veut dans chaque partie de l'espace ainsi que la profondeur maximale qui est le nombre de récursion maximal autorisée (au-dela de cette limite l'algo s'arrête même-ci le treshold n'est pas atteint).
```
class QTree():
    def __init__(self, k, points, max_depth, _depth=0):
        self.max_depth=10
        self.threshold = k
        self.points = points
        self.root = Node(0, 0, 101, 101, self.points)
        self.max_depth = max_depth
        self._depth = _depth
```

3. Division récursive

On va appliquer la fonction **recursive_subdivide** à la racine.
```
    def subdivide_qad(self):
        recursive_subdivide(self.root, self.threshold, self._depth, self.max_depth)
```
Cette fonction récursive divise en 2 les positions x et y maximale, séparant ainsi l'espace en quatre partie(noeuds) à chaque récursion. La fonction s'arrête quand on au maximum k point dans chaque partie de l'espace où que l'on atteint le nombre de récursion maximal.

Remarque: la fonctions **contains** utilisé dans **recursive_subdivide** sert à rechercher les points dans chaque partie de l'espace.
```
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

def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts
```
3. Récupération des noeuds

Une fois la division récursive appliquée on retourne les enfant de chaque noeuds afin de récuperer les noeuds de la quadtree. Et on se sert des position des noeuds pour dessiner l'octree.
```
def get_node(self):
        c = find_children(self.root)
        for n in c:
            print(n.x0, n.y0)
            for p in n.points:
                p.rep()
            print()
        return
```
**Résultat :**

On a appliquée notre algorithme sur un nuage de 100 points, on à fixé le nombre de points par espace à k=2 et le profondeur max à p=8.
Et on obtient les figures suivantes, le code pour les exemples se trouve dans le fichier test.py

Nuage de points de Base
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/nuage2D.png"/>

Après quadtree
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/quad2D.png"/>


### a) Octree

L'Octree suit le même principe que quadtree précédemment expliquer. Dans le cas de l'octree l'espace est en 3 dimensions donc l'espace est séparé en 8 sous parite. Pour implémenter l'octree on a ajouter l'équivalent d'une dimension en plus au code utilisés pour quadtree.

```
class QTree3D():
    def __init__(self, k, points, max_depth, _depth=0):
        self.max_depth=10
        self.threshold = k
        self.points = points
        self.root = Node3D(0, 0, 0, 101, 101, 101, self.points)
        self.max_depth = max_depth
        self._depth = _depth
```
**Résultats :**

Images résultante de l'application d'une octree sur un nuage de points (code exemple dans test.py)

<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/point.png"/>

<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/octree.png"/>

<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/octree_plane.png"/>


## 3) Alignement de Procuste

### Définition théorique 
Pour deux nuages de points A et B (ou forme) l'alignement de procuste à pour but de trouver la transformation qui nous permet de passer de A vers B.

La procédure suit en générale 3 étapes :

1. Rechercher, dans la forme à étudier, un certain nombre de points considérés comme des points de références ou points d'intérêts.

2. Suppression des composante rotation, translation et échelles 

  - translation : correspond à un centrage des données sur l'origine

<img src="https://latex.codecogs.com/svg.latex?\Large&space;ca=\sum_{i=0,\i\neq}^n a_{i}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;cb=\sum_{i=0,\i\neq}^n b_{i}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;A = A-ca"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;B = B-cb"/>

  - mise à l'échelle : correspond à une standardisation des données (division par la variance)
  - Rotation : trouver l'ange de rotation optimale entre les 2 distributions
