# Rapport

**Objectif:** Déterminer une transforamtion spatial qui relie les positions dans une image aux positions correspondantes dans une ou plusieurs autres images.

Que l'on peut formuler comme ci-dessous:

## 1) La distance de Hausdorff

La distance de Hausdorff est un outil mathématique permettant  mesure l’éloignement entre deux ensembles de point. Pour mesurer celle-ci, on prend la plus grandes de toutes les distances d’un ensemble, au point le plus proches dans un autres ensemble, ce qui se traduit par cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;h(A,B)=\max{({\min{d(a,b)})}" title="\Large x=\max_{A,B}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;a\in{A}"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;b\in{B}"/>
avec A et B deux sous ensemble distinct et d une mesure de distance entre 2 points (exemple la distance euclienne).

On note que la distance de Hausdorff est asymétrique c’est à dire que h(A,B) n’est pas égale à h(B,A), ceci est une propriété des fonction de types maxmin, donc on généralise la distance de Hausdorff avec cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;h(A,B)=\max{h(A,B),h(B,A)}"/>

On peut dire que A et B sont proches si tous les point de A sont proches d’un ou plusieurs points de B.


