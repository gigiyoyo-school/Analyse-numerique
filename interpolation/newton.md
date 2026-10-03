# Interpolation de Newton : fondements théoriques

Code associé : [`newton.py`](newton.py)

## 1. La base de Newton

Au lieu de la base $1, t, t^2, \dots$ (méthode directe) ou des $L_i$ (Lagrange), on utilise les polynômes :

$$\omega_0(t) = 1, \quad \omega_1(t) = (t - t_0), \quad \omega_2(t) = (t - t_0)(t - t_1), \quad \dots, \quad \omega_k(t) = \prod_{j=0}^{k-1} (t - t_j)$$

et on cherche le polynôme d'interpolation sous la forme :

$$P(t) = c_0 + c_1\,\omega_1(t) + c_2\,\omega_2(t) + \dots + c_n\,\omega_n(t)$$

**Pourquoi cette base est pratique.** $\omega_k$ s'annule en $t_0, \dots, t_{k-1}$. En écrivant $P(t_0) = y_0$, puis $P(t_1) = y_1$, etc., chaque nouvelle équation ne fait apparaître qu'**une seule nouvelle inconnue**. Le système est triangulaire, donc facile à résoudre de proche en proche.

## 2. Les différences divisées

Les coefficients $c_k$ se calculent par une récurrence appelée **différences divisées** :

$$f[t_i] = y_i$$

$$f[t_i, \dots, t_{i+k}] = \frac{f[t_{i+1}, \dots, t_{i+k}] - f[t_i, \dots, t_{i+k-1}]}{t_{i+k} - t_i}$$

On les range dans un tableau triangulaire : chaque colonne se calcule à partir de la précédente.

## 3. Théorème : formule de Newton

> **Théorème.** Le polynôme d'interpolation des points $(t_i, y_i)$ s'écrit :
>
> $$P(t) = \sum_{k=0}^{n} f[t_0, \dots, t_k]\;\omega_k(t)$$
>
> Autrement dit, $c_k = f[t_0, \dots, t_k]$ : ce sont les coefficients de la **première ligne** du tableau des différences divisées.

**Idée de la preuve (par récurrence).** Notons $P_k$ le polynôme qui interpole les $k + 1$ premiers points.

1. $P_k - P_{k-1}$ est de degré au plus $k$ et s'annule en $t_0, \dots, t_{k-1}$ (les deux polynômes y prennent les mêmes valeurs). Il est donc de la forme $c_k\,\omega_k(t)$, où $c_k$ est le coefficient de $t^k$ dans $P_k$.
2. On montre que ce coefficient dominant vérifie la récurrence des différences divisées. Pour cela, on utilise la relation suivante, où $Q$ interpole les points $t_1, \dots, t_k$ et $R$ les points $t_0, \dots, t_{k-1}$ :
$$P_k(t) = \frac{(t - t_0)\,Q(t) - (t - t_k)\,R(t)}{t_k - t_0}$$
On vérifie facilement qu'elle donne les bonnes valeurs en chaque $t_i$. En comparant les coefficients de $t^k$ des deux côtés, on retrouve exactement la formule de récurrence de la section 2.

## 4. Propriétés des différences divisées

**Symétrie.** $f[t_0, \dots, t_k]$ ne dépend pas de l'ordre des points : c'est le coefficient dominant du polynôme qui interpole ces points, et ce polynôme ne dépend pas de l'ordre dans lequel on les donne.

**Lien avec les dérivées.** Si $y_i = f(t_i)$ avec $f$ de classe $C^k$, il existe $\xi$ entre le plus petit et le plus grand des $t_i$ tel que :

$$f[t_0, \dots, t_k] = \frac{f^{(k)}(\xi)}{k!}$$

Les différences divisées sont donc des « dérivées discrètes ». À l'ordre 1, on reconnaît le taux d'accroissement $\frac{f(t_1) - f(t_0)}{t_1 - t_0}$.

**Lien avec l'erreur d'interpolation.** On peut réécrire l'erreur (voir [`lagrange.md`](lagrange.md), section 4) sous la forme :

$$f(x) - P(x) = f[t_0, \dots, t_n, x]\;\omega_{n+1}(x)$$

C'est le terme qu'on ajouterait à $P$ si on rajoutait $x$ comme nouveau point d'interpolation.

## 5. Avantage principal : ajouter un point

> **Propriété.** Si on ajoute un point $(t_{n+1}, y_{n+1})$, le nouveau polynôme est :
>
> $$P_{n+1}(t) = P_n(t) + f[t_0, \dots, t_{n+1}]\;\omega_{n+1}(t)$$

Les coefficients $c_0, \dots, c_n$ déjà calculés **restent valables**. Il suffit de calculer une nouvelle diagonale du tableau. Avec Lagrange, il faudrait tout recommencer.

**Illustration (point hypothétique).** Ajoutons le point $(3, 2)$ à notre exemple. On complète le tableau :

| $t_i$ | Ordre 0 | Ordre 1 | Ordre 2 | Ordre 3 |
|---:|---:|---:|---:|---:|
| 0 | **0** | **1** | **−1,5** | **4/3** |
| 1 | 1 | −2 | 2,5 | |
| 2 | −1 | 3 | | |
| 3 | 2 | | | |

Seule la dernière diagonale est nouvelle. Le polynôme devient :

$$P_3(t) = \underbrace{t - \frac{3}{2}\,t(t-1)}_{P_2(t)\ \text{inchangé}} + \frac{4}{3}\,t(t-1)(t-2)$$

Vérification : $P_3(3) = (7{,}5 - 13{,}5) + \frac{4}{3} \times 6 = -6 + 8 = 2$.

## 6. Évaluation par le schéma de Horner

La forme de Newton se factorise naturellement :

$$P(t) = c_0 + (t - t_0)\Big(c_1 + (t - t_1)\big(c_2 + \dots + (t - t_{n-1})\,c_n\big)\Big)$$

On évalue en partant de l'intérieur : $n$ multiplications et $2n$ additions, soit un coût de l'ordre de $n$ opérations. Le calcul du tableau des différences divisées, lui, coûte de l'ordre de $n^2$ opérations, et on le fait une seule fois.

**Application.** En $t = 0{,}5$ avec $c_0 = 0$, $c_1 = 1$, $c_2 = -1{,}5$ :

- intérieur : $1 + (0{,}5 - 1) \times (-1{,}5) = 1{,}75$ ;
- extérieur : $0 + (0{,}5 - 0) \times 1{,}75 = 0{,}875$.

## 7. Bilan

| | Directe | Lagrange | Newton |
|---|---|---|---|
| Calcul des coefficients | système, coût en $n^3$ | aucun | tableau, coût en $n^2$ |
| Évaluation de $P(x)$ | Horner, coût en $n$ | coût en $n^2$ | Horner, coût en $n$ |
| Ajout d'un point | tout recalculer | tout recalculer | une diagonale de plus |
| Stabilité numérique | mauvaise si $n$ grand | bonne | bonne |