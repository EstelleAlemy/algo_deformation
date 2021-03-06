# Rapport algorithme de déformation non rigide

**Objectif:** Déterminer ou estimer une transformation spatial qui relie les positions dans une image aux positions correspondantes dans une ou plusieurs autres images. Puis appliquer cette transformation à des données 3D.

## INTRODUCTION

Tout d'abord introduisons la notion de forme puisque l'objectif du recalage sur des images 2D ou 3D est de mettre en correspondance des formes. Une forme selon le dictionnaire est l'organisation des contours d'un objet. Une forme (géométrique) simple peut être définit comme un objet géométrique de base tel qu'un ensemble de deux ou plusieurs points, une ligne, une courbe, un plan, une figure plane (par exemple carré ou cercle en 2D), ou une figure solide (cube ou sphère en 3D). Mais dans toutes les formes géométriques on retrouve d'une par des points et de l'autres des arrêtes qui vont faire la liaison entre les points (dessiner le contours de la forme).

Le recalage correspond à l'estimation d'une transformation géométrique permettant la superposition spatiale des structures anatomiques ou fonctionnelles présentes dans les images où formes à recaler.
Que l'on peut formuler comme ci-dessous:

<img align="center" src="https://latex.codecogs.com/svg.latex?\Large&space;\min{f(I1,t(I2))}_{t\in{T}}"/>

- I1 et I2 images à recaler ou informations extraites de ces images
- t: transformation
- T ensemble de des transformation admissible
- f critère de dissimilarité ou de similarité

Ainsi pour mettre en place un systeme de recalage de forme ou d'image on doit définir 4 critères:
*  L'information à mettre en correspondance (exemple :points d'intérets) 
*  La mesure de similarité(distance) qui définit la concordance de deux images.
*  Le modèle de transformation, qui spécifie la façon dont l'image source peut être modifiée pour correspondre à la cible.
*  Le processus d'optimisation qui fait varier les paramètres du modèle de transformation pour maximiser l'appariement critère.

On peut définir plusieurs contexte appliatif du recalage qui sont:
* Le recalage intra-individu, les images viennent du même sujet (ex: plusieurs images d'une tumeur dans le temps
* Le recalage inter-individu (plusieurs sujet ou bien un sujet face un modèle de référence)
* La correction de distorsion dans géométriques dans une images.

Le recalage d'image à deux nombreuses applications dans le domaine médical dans lequel il permet par exemple de fusionner les images d'un même patient mais pas seulement le recalage d'image à des application en reconnaissance faciale (calculer la déformation entre 2 visage) où encore dans des problèmes de cartographie (effectuer la carte de disparité d'une image).

Dans les partie suivantes on va voir les blocs de fonctions de bases que l'on a implémenté dans l'objectif de composer un algoritme de recalage. 

## 1) La distance de Hausdorff (Mesure de similarité)

