# Point fixe : fondements théoriques

Code associé : [`point_fixe.py`](point_fixe.py)

## 1. Définitions

**Point fixe.** On dit que $\alpha$ est un point fixe de $g$ si $g(\alpha) = \alpha$. Résoudre $f(x) = 0$ revient à trouver un point fixe d'une fonction $g$ bien choisie, par exemple $g(x) = x - f(x)$ ou toute autre réécriture équivalente.

**Fonction contractante.** $g$ est **contractante** sur $[a, b]$ s'il existe une constante $k < 1$ telle que :

$$|g(x) - g(y)| \leq k\,|x - y| \quad \text{pour tous } x, y \in [a, b]$$

Autrement dit, $g$ rapproche les points les uns des autres d'au moins un facteur $k$.

**Lien avec la dérivée.** Si $g$ est dérivable et $|g'(x)| \leq k < 1$ sur $[a, b]$, alors $g$ est contractante de rapport $k$. C'est une conséquence directe du théorème des accroissements finis : $g(x) - g(y) = g'(c)(x - y)$ pour un certain $c$ entre $x$ et $y$. En pratique, c'est ainsi qu'on vérifie la contraction.

## 2. Théorème du point fixe

> **Théorème.** Soit $g : [a, b] \to [a, b]$ une fonction **contractante** de rapport $k < 1$. Alors :
>
> 1. $g$ admet un **unique** point fixe $\alpha$ dans $[a, b]$ ;
> 2. pour **tout** $x_0 \in [a, b]$, la suite $x_{n+1} = g(x_n)$ converge vers $\alpha$ ;
> 3. on dispose des majorations d'erreur suivantes :
>
> $$\text{a priori : } |x_n - \alpha| \leq k^n\,|x_0 - \alpha| \leq k^n\,(b - a)$$
>
> $$\text{a posteriori : } |x_n - \alpha| \leq \frac{k}{1 - k}\,|x_n - x_{n-1}|$$

Les deux hypothèses sont indispensables : $g$ doit **envoyer $[a, b]$ dans lui-même** (sinon les itérés peuvent sortir de l'intervalle) et être **contractante**.

**Idée de la preuve.**

- **Existence.** On pose $h(x) = g(x) - x$. Comme $g(a) \geq a$ et $g(b) \leq b$, on a $h(a) \geq 0$ et $h(b) \leq 0$. Par le théorème des valeurs intermédiaires, $h$ s'annule, donc $g$ a un point fixe.
- **Unicité.** Si $\alpha$ et $\beta$ sont deux points fixes : $|\alpha - \beta| = |g(\alpha) - g(\beta)| \leq k\,|\alpha - \beta|$. Comme $k < 1$, cela force $|\alpha - \beta| = 0$.
- **Convergence.** $|x_{n+1} - \alpha| = |g(x_n) - g(\alpha)| \leq k\,|x_n - \alpha|$. L'erreur est multipliée par au plus $k$ à chaque étape, d'où $|x_n - \alpha| \leq k^n\,|x_0 - \alpha| \to 0$.
- **Majoration a posteriori.** $|x_n - \alpha| \leq k\,|x_{n-1} - \alpha| \leq k\left(|x_{n-1} - x_n| + |x_n - \alpha|\right)$. On regroupe les termes en $|x_n - \alpha|$ : $(1 - k)\,|x_n - \alpha| \leq k\,|x_n - x_{n-1}|$.

**Intérêt de la majoration a posteriori.** Elle ne fait intervenir que des quantités **calculables** (deux itérés successifs), contrairement à $|x_n - \alpha|$ qui dépend de la racine inconnue. C'est elle qu'utilise le script comme critère d'arrêt.

## 3. Critère local : point attractif ou répulsif

Quand on ne sait pas vérifier la contraction sur tout un intervalle, on regarde la dérivée **au point fixe** (supposée continue) :

| Valeur de $\lvert g'(\alpha) \rvert$ | Nature du point fixe | Comportement |
|---|---|---|
| $< 1$ | attractif | converge si $x_0$ est assez proche de $\alpha$ |
| $> 1$ | répulsif | les itérés s'éloignent de $\alpha$ |
| $= 1$ | cas douteux | on ne peut pas conclure |

**Signe de $g'(\alpha)$.** Si $g'(\alpha) > 0$, les itérés approchent $\alpha$ d'un seul côté (convergence monotone). Si $g'(\alpha) < 0$, ils sautent d'un côté à l'autre (convergence alternée).

## 4. Ordre de convergence

Près de $\alpha$, on a $x_{n+1} - \alpha = g(x_n) - g(\alpha) \approx g'(\alpha)\,(x_n - \alpha)$. Donc :

- si $0 < |g'(\alpha)| < 1$ : convergence **linéaire** de rapport $|g'(\alpha)|$ ;
- si $g'(\alpha) = 0$ (et $g$ de classe $C^2$) : convergence **au moins quadratique**. C'est exactement le cas de la méthode de Newton (voir [`newton.md`](newton.md)).

## 5. Application à $x^3 - 2 = 0$

On choisit $g(x) = \sqrt{\dfrac{2}{x}}$ sur $[1, 2]$.

- **Stabilité de l'intervalle.** $g$ est décroissante, $g(1) = \sqrt{2} \approx 1{,}414$ et $g(2) = 1$, donc $g([1, 2]) = [1, \sqrt{2}] \subset [1, 2]$.
- **Contraction.** $g'(x) = -\dfrac{\sqrt{2}}{2}\,x^{-3/2}$, donc $|g'(x)| \leq |g'(1)| = \dfrac{\sqrt{2}}{2} = k \approx 0{,}707 < 1$.

Le théorème s'applique : convergence pour tout $x_0 \in [1, 2]$.

**Vitesse réelle.** Au point fixe $\alpha = 2^{1/3}$, on a $\alpha^{3/2} = \sqrt{2}$, donc $g'(\alpha) = -\dfrac{1}{2}$. Deux conséquences visibles dans le tableau du script :

- la convergence est **alternée** (car $g'(\alpha) < 0$) : 1,414 puis 1,189 puis 1,297...
- l'écart entre deux itérés est à peu près divisé par **2** à chaque étape (et non par $1/0{,}707$) : $k$ est une majoration valable sur tout l'intervalle, tandis que $|g'(\alpha)| = 0{,}5$ décrit le comportement près de la racine.

**Contre-exemple.** La réécriture $g(x) = \dfrac{2}{x^2}$ a les mêmes points fixes, mais $g'(x) = -\dfrac{4}{x^3}$ donne $g'(\alpha) = -2$. Le point fixe est répulsif : la suite diverge.

## 6. Limites

- **Le choix de $g$ est tout le problème.** Une même équation admet une infinité de réécritures $x = g(x)$, et le théorème ne dit pas comment trouver la bonne.
- **Convergence linéaire** dans le cas général, donc lente si $|g'(\alpha)|$ est proche de 1.
- **Hypothèses à vérifier** sur tout l'intervalle (stabilité et contraction), ce qui n'est pas toujours facile.