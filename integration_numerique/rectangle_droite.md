# Rectangles à droite : fondements théoriques

Code associé : [`rectangle_droite.py`](rectangle_droite.py)

Cette méthode est le « miroir » des rectangles à gauche. Les résultats qui se démontrent de la même manière sont seulement rappelés ici ; leur preuve détaillée est dans [`rectangle_gauche.md`](rectangle_gauche.md).

## 1. Principe

On découpe $[a, b]$ en $n$ sous-intervalles de même largeur :

$$h = \frac{b - a}{n}, \qquad x_i = a + i\,h \quad (i = 0, 1, \dots, n)$$

Sur chaque sous-intervalle $[x_i, x_{i+1}]$, on remplace $f$ par la **constante** $f(x_{i+1})$, sa valeur au bord droit :

$$D_n = h \sum_{i=1}^{n} f(x_i)$$

Le premier point $x_0 = a$ n'intervient jamais.

**Lien avec les rectangles à gauche.** Les deux sommes partagent tous les points sauf les extrémités :

$$D_n = R_n + h\,\big(f(b) - f(a)\big)$$

où $R_n$ désigne la somme des rectangles à gauche. Une fois l'une calculée, l'autre s'obtient en deux opérations.

## 2. Théorème de convergence

> **Théorème.** Si $f$ est continue sur $[a, b]$, alors :
>
> $$\lim_{n \to \infty} D_n = \int_a^b f(x)\,dx$$

**Idée.** $D_n$ est elle aussi une **somme de Riemann** : la définition de l'intégrale autorise à choisir n'importe quel point dans chaque sous-intervalle. On peut aussi le voir avec la relation de la section 1 : $D_n - R_n = h\,(f(b) - f(a)) \to 0$, donc $D_n$ a la même limite que $R_n$.

## 3. Majoration de l'erreur

> **Théorème.** Si $f$ est de classe $C^1$ sur $[a, b]$ et si $M_1 = \max_{[a, b]} |f'(x)|$, alors :
>
> $$\left| D_n - \int_a^b f(x)\,dx \right| \leq \frac{(b - a)\,h}{2}\,M_1$$

**Idée de la preuve.** Identique à celle des rectangles à gauche, en mesurant l'écart à partir du bord droit : $|f(x) - f(x_{i+1})| \leq M_1\,(x_{i+1} - x)$, puis on intègre sur chaque sous-intervalle et on somme.

**Ordre de la méthode.** L'erreur est proportionnelle à $h$ : la méthode est **d'ordre 1**, comme les rectangles à gauche.

## 4. Estimation asymptotique de l'erreur

Pour $h$ petit :

$$D_n - \int_a^b f(x)\,dx \approx \frac{h}{2}\,\big(f(b) - f(a)\big)$$

**Idée.** On part de l'estimation des rectangles à gauche, $R_n - I \approx \frac{h}{2}(f(a) - f(b))$, et on ajoute $h\,(f(b) - f(a))$ grâce à la relation de la section 1 :

$$D_n - I \approx \frac{h}{2}\,\big(f(a) - f(b)\big) + h\,\big(f(b) - f(a)\big) = \frac{h}{2}\,\big(f(b) - f(a)\big)$$

**À retenir.** Les erreurs des rectangles à gauche et à droite ont **la même taille et des signes opposés**.

## 5. Signe de l'erreur

- Si $f$ est **décroissante**, le bord droit est le point le plus bas de chaque sous-intervalle : chaque rectangle reste sous la courbe et la méthode **sous-estime** l'intégrale.
- Si $f$ est **croissante**, la méthode **surestime**.
- Si $f$ est **constante**, la méthode est **exacte** (degré d'exactitude 0).

C'est exactement l'inverse des rectangles à gauche. Conséquence pratique : pour une fonction monotone, la valeur exacte est **encadrée** par les deux méthodes. Ici, $D_{10} \leq I \leq R_{10}$, soit $0{,}7146 \leq I \leq 0{,}7778$, ce qui fournit une garantie sans connaître $I$.

## 6. Application à $\displaystyle\int_0^1 e^{-x^2}\,dx$

**Valeur de référence.** $\displaystyle\int_0^1 e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}\,\operatorname{erf}(1) \approx 0{,}746824$ (pas de primitive usuelle).

**Majoration.** Comme pour les rectangles à gauche, $M_1 = \sqrt{2}\,e^{-1/2} \approx 0{,}858$.

**Signe.** $f$ est décroissante sur $[0, 1]$, donc la méthode sous-estime.

| | $n = 10$ |
|---|---:|
| Approximation $D_{10}$ | 0,714605 |
| Erreur réelle | $-3{,}22 \times 10^{-2}$ (4,31 %) |
| Estimation $\frac{h}{2}(f(1) - f(0))$ | $-3{,}16 \times 10^{-2}$ |
| Majoration $\frac{(b-a)h}{2} M_1$ | $4{,}29 \times 10^{-2}$ |

L'erreur est bien négative, reste sous la majoration, et le script montre un rapport qui tend vers 2 quand $n$ double (ordre 1).

## 7. De la moyenne des deux rectangles à la méthode des trapèzes

Puisque les erreurs à gauche et à droite sont presque opposées, leur **moyenne** les fait presque disparaître :

$$T_n = \frac{R_n + D_n}{2} = h\left[\frac{f(x_0)}{2} + f(x_1) + \dots + f(x_{n-1}) + \frac{f(x_n)}{2}\right]$$

C'est la **méthode des trapèzes** : sur chaque sous-intervalle, on remplace $f$ par le segment qui relie $f(x_i)$ à $f(x_{i+1})$.

| Méthode ($n = 10$) | Approximation | Erreur |
|---|---:|---:|
| Rectangles à gauche | 0,777817 | $+3{,}10 \times 10^{-2}$ |
| Rectangles à droite | 0,714605 | $-3{,}22 \times 10^{-2}$ |
| Moyenne (trapèzes) | 0,746211 | $-6{,}1 \times 10^{-4}$ |

L'erreur est divisée par environ 50, pour un coût identique (11 évaluations de $f$). Les termes en $h$ se compensent exactement, il ne reste qu'une erreur en $h^2$ :

$$T_n - \int_a^b f(x)\,dx \approx \frac{h^2}{12}\,\big(f'(b) - f'(a)\big)$$

Ici : $\frac{0{,}01}{12} \times (-2e^{-1} - 0) \approx -6{,}1 \times 10^{-4}$, exactement l'erreur observée. La méthode des trapèzes est **d'ordre 2**.

## 8. Limites

- **Convergence lente** (ordre 1), exactement comme les rectangles à gauche : environ 430 000 intervalles pour garantir une erreur inférieure à $10^{-6}$ sur notre exemple.
- **Asymétrie** : la méthode ignore la valeur en $a$ et favorise systématiquement le bord droit, d'où une erreur qui ne se compense pas.
- **Intérêt surtout pédagogique**, mais avec un vrai usage : associée aux rectangles à gauche, elle **encadre** l'intégrale d'une fonction monotone, et leur moyenne donne directement la méthode des trapèzes.