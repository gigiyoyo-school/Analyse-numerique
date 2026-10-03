# Méthode de Newton : fondements théoriques

Code associé : [`newton.py`](newton.py)

## 1. Construction géométrique

Au point $x_n$, on remplace la courbe de $f$ par sa **tangente** :

$$y = f(x_n) + f'(x_n)\,(x - x_n)$$

On prend comme nouvel itéré l'abscisse où cette tangente coupe l'axe ($y = 0$) :

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

La formule n'a de sens que si $f'(x_n) \neq 0$ : une tangente horizontale ne coupe jamais l'axe.

## 2. Newton est une méthode de point fixe

La méthode s'écrit $x_{n+1} = g(x_n)$ avec :

$$g(x) = x - \frac{f(x)}{f'(x)} \qquad \text{et} \qquad g'(x) = \frac{f(x)\,f''(x)}{f'(x)^2}$$

Au niveau de la racine, $f(\alpha) = 0$, donc **$g'(\alpha) = 0$** dès que $f'(\alpha) \neq 0$.

D'après le résultat sur l'ordre de convergence du point fixe (voir [`point_fixe.md`](point_fixe.md), section 4), une dérivée nulle au point fixe donne une convergence au moins quadratique. C'est l'explication profonde de la rapidité de Newton : la fonction $g$ est construite pour être « parfaitement contractante » près de la racine.

## 3. Théorème de convergence locale

> **Théorème.** Soit $f$ de classe $C^2$ au voisinage d'une racine $\alpha$, avec $f'(\alpha) \neq 0$ (racine **simple**). Alors il existe un voisinage de $\alpha$ tel que, pour tout $x_0$ dans ce voisinage, la suite de Newton converge vers $\alpha$, et la convergence est **quadratique** :
>
> $$|x_{n+1} - \alpha| \approx \frac{|f''(\alpha)|}{2\,|f'(\alpha)|}\,|x_n - \alpha|^2$$

**Idée de la preuve.** On écrit la formule de Taylor à l'ordre 2 de $f$ autour de $x_n$, évaluée en $\alpha$ :

$$0 = f(\alpha) = f(x_n) + f'(x_n)\,(\alpha - x_n) + \frac{f''(\xi_n)}{2}\,(\alpha - x_n)^2$$

pour un certain $\xi_n$ entre $x_n$ et $\alpha$. On divise par $f'(x_n)$ et on utilise la définition de $x_{n+1}$ :

$$x_{n+1} - \alpha = \frac{f''(\xi_n)}{2\,f'(x_n)}\,(x_n - \alpha)^2$$

L'erreur suivante est proportionnelle au **carré** de l'erreur actuelle.

**Ce que cela signifie concrètement.** Si l'erreur vaut $10^{-2}$, la suivante est de l'ordre de $10^{-4}$, puis $10^{-8}$ : le nombre de chiffres exacts double environ à chaque itération.

**Application.** Pour $f(x) = x^3 - 2$ : $f'(\alpha) = 3\alpha^2$ et $f''(\alpha) = 6\alpha$, donc la constante vaut $\frac{6\alpha}{2 \cdot 3\alpha^2} = \frac{1}{\alpha} \approx 0{,}794$. On le vérifie sur les itérés du script : avec une erreur de $0{,}0364$ à l'itération 2, on prévoit $0{,}794 \times 0{,}0364^2 \approx 0{,}0011$ à l'itération 3, et on observe $0{,}0010$.

**Limite du théorème.** Il est **local** : il affirme qu'un « bon voisinage » existe, sans dire comment le trouver. C'est ce que règle le théorème suivant.

## 4. Théorème de Fourier (convergence garantie sur un intervalle)

> **Théorème.** Soit $f$ de classe $C^2$ sur $[a, b]$ telle que :
>
> 1. $f(a) \cdot f(b) < 0$ ;
> 2. $f'$ ne s'annule pas sur $[a, b]$ ;
> 3. $f''$ ne s'annule pas sur $[a, b]$ (pas de point d'inflexion).
>
> Si $x_0 \in [a, b]$ vérifie $f(x_0) \cdot f''(x_0) > 0$, alors la suite de Newton est **monotone** et converge vers l'unique racine $\alpha$ de $f$ dans $[a, b]$.

**Idée.** Prenons le cas $f' > 0$ et $f'' > 0$ (fonction croissante et convexe). Une fonction convexe est toujours **au-dessus de ses tangentes**. Si on part à droite de la racine ($f(x_0) > 0$), la tangente coupe l'axe entre $\alpha$ et $x_0$ : on se rapproche sans jamais dépasser. La suite est décroissante et minorée par $\alpha$, donc elle converge, et sa limite ne peut être que $\alpha$.

**Application.** Pour $f(x) = x^3 - 2$ sur $[1, 2]$ : $f(1) \cdot f(2) < 0$, $f'(x) = 3x^2 > 0$ et $f''(x) = 6x > 0$.

- $x_0 = 2$ : $f(2) \cdot f''(2) = 6 \times 12 > 0$. La condition est remplie, et le script montre bien une suite décroissante : 2 ; 1,5 ; 1,296 ; 1,2609 ; 1,2599.
- $x_0 = 1$ : $f(1) \cdot f''(1) = -6 < 0$. La condition n'est pas remplie. Ici, le premier pas « dépasse » la racine ($x_1 = \frac{4}{3} \approx 1{,}333 > \alpha$), puis la suite redevient monotone. La condition de Fourier est **suffisante**, pas nécessaire : ne pas la respecter n'entraîne pas forcément une divergence, mais on perd la garantie.

## 5. Justification du critère d'arrêt

Le script s'arrête quand $|x_{n+1} - x_n| < \varepsilon$. Grâce à la convergence quadratique, $x_{n+1}$ est beaucoup plus proche de $\alpha$ que $x_n$, donc :

$$|x_n - \alpha| \approx |x_n - x_{n+1}|$$

L'écart entre deux itérés est une bonne estimation de l'erreur sur $x_n$, et l'erreur sur $x_{n+1}$ est de l'ordre de son carré. C'est pourquoi on obtient une erreur de $8 \times 10^{-7}$ alors qu'on demandait seulement $10^{-2}$.

## 6. Limites

- **Racine multiple** ($f'(\alpha) = 0$). La convergence devient seulement linéaire. Pour une racine de multiplicité $m$, le rapport vaut $1 - \frac{1}{m}$.
- **Tangente horizontale.** Si $f'(x_n) = 0$ en cours de route, la méthode s'arrête (division par zéro). Le script lève une erreur dans ce cas.
- **Mauvais point de départ.** Loin de la racine, les itérés peuvent partir très loin ou tourner en boucle. Exemple classique : $f(x) = x^3 - 2x + 2$ avec $x_0 = 0$ donne $x_1 = 1$, puis $x_2 = 0$, et ainsi de suite indéfiniment.
- **Il faut connaître $f'$**, ce qui n'est pas toujours possible ou pratique.