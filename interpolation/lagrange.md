# Interpolation de Lagrange : fondements théoriques

Code associé : [`lagrange.py`](lagrange.py)

## 1. Les polynômes de base de Lagrange

Pour $n + 1$ abscisses distinctes $t_0, \dots, t_n$, on définit pour chaque $i$ :

$$L_i(t) = \prod_{j \neq i} \frac{t - t_j}{t_i - t_j}$$

> **Propriété fondamentale.** Chaque $L_i$ est un polynôme de degré $n$ qui vaut **1 en $t_i$ et 0 en tous les autres points** :
>
> $$L_i(t_j) = \begin{cases} 1 & \text{si } j = i \\ 0 & \text{si } j \neq i \end{cases}$$

**Pourquoi.** Le numérateur contient le facteur $(t - t_j)$ pour chaque $j \neq i$, donc il s'annule en ces points. En $t = t_i$, chaque fraction vaut $\frac{t_i - t_j}{t_i - t_j} = 1$, donc le produit vaut 1.

## 2. Théorème : formule de Lagrange

> **Théorème.** Le polynôme d'interpolation des points $(t_i, y_i)$ s'écrit :
>
> $$P(t) = \sum_{i=0}^{n} y_i\,L_i(t)$$

**Preuve.**

- $P$ est une somme de polynômes de degré $n$, donc de degré au plus $n$.
- En $t = t_j$, tous les termes s'annulent sauf celui où $i = j$ : $P(t_j) = y_j \times 1 = y_j$.

$P$ vérifie donc toutes les conditions. Par **unicité** du polynôme d'interpolation (voir [`directe.md`](directe.md)), c'est le bon.

**Avantage.** Aucun système linéaire à résoudre : la formule donne directement le polynôme.

## 3. Propriété de partition de l'unité

> **Propriété.** Pour tout réel $t$ :
>
> $$\sum_{i=0}^{n} L_i(t) = 1$$

**Preuve.** On interpole la fonction constante $f(t) = 1$ : tous les $y_i$ valent 1. Le polynôme constant égal à 1 passe par ces points et est de degré $0 \leq n$. Par unicité, $\sum_i 1 \cdot L_i(t) = 1$.

**Intérêt pratique.** C'est une vérification gratuite des calculs. Le script l'affiche dans la ligne « Somme » du tableau.

**Application.** En $t = 0{,}5$ : $L_0 = 0{,}375$, $L_1 = 0{,}75$, $L_2 = -0{,}125$, et la somme vaut bien 1.

## 4. Théorème de l'erreur d'interpolation

Jusqu'ici, on n'a que des points. Si ces points proviennent d'une fonction $f$ (c'est à dire $y_i = f(t_i)$), on peut se demander à quel point $P$ est proche de $f$ **entre** les points.

> **Théorème.** Soit $f$ de classe $C^{n+1}$ sur un intervalle $I$ contenant les $t_i$, et $P$ son polynôme d'interpolation aux points $t_0, \dots, t_n$. Pour tout $x \in I$, il existe $\xi \in I$ tel que :
>
> $$f(x) - P(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}\,\prod_{i=0}^{n} (x - t_i)$$

**Idée de la preuve.** Si $x$ est l'un des $t_i$, les deux membres sont nuls. Sinon, on construit une fonction auxiliaire qui s'annule en $n + 2$ points (les $t_i$ et $x$). En appliquant le théorème de Rolle $n + 1$ fois de suite, on trouve un point $\xi$ où sa dérivée $(n+1)$-ième s'annule, ce qui donne la formule.

**Lecture de la formule.** L'erreur dépend de deux choses :

- **de $f$**, à travers sa dérivée $(n+1)$-ième : plus $f$ est « régulière », plus l'erreur est faible. Si $f$ est elle-même un polynôme de degré au plus $n$, cette dérivée est nulle et l'interpolation est **exacte** ;
- **du choix des points**, à travers le produit $\prod (x - t_i)$ : l'erreur est nulle aux points d'interpolation et grandit quand on s'en éloigne.

**Application.** Dans notre exemple, on ne connaît que trois valeurs, pas de fonction $f$. On ne peut donc pas estimer l'erreur commise en $t = 0{,}5$ et $t = 1{,}5$ : le théorème suppose que l'on connaisse $f$, ou au moins une borne sur sa dérivée troisième.

## 5. Plus de points n'est pas toujours mieux : le phénomène de Runge

On pourrait croire qu'en augmentant le nombre de points, le polynôme se rapproche forcément de $f$. C'est faux avec des **points régulièrement espacés** : pour certaines fonctions pourtant très régulières (l'exemple classique est $f(x) = \dfrac{1}{1 + 25x^2}$ sur $[-1, 1]$), le polynôme oscille de plus en plus fort près des bords de l'intervalle quand $n$ augmente.

L'explication se lit dans la formule d'erreur : avec des points équidistants, le produit $\prod (x - t_i)$ devient très grand près des bords.

**Remède.** Choisir des points plus resserrés aux bords, comme les **points de Tchebychev**, qui minimisent ce produit.

## 6. Limites de la méthode de Lagrange

- **Ajout d'un point.** Tous les $L_i$ dépendent de **toutes** les abscisses. Si on ajoute un point, il faut tout recalculer. La méthode de Newton ([`newton.md`](newton.md)) règle ce problème.
- **Coût d'évaluation.** Évaluer $P(x)$ avec la formule directe demande de l'ordre de $n^2$ opérations, contre $n$ pour Horner une fois les coefficients connus.