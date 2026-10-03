# Méthode de Simpson : fondements théoriques

Code associé : [`simpson.py`](simpson.py)

## 1. Principe

Les rectangles remplacent $f$ par une constante. Simpson remplace $f$, sur chaque **paire** de sous-intervalles, par la **parabole** qui passe par trois points : les deux bords et le milieu. On intègre ensuite cette parabole, ce qui se fait exactement.

C'est une application directe de l'interpolation polynomiale de degré 2 (voir [`../interpolation/lagrange.md`](../interpolation/lagrange.md)).

## 2. La formule simple sur une paire d'intervalles

Pour simplifier les calculs, on se place sur $[-h, h]$ avec les trois points $-h$, $0$ et $h$.

> **Formule de Simpson simple.**
>
> $$\int_{-h}^{h} f(x)\,dx \approx \frac{h}{3}\,\big[f(-h) + 4\,f(0) + f(h)\big]$$

**Démonstration par Lagrange.** La parabole d'interpolation s'écrit $P(x) = f(-h)\,L_0(x) + f(0)\,L_1(x) + f(h)\,L_2(x)$. Il suffit d'intégrer chaque polynôme de base :

| Polynôme de base | Expression | Intégrale sur $[-h, h]$ |
|---|---|---:|
| $L_0$ | $\dfrac{x\,(x - h)}{2h^2}$ | $\dfrac{h}{3}$ |
| $L_1$ | $\dfrac{h^2 - x^2}{h^2}$ | $\dfrac{4h}{3}$ |
| $L_2$ | $\dfrac{x\,(x + h)}{2h^2}$ | $\dfrac{h}{3}$ |

On obtient bien les poids $\frac{h}{3}$, $\frac{4h}{3}$, $\frac{h}{3}$. Le point du milieu pèse **4 fois plus** que les bords.

**Vérification rapide.** La formule doit être exacte pour $f(x) = 1$ : $\int_{-h}^{h} 1\,dx = 2h$ et $\frac{h}{3}(1 + 4 + 1) = 2h$. ✔

## 3. Degré d'exactitude : un bonus gratuit

La formule a été construite pour être exacte sur les polynômes de degré 2. En réalité, elle est exacte **jusqu'au degré 3** :

| $f(x)$ | Intégrale exacte sur $[-h, h]$ | Formule de Simpson | Exacte ? |
|---|---:|---:|:---:|
| $1$ | $2h$ | $2h$ | ✔ |
| $x$ | $0$ | $0$ | ✔ |
| $x^2$ | $\frac{2h^3}{3}$ | $\frac{h}{3}(h^2 + 0 + h^2) = \frac{2h^3}{3}$ | ✔ |
| $x^3$ | $0$ | $\frac{h}{3}(-h^3 + 0 + h^3) = 0$ | ✔ |
| $x^4$ | $\frac{2h^5}{5}$ | $\frac{2h^5}{3}$ | ✘ |

**Pourquoi.** Pour $x^3$ (et toute fonction impaire), l'intégrale sur un intervalle symétrique est nulle, et la formule aussi car ses poids sont symétriques. La symétrie fait gagner un degré « gratuitement ».

C'est ce degré d'exactitude 3 qui explique l'ordre 4 de la méthode.

## 4. La formule composite

On découpe $[a, b]$ en $n$ sous-intervalles de largeur $h = \frac{b - a}{n}$, avec **$n$ pair**, et on applique la formule simple sur chaque paire $[x_{2k}, x_{2k+2}]$. Les points $x_2, x_4, \dots$ sont partagés entre deux paires, donc comptés deux fois :

$$S_n = \frac{h}{3}\left[f(x_0) + 4\sum_{i \text{ impair}} f(x_i) + 2\sum_{\substack{i \text{ pair} \\ 0 < i < n}} f(x_i) + f(x_n)\right]$$

Les coefficients suivent le motif **1, 4, 2, 4, 2, ..., 2, 4, 1**.

**Lien avec les autres méthodes.** On peut montrer que Simpson est une moyenne pondérée de deux méthodes d'ordre 2 calculées avec des intervalles de largeur $2h$ : $S = \frac{T + 2M}{3}$, où $T$ est la méthode des trapèzes et $M$ celle du point milieu. Leurs erreurs principales sont de signes opposés et se compensent.

## 5. Théorème de l'erreur

