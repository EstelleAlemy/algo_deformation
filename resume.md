# Rapport

**Objectif:** Déterminer une transforamtion spatial qui relie les positions dans une image aux positions correspondantes dans une ou plusieurs autres images.

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



## 1) La distance de Hausdorff

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
