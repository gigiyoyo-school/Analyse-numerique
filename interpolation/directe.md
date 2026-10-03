# Interpolation : méthode directe et théorème fondamental

Code associé : [`directe.py`](directe.py)

## 1. Le problème d'interpolation

On dispose de $n + 1$ points $(t_0, y_0), (t_1, y_1), \dots, (t_n, y_n)$ avec des abscisses $t_i$ **deux à deux distinctes**. On cherche un polynôme $P$ de degré au plus $n$ qui passe par tous ces points :

$$P(t_i) = y_i \quad \text{pour } i = 0, 1, \dots, n$$

Ce théorème est la base commune des trois méthodes du dossier : directe, Lagrange ([`lagrange.md`](lagrange.md)) et Newton ([`newton.md`](newton.md)).

## 2. Théorème d'existence et d'unicité

> **Théorème.** Si les abscisses $t_0, t_1, \dots, t_n$ sont deux à deux distinctes, il existe **un unique** polynôme $P$ de degré au plus $n$ tel que $P(t_i) = y_i$ pour tout $i$.

**Preuve par le système linéaire.** On écrit $P(t) = a_0 + a_1 t + \dots + a_n t^n$. Les $n + 1$ conditions $P(t_i) = y_i$ forment le système $V a = y$, où $V$ est la **matrice de Vandermonde** :

$$V = \begin{pmatrix} 1 & t_0 & t_0^2 & \cdots & t_0^n \\ 1 & t_1 & t_1^2 & \cdots & t_1^n \\ \vdots & \vdots & \vdots & & \vdots \\ 1 & t_n & t_n^2 & \cdots & t_n^n \end{pmatrix}$$

Son déterminant a une formule explicite :

$$\det V = \prod_{0 \leq i < j \leq n} (t_j - t_i)$$

C'est un produit de facteurs tous non nuls, puisque les $t_i$ sont distincts. Donc $\det V \neq 0$, la matrice est inversible, et le système a une unique solution.

**Autre preuve de l'unicité.** Si $P$ et $Q$ conviennent tous les deux, $P - Q$ est un polynôme de degré au plus $n$ qui s'annule en $n + 1$ points distincts. Or un polynôme non nul de degré au plus $n$ a au plus $n$ racines. Donc $P - Q = 0$.

**Conséquence importante.** Les méthodes directe, de Lagrange et de Newton calculent **le même polynôme**. Elles diffèrent seulement par la base dans laquelle elles l'écrivent, et donc par leur coût et leur stabilité numérique.

## 3. Application à notre exemple

Avec les points $(0, 0)$, $(1, 1)$, $(2, -1)$ :

$$V = \begin{pmatrix} 1 & 0 & 0 \\ 1 & 1 & 1 \\ 1 & 2 & 4 \end{pmatrix}, \qquad \det V = (1 - 0)(2 - 0)(2 - 1) = 2 \neq 0$$

La résolution de $V a = y$ donne $a_0 = 0$, $a_1 = \frac{5}{2}$, $a_2 = -\frac{3}{2}$, soit :

$$P(t) = \frac{5}{2}\,t - \frac{3}{2}\,t^2$$

## 4. Limite : le conditionnement

Le **conditionnement** d'une matrice mesure à quel point la solution d'un système est sensible aux petites erreurs (arrondis de l'ordinateur, imprécision des données). Plus il est grand, plus les erreurs sont amplifiées.

Pour la matrice de Vandermonde, le conditionnement **augmente très vite** avec le nombre de points, surtout s'ils sont proches les uns des autres : les colonnes $t^k$ et $t^{k+1}$ finissent par se ressembler, et la matrice est « presque » non inversible. Avec quelques dizaines de points, les coefficients calculés peuvent être complètement faux, même si le système est théoriquement inversible.

Avec 3 points comme ici, aucun problème. Mais c'est la raison pour laquelle on préfère Lagrange ou Newton dès que $n$ grandit.

## 5. Coût

La résolution du système par la méthode de Gauss coûte de l'ordre de $n^3$ opérations. Une fois les coefficients connus, l'évaluation de $P$ par le schéma de Horner coûte de l'ordre de $n$ opérations.