> **Théorème.** Si $f$ est de classe $C^4$ sur $[a, b]$ et si $n$ est pair, il existe $\xi \in [a, b]$ tel que :
>
> $$S_n - \int_a^b f(x)\,dx = \frac{(b - a)\,h^4}{180}\,f^{(4)}(\xi)$$
>
> En particulier, avec $M_4 = \max_{[a, b]} |f^{(4)}(x)|$ :
>
> $$\left| S_n - \int_a^b f(x)\,dx \right| \leq \frac{(b - a)\,h^4}{180}\,M_4$$

**Idée de la preuve.** Sur une paire d'intervalles, on développe $f$ en série de Taylor autour du milieu. Comme la formule est exacte jusqu'au degré 3, tous les termes jusqu'à $x^3$ disparaissent de l'erreur. Le premier terme qui reste est celui en $x^4$, ce qui fait apparaître $f^{(4)}$ et un facteur $h^5$ par paire. En sommant sur les $\frac{n}{2}$ paires, on perd une puissance de $h$ (car $\frac{n}{2} \times h = \frac{b - a}{2}$), d'où le $h^4$ final.

**Ordre de la méthode.** L'erreur est proportionnelle à $h^4$ : la méthode est **d'ordre 4**. Doubler $n$ divise l'erreur par $2^4 = 16$ ; multiplier $n$ par 10 la divise par 10 000.

**Conséquence.** Si $f$ est un polynôme de degré au plus 3, $f^{(4)} = 0$ et Simpson est **exacte**, quel que soit $n$.

## 6. Application à $\displaystyle\int_0^1 e^{-x^2}\,dx$

**Dérivée quatrième.** En dérivant quatre fois :

$$f^{(4)}(x) = (16x^4 - 48x^2 + 12)\,e^{-x^2}$$

Sur $[0, 1]$, on compare les valeurs aux bords et au point critique intérieur (où $f^{(5)}$ s'annule, en $x \approx 0{,}96$) :

| $x$ | $f^{(4)}(x)$ |
|---:|---:|
| 0 | 12 |
| 0,96 | environ $-7{,}4$ |
| 1 | $-\frac{20}{e} \approx -7{,}36$ |

Donc $M_4 = 12$, atteint en $x = 0$.

**Résultats.**

| | $n = 10$ | $n = 100$ |
|---|---:|---:|
| Approximation $S_n$ | 0,746824948 | 0,746824132894 |
| Erreur réelle | $8{,}2 \times 10^{-7}$ | $8{,}2 \times 10^{-11}$ |
| Majoration $\frac{(b-a)h^4}{180} M_4$ | $6{,}7 \times 10^{-6}$ | $6{,}7 \times 10^{-10}$ |

L'erreur est bien divisée par 10 000 quand $n$ est multiplié par 10, et le script montre un rapport qui tend vers 16 quand $n$ double.

**Coût d'une précision donnée.** Pour garantir une erreur inférieure à $10^{-6}$, il faut :

$$\frac{h^4}{180} \times 12 \leq 10^{-6} \iff h \leq \left(1{,}5 \times 10^{-5}\right)^{1/4} \approx 0{,}062 \iff n \geq 16{,}1$$

Comme $n$ doit être pair : **$n = 18$** suffit. Les rectangles à gauche en demandent environ 430 000 (voir [`rectangle_gauche.md`](rectangle_gauche.md), section 6).

## 7. Comparaison avec les rectangles à gauche

| | Rectangles à gauche | Simpson |
|---|---|---|
| Approximation locale de $f$ | constante (degré 0) | parabole (degré 2) |
| Degré d'exactitude | 0 | 3 |
| Ordre | 1 | 4 |
| Régularité requise pour la majoration | $C^1$ | $C^4$ |
| $n$ pour une erreur $< 10^{-6}$ (ici) | environ 430 000 | 18 |
| Contrainte sur $n$ | aucune | $n$ pair |

## 8. Limites

- **$n$ doit être pair**, puisqu'on travaille par paires d'intervalles.
- **La fonction doit être régulière.** La majoration suppose $f$ de classe $C^4$. Si $f$ a un point anguleux ou une dérivée infinie (comme $\sqrt{x}$ en 0), la méthode converge toujours, mais l'ordre 4 est perdu.
- **Fonctions très oscillantes.** Si $f$ varie beaucoup à l'échelle de $h$, la parabole l'approche mal. Il faut alors réduire $h$ là où c'est nécessaire, ce que font les méthodes **adaptatives** : elles raffinent automatiquement le découpage là où l'erreur estimée est grande.
- **Données tabulées.** Si on ne dispose que de mesures à pas constant (et non de la fonction $f$), on ne peut pas augmenter $n$ à volonté, et il faut que leur nombre soit adapté (un nombre impair de points).