### définition théorique
La distance de Hausdorff est un outil mathématique permettant  mesurer l’éloignement entre deux ensembles de points. Pour mesurer celle-ci, on prend la plus grandes de toutes les distances d’un ensemble, au point le plus proches dans un autre ensemble, ce qui se traduit par cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;h(A,B)=\max{({\min{{d(a,b)}})}" title="\Large x=\max_{A,B}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;a\in{A}"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;b\in{B}"/>
avec A et B deux sous ensembles distincts et d une mesure de distance entre 2 points (exemple la distance euclienne).



On note que la distance de Hausdorff est asymétrique c’est à dire que h(A,B) n’est pas égale à h(B,A), ceci est une propriété des fonction de types maxmin, donc on généralise la distance de Hausdorff avec cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;H(A,B)=\max({h(A,B),h(B,A)})"/>

On peut dire que A et B sont proches si tous les point de A sont proches d’un ou plusieurs points de B.

<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/hausdorff.png"/>

### Application

Le fichier **haussdorff.py**, est la définition de notre fonction qui calcule la distance de hausdorff pour des nuages de points 2D créés artificiellement.
Pour définir cette fonction on suit 3 étapes:

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

Une octree est une structure de type arbre dans laquelle chaque noeud possède huit enfants. Dans notre cas l'octree correspond à l'application d'une quadtree en trois dimension. L'octree est utilisé pour réduire les dimensions, plutôt que de servir de l'ensemble des points on va appliquer la transformation sur les points noeuds de l'octree.

Les octrees sont très utilisés, car ils permettent une recherche de voisins efficace et une subdivision adaptative. Il en résulte un grand nombre d'applications :

- la détection de collision en trois dimensions dans les logiciels de CAO ou les moteurs physiques
- le sparse voxel octree pour réaliser du ray-casting (calcule d'images de synthèses accélérés)
- l'élimination des objets hors du cône de vue dans le cadre d'un rendu 3D 
- les maillages, d'une manière générale, notamment dans le cadre de la méthode des éléments finis ;
- le problème à n corps

**Vocabulaire**

Définissons un peu de vocabulaire qui indique les éléments essentiel à une octree:

- un nœud est un élément de l'arbre. Dans un octree, un nœud correspond à un cube dans l'espace 3D à partitionner
- la racine d'un arbre est l'unique nœud ne possédant pas de parent, il permet d'accéder à tous les éléments de l'arbre (dans l'espace c'est le premier cube)
- un nœud interne est un élément qui a des fils (huit dans notre cas) 
- une feuille de l'arbre est un nœud qui n'a pas de fils
- la profondeur (à fixer) nombre d'itérations maximal pour réaliser l'octree
- le seuil (treshold) nombre d'information (ici des points) maximal à stocker dans un noeuds avant séparation.

## Application
#### a) Quadtree

Une quadtree est une structure arbre où chaque noeud possèdent quatre enfant. On l'utilise pour partitionner un espace bidimensionnel en le subdivisent récursivement en quatre noeuds.

<img align="center"  src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/quadtree.png" width="450" height="450"/>

On a commencé par travailler sur des nuages de points en 2D dimensions et donc implémenter une quadtree dans ce cas. 
L'ensemble des implémentations pour la quadtree sont définit dans le fichier **qdree_struct.py** qui implémente des objet de type octree et quadtree.

**Implémentation :**
Pour implémenter on a suivit 4 étapes:

1. Nuage de points

 On creer un nuage de points aléatoires(valeur entre 0 et 100) de taille N, contients une liste de N points 2D ayant une coordonnée x et y.
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

On définit aussi le _treshold_ qui est le nombre de points maximal que l'on veut dans chaque partie de l'espace ainsi que la *max_depth*  qui est le nombre de récursion maximales autorisées (au-dela de cette limite l'algo s'arrête même-ci le treshold n'est pas atteint).
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

Une fois la division récursive appliquée on retourne les enfants de chaque noeud afin de récuperer les noeuds de la quadtree. Et on se sert des position des noeuds pour dessiner l'espace de quadtree.
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
Et on obtient les figures suivantes, le code pour les exemples se trouve dans le fichier **test.py**.

Nuage de points de Base
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/nuage2D.png"/>

Après quadtree
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/quad2D.png"/>


#### a) Octree

L'Octree suit le même principe que quadtree précédemment expliquer. Dans le cas de l'octree l'espace est en 3 dimensions donc l'espace est séparé en 8 sous parties. Pour implémenter l'octree on a ajouter l'équivalent d'une dimension en plus aux codes utilisés pour quadtree.

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

2. Suppression des composante rotation, translation et échelle

  - translation : correspond à un centrage des données sur l'origine

	<img src="https://latex.codecogs.com/svg.latex?\Large&space;\bar{a}=\frac{\sum_{i=1}^{n}{a_i}}{n}"/>  
	<img src="https://latex.codecogs.com/svg.latex?\Large&space;\bar{b}=\frac{\sum_{i=1}^{n}{b_i}}{n}"/>

<img src="https://latex.codecogs.com/svg.latex?\Large&space;A={A-\bar{a}}"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;B={B-\bar{b}}"/>

  - mise à l'échelle : correspond à une standardisation des données (division par l'écart-type)

	<img src="https://latex.codecogs.com/svg.latex?\Large&space;s_a=\frac{\sum_{i=1}^{n}{\sqrt{(a_i-\bar{a})^2}}}{n}"/>  
	<img src="https://latex.codecogs.com/svg.latex?\Large&space;s_b=\frac{\sum_{i=1}^{n}{\sqrt{(b_i-\bar{b})^2}}}{n}"/>

<img src="https://latex.codecogs.com/svg.latex?\Large&space;A=\frac{A}{s_a}"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;B=\frac{B}{s_b}"/>

  - Rotation : trouver l'ange de rotation optimale entre les 2 distributions

On utilise la décomposition en valeurs singulières des distribution (SVD) pour obtenir
<img src="https://latex.codecogs.com/svg.latex?\Large&space;R=VU^{T}"/>

On peut illustrer ces différentes étapes avec l'image ci-dessous
<img align="center"  src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/rotat.gif" width="450" height="400"/>

3. Calculer la distance pour passer de l’objet B à l’objet A.

### Application

On a implémenté une fonction pour génerer un exemple d'alignement de procrust en python dans le fichier **procrust.py**, on a suivit 5 étapes:

1. On a définit une distribution de points x de manière aléatoire.

2. On a appliquer une matrice de rotation sur x pour obtenir 2 distributions distinctes:
	<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{pmatrix}\cos(\theta)&-\sin(\theta)\\\sin(\theta)&\cos(\theta)\end{pmatrix}"/>

```
def M_rotate(teta):
     R=np.array([[np.cos(teta), -np.sin(teta)],
                 [np.sin(teta), np.cos(teta)]])
     return(R)
# Génération des matrices de point 2D en colonnes
x=np.random.randint(101, size=(2,200))

#Orientation des données de 45° et -45°
R1=M_rotate(20)
R2=M_rotate(-45)

X1=R1@x
X2=R2@x
```
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/distribution.png"/>

3. On centre les distributions
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/dist_centre.png"/>

4. On calcule les vecteur propres des matrices de covariancese de X1 et X2
```
_,U1=LA.eig(X1@X1.T)
_,U2=LA.eig(X2@X2.T)
```

5. On applique la rotation: ici on fait une rotation de la distribution X1(bleu) vers X2(rouge)
```
newX  = U2@U1.T@X1
```
<img src="https://github.com/EstelleAlemy/algo_deformation/blob/master/image/rotation.png"/>

## Sources

[1](https://en.wikipedia.org/wiki/Procrustes_analysis)

[2](https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem)

[3](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.directed_hausdorff.html)

[4](https://en.wikipedia.org/wiki/Hausdorff_distance)

[5](https://kpully.github.io/Quadtrees/)

[6](https://en.wikipedia.org/wiki/Quadtree)

[7](http://cgm.cs.mcgill.ca/~godfried/teaching/cg-projects/98/normand/main.html)













