# Rectangles à gauche : fondements théoriques

Code associé : [`rectangle_gauche.py`](rectangle_gauche.py)

## 1. Principe

On découpe $[a, b]$ en $n$ sous-intervalles de même largeur :

$$h = \frac{b - a}{n}, \qquad x_i = a + i\,h \quad (i = 0, 1, \dots, n)$$

Sur chaque sous-intervalle $[x_i, x_{i+1}]$, on remplace $f$ par la **constante** $f(x_i)$, sa valeur au bord gauche. L'aire sous la courbe devient une somme d'aires de rectangles :

$$R_n = h \sum_{i=0}^{n-1} f(x_i)$$

Le dernier point $x_n = b$ n'intervient jamais.

**Lien avec l'interpolation.** Remplacer $f$ par une constante sur chaque sous-intervalle revient à l'interpoler par un polynôme de **degré 0** en un seul point. Simpson fera la même chose avec un polynôme de degré 2 (voir [`simpson.md`](simpson.md)).

## 2. Théorème de convergence

> **Théorème.** Si $f$ est continue sur $[a, b]$, alors :
>
> $$\lim_{n \to \infty} R_n = \int_a^b f(x)\,dx$$

**Idée.** $R_n$ est une **somme de Riemann** : c'est précisément la construction qui sert à définir l'intégrale. Quand $h$ tend vers 0, les rectangles épousent de mieux en mieux la courbe.

Ce théorème garantit la convergence, mais ne dit **rien sur la vitesse**. C'est le rôle de la majoration d'erreur.

## 3. Majoration de l'erreur

> **Théorème.** Si $f$ est de classe $C^1$ sur $[a, b]$ et si $M_1 = \max_{[a, b]} |f'(x)|$, alors :
>
> $$\left| R_n - \int_a^b f(x)\,dx \right| \leq \frac{(b - a)\,h}{2}\,M_1$$

**Idée de la preuve.**

1. Sur un sous-intervalle, d'après le théorème des accroissements finis, $|f(x) - f(x_i)| \leq M_1\,(x - x_i)$.
2. En intégrant sur $[x_i, x_{i+1}]$ : l'erreur sur ce rectangle est au plus $M_1 \displaystyle\int_{x_i}^{x_{i+1}} (x - x_i)\,dx = M_1\,\frac{h^2}{2}$.
3. Il y a $n$ rectangles, et $n\,h = b - a$ : l'erreur totale est au plus $n\,M_1\,\dfrac{h^2}{2} = \dfrac{(b - a)\,h}{2}\,M_1$.

**Ordre de la méthode.** L'erreur est proportionnelle à $h$ : la méthode est **d'ordre 1**. Doubler $n$ divise l'erreur par 2 ; multiplier $n$ par 10 la divise par 10.

## 4. Estimation asymptotique de l'erreur

La majoration précédente est souvent pessimiste. Pour $h$ petit, on a une estimation plus fine :

$$R_n - \int_a^b f(x)\,dx \approx \frac{h}{2}\,\big(f(a) - f(b)\big)$$

**Idée.** Sur chaque sous-intervalle, $f(x) - f(x_i) \approx f'(x_i)\,(x - x_i)$, donc l'erreur locale vaut environ $-f'(x_i)\,\dfrac{h^2}{2}$. En sommant, on reconnaît une somme de Riemann de $f'$ :

$$\sum_i f'(x_i)\,\frac{h^2}{2} = \frac{h}{2} \sum_i h\,f'(x_i) \approx \frac{h}{2} \int_a^b f'(x)\,dx = \frac{h}{2}\,\big(f(b) - f(a)\big)$$

**Intérêt pratique.** Cette formule donne à la fois la **taille** et le **signe** de l'erreur, sans connaître la valeur exacte de l'intégrale.

## 5. Signe de l'erreur

- Si $f$ est **décroissante**, le bord gauche est le point le plus haut de chaque sous-intervalle : chaque rectangle dépasse la courbe et la méthode **surestime** l'intégrale.
- Si $f$ est **croissante**, c'est l'inverse : la méthode **sous-estime**.
- Si $f$ est **constante**, la méthode est **exacte**. On dit que son degré d'exactitude est 0 : elle intègre exactement les polynômes de degré 0, mais pas ceux de degré 1.

## 6. Application à $\displaystyle\int_0^1 e^{-x^2}\,dx$

**Valeur de référence.** $e^{-x^2}$ n'a pas de primitive exprimable avec les fonctions usuelles. On utilise la fonction d'erreur :

$$\int_0^1 e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}\,\operatorname{erf}(1) \approx 0{,}746824$$

**Majoration.** $f'(x) = -2x\,e^{-x^2}$. Le maximum de $|f'|$ sur $[0, 1]$ est atteint en $x = \frac{1}{\sqrt{2}}$ (là où $f''$ s'annule) et vaut $M_1 = \sqrt{2}\,e^{-1/2} \approx 0{,}858$.

**Signe.** $f$ est décroissante sur $[0, 1]$, donc la méthode surestime.

| | $n = 10$ | $n = 100$ |
|---|---:|---:|
| Approximation $R_n$ | 0,777817 | 0,749979 |
| Erreur réelle | $+3{,}10 \times 10^{-2}$ | $+3{,}15 \times 10^{-3}$ |
| Estimation $\frac{h}{2}(f(0) - f(1))$ | $3{,}16 \times 10^{-2}$ | $3{,}16 \times 10^{-3}$ |
| Majoration $\frac{(b-a)h}{2} M_1$ | $4{,}29 \times 10^{-2}$ | $4{,}29 \times 10^{-3}$ |

On observe les trois résultats théoriques : l'erreur est positive (surestimation), elle reste sous la majoration, et l'estimation asymptotique devient presque exacte quand $h$ diminue.

**Coût d'une précision donnée.** Pour garantir une erreur inférieure à $10^{-6}$, il faut $\dfrac{h}{2}\,M_1 \leq 10^{-6}$, soit $n \geq$ environ **430 000** intervalles. C'est le prix d'une méthode d'ordre 1.

## 7. Variantes

| Méthode | Point utilisé sur $[x_i, x_{i+1}]$ | Ordre | Degré d'exactitude |
|---|---|---:|---:|
| Rectangles à gauche | $x_i$ | 1 | 0 |
| Rectangles à droite | $x_{i+1}$ | 1 | 0 |
| Point milieu | $\frac{x_i + x_{i+1}}{2}$ | 2 | 1 |
| Trapèzes | moyenne de $f(x_i)$ et $f(x_{i+1})$ | 2 | 1 |

Le simple fait de prendre le point **milieu** au lieu du bord gauche fait gagner un ordre : les erreurs des deux moitiés du rectangle se compensent.

## 8. Limites

- **Convergence lente** (ordre 1) : chaque chiffre exact supplémentaire coûte 10 fois plus de calculs.
- **Asymétrie** : la méthode ignore la valeur en $b$ et favorise systématiquement un côté de chaque sous-intervalle, d'où une erreur qui ne se compense pas.
- **Intérêt surtout pédagogique** : elle illustre la définition de l'intégrale, mais on lui préfère en pratique le point milieu, les trapèzes ou Simpson.