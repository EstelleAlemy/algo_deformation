# Rapport

**Objectif:** Déterminer une transforamtion spatial qui relie les positions dans une image aux positions correspondantes dans une ou plusieurs autres images.

Que l'on peut formuler comme ci-dessous:

## 1) La distance de Hausdorff

La distance de Hausdorff est un outil mathématique permettant  mesure l’éloignement entre deux ensembles de point. Pour mesurer celle-ci, on prend la plus grandes de toutes les distances d’un ensemble, au point le plus proches dans un autres ensemble, ce qui se traduit par cette formule :

<img src="https://latex.codecogs.com/svg.latex?\Large&space;h(A,B)=\max{({\min{d(a,b)})}" title="\Large x=\max_{A,B}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;a\in A"/>
<img src="https://latex.codecogs.com/svg.latex?\Large&space;b\in B"/>
avec A et B deux sous ensemble distinct.

