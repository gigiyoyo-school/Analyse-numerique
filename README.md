# Analyse numérique

Présentation, en Python, des principales méthodes d'analyse numérique vues en cours, chacune illustrée par un exemple complet dont toutes les itérations sont affichées dans un tableau.

Le projet couvre trois chapitres :

1. la **résolution d'équations non linéaires** $f(x) = 0$, cœur du projet ;
2. l'**interpolation polynomiale** ;
3. l'**intégration numérique**.

Chaque méthode est accompagnée d'une **fiche théorique** (fichier `.md` du même nom) qui énonce et démontre les théorèmes sur lesquels elle repose.

## Sommaire

- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Lancer un exemple](#lancer-un-exemple)
- [Partie 1 : équations non linéaires](#partie-1--équations-non-linéaires)
  - [Méthode de dichotomie](#méthode-de-dichotomie)
  - [Méthode du point fixe](#méthode-du-point-fixe)
  - [Méthode de Newton](#méthode-de-newton)
  - [Comparaison des trois méthodes](#comparaison-des-trois-méthodes)
- [Partie 2 : interpolation polynomiale](#partie-2--interpolation-polynomiale)
- [Partie 3 : intégration numérique](#partie-3--intégration-numérique)
  - [Méthode des rectangles à gauche](#méthode-des-rectangles-à-gauche)
  - [Méthode des rectangles à droite](#méthode-des-rectangles-à-droite)
  - [Méthode de Simpson](#méthode-de-simpson)
  - [Comparaison des méthodes d'intégration](#comparaison-des-méthodes-dintégration)

## Structure du projet

```
analyse-numerique/
├── README.md
├── pyproject.toml              # dépendances (numpy, rich)
├── equations_non_lineaires/    # Partie 1 : résoudre f(x) = 0
│   ├── __init__.py
│   ├── dichotomie.py           # code et exemple
│   ├── dichotomie.md           # fiche théorique
│   ├── point_fixe.py
│   ├── point_fixe.md
│   ├── newton.py
│   └── newton.md
├── interpolation/              # Partie 2 : polynôme passant par des points donnés
│   ├── __init__.py
│   ├── directe.py              # système de Vandermonde
│   ├── directe.md
│   ├── lagrange.py
│   ├── lagrange.md
│   ├── newton.py               # différences divisées
│   └── newton.md
└── integration_numerique/      # Partie 3 : approcher une intégrale
    ├── __init__.py
    ├── rectangle_gauche.py
    ├── rectangle_gauche.md
    ├── rectangle_droite.py
    ├── rectangle_droite.md
    ├── simpson.py
    └── simpson.md
```

Chaque fichier `.py` contient la méthode, l'exemple et l'affichage des résultats. Il est autonome, à une exception près : `rectangle_droite.py` réutilise la fonction de `rectangle_gauche.py` pour comparer les deux méthodes. Le fichier `.md` du même nom en donne les fondements théoriques (théorèmes, idées de preuve, limites).

Les fichiers `__init__.py` déclarent explicitement chaque dossier comme un paquet Python. Les deux fichiers `newton.py` ne se gênent donc pas : l'un est `equations_non_lineaires.newton`, l'autre `interpolation.newton`.

## Installation

Le projet utilise Python 3.14 et [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Dépendances : `numpy` (calcul matriciel) et `rich` (tableaux colorés dans le terminal).

## Lancer un exemple

Depuis la racine du projet, on lance un fichier comme un module (`dossier.fichier`, sans `.py`).

Partie 1 :

```bash
uv run python -m equations_non_lineaires.dichotomie
```

```bash
uv run python -m equations_non_lineaires.point_fixe
```

```bash
uv run python -m equations_non_lineaires.newton
```

Partie 2 :

```bash
uv run python -m interpolation.directe
```

```bash
uv run python -m interpolation.lagrange
```

```bash
uv run python -m interpolation.newton
```

Partie 3 :

```bash
uv run python -m integration_numerique.rectangle_gauche
```

```bash
uv run python -m integration_numerique.rectangle_droite
```

```bash
uv run python -m integration_numerique.simpson
```

---

## Partie 1 : équations non linéaires

### Le problème commun

Les trois méthodes résolvent la **même équation**, ce qui permet de les comparer :

$$f(x) = x^3 - 2 = 0 \quad \text{sur } [1, 2], \qquad \text{précision } \varepsilon = 0{,}01$$

La solution exacte est $\alpha = \sqrt[3]{2} \approx 1{,}259921$. Elle existe et est unique sur $[1, 2]$ car $f(1) = -1 < 0$, $f(2) = 6 > 0$ et $f$ est strictement croissante ($f'(x) = 3x^2 > 0$).

### Méthode de dichotomie

Code : [`dichotomie.py`](equations_non_lineaires/dichotomie.py) | Théorie : [`dichotomie.md`](equations_non_lineaires/dichotomie.md)

**Principe.** Si $f$ est continue et $f(a) \cdot f(b) < 0$, une racine se trouve dans $[a, b]$ (théorème des valeurs intermédiaires). On calcule le milieu $m = \frac{a+b}{2}$ et on garde la moitié de l'intervalle où $f$ change de signe :

- si $f(a) \cdot f(m) < 0$, la racine est dans $[a, m]$ ;
- sinon, elle est dans $[m, b]$.

**Critère d'arrêt.** Après $n$ itérations, l'erreur sur le milieu est au plus $\frac{b-a}{2^n}$. On s'arrête quand cette borne passe sous $\varepsilon$. Le nombre d'itérations est donc **connu à l'avance** :

$$n \geq \log_2\left(\frac{b-a}{\varepsilon}\right) = \log_2(100) \approx 6{,}64 \quad \Rightarrow \quad n = 7$$

**Résultat.** $x \approx 1{,}2578$ en **7 itérations** (erreur réelle : $2{,}1 \times 10^{-3}$).

**À retenir.** Convergence toujours garantie dès que $f(a) \cdot f(b) < 0$, mais lente : on gagne un chiffre binaire par itération (convergence linéaire de rapport $\frac{1}{2}$).

### Méthode du point fixe

Code : [`point_fixe.py`](equations_non_lineaires/point_fixe.py) | Théorie : [`point_fixe.md`](equations_non_lineaires/point_fixe.md)

**Principe.** On réécrit $f(x) = 0$ sous la forme $x = g(x)$, puis on itère $x_{n+1} = g(x_n)$. Ici :

$$x^3 = 2 \iff x^2 = \frac{2}{x} \iff x = g(x) = \sqrt{\frac{2}{x}}$$

**Condition de convergence.** La suite converge si $g$ est **contractante** sur $[1, 2]$ :

- $g$ envoie $[1, 2]$ dans lui-même : $g([1, 2]) = [1, \sqrt{2}] \subset [1, 2]$ ;
- $|g'(x)| = \frac{\sqrt{2}}{2\, x^{3/2}} \leq k = \frac{\sqrt{2}}{2} \approx 0{,}707 < 1$.

Le choix de $g$ est déterminant : la réécriture $x = \frac{2}{x^2}$, pourtant équivalente, donne $|g'(\alpha)| = 2 > 1$ et diverge.

**Critère d'arrêt.** On utilise la majoration de l'erreur :

$$|x_n - \alpha| \leq \frac{k}{1-k}\,|x_n - x_{n-1}| < \varepsilon$$

**Résultat.** $x \approx 1{,}2588$ en **8 itérations** à partir de $x_0 = 1$ (erreur réelle : $1{,}1 \times 10^{-3}$).

**À retenir.** Convergence linéaire, d'autant plus rapide que $k$ est petit. Toute la difficulté est de trouver une bonne fonction $g$.

### Méthode de Newton

Code : [`newton.py`](equations_non_lineaires/newton.py) | Théorie : [`newton.md`](equations_non_lineaires/newton.md)

**Principe.** On remplace la courbe par sa tangente au point $x_n$ et on prend l'intersection de cette tangente avec l'axe des abscisses :

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} = x_n - \frac{x_n^3 - 2}{3x_n^2}$$

**Condition de convergence (Fourier).** Si $f(a) \cdot f(b) < 0$, si $f'$ et $f''$ ne s'annulent pas sur $[a, b]$ et si le point de départ $x_0 \in [a, b]$ vérifie $f(x_0) \cdot f''(x_0) > 0$, la suite converge de façon monotone. Avec $x_0 = 2$ : $f(2) = 6 > 0$ et $f''(2) = 12 > 0$. Le programme vérifie la dernière condition et affiche un avertissement si $f(x_0) \cdot f''(x_0) \leq 0$.

**Critère d'arrêt.** $|x_{n+1} - x_n| < \varepsilon$.

**Résultat.** $x \approx 1{,}259922$ en **4 itérations** (erreur réelle : $8{,}1 \times 10^{-7}$).

**À retenir.** Convergence quadratique : le nombre de chiffres exacts double à peu près à chaque itération. En contrepartie, il faut connaître $f'$ et partir assez près de la racine ; la méthode échoue si $f'(x_n) = 0$ (tangente horizontale).

### Comparaison des trois méthodes

Même équation, même précision demandée ($\varepsilon = 0{,}01$) :

| Méthode | Départ | Itérations | Racine approchée | Erreur réelle | Convergence |
|---|---|---:|---:|---:|---|
| Dichotomie | $[1, 2]$ | 7 | 1,2578 | $2{,}1 \times 10^{-3}$ | linéaire, toujours garantie |
| Point fixe | $x_0 = 1$ | 8 | 1,2588 | $1{,}1 \times 10^{-3}$ | linéaire, si $g$ contractante |
| Newton | $x_0 = 2$ | 4 | 1,259922 | $8{,}1 \times 10^{-7}$ | quadratique, si bon départ |

Newton est de loin la plus rapide et la plus précise ; la dichotomie est la plus robuste. En pratique, on combine souvent les deux : quelques itérations de dichotomie pour s'approcher de la racine, puis Newton pour converger vite.

> Les critères d'arrêt ne sont pas identiques (borne d'erreur pour la dichotomie et le point fixe, écart entre deux itérés pour Newton). Si Newton dépasse largement la précision demandée, c'est grâce à sa convergence quadratique : au moment où l'écart entre deux itérés passe sous $\varepsilon$, l'erreur sur le dernier itéré est déjà de l'ordre du carré de cet écart.

---

## Partie 2 : interpolation polynomiale

On cherche le polynôme $P$ de degré au plus 2 qui passe par les trois points :

| $t_i$ | 0 | 1 | 2 |
|---|---:|---:|---:|
| $y_i$ | 0 | 1 | −1 |

Les trois méthodes donnent **le même polynôme** (il est unique), écrit dans trois bases différentes :

$$P(t) = \frac{5}{2}\,t - \frac{3}{2}\,t^2, \qquad P(0{,}5) = 0{,}875, \qquad P(1{,}5) = 0{,}375$$

| Méthode | Code | Théorie | Idée |
|---|---|---|---|
| Directe | [`directe.py`](interpolation/directe.py) | [`directe.md`](interpolation/directe.md) | On écrit $P(t) = a_0 + a_1 t + a_2 t^2$ et on résout le système de Vandermonde $V a = y$. |
| Lagrange | [`lagrange.py`](interpolation/lagrange.py) | [`lagrange.md`](interpolation/lagrange.md) | $P(x) = \sum_i y_i\, L_i(x)$ avec $L_i(x) = \prod_{j \neq i} \frac{x - t_j}{t_i - t_j}$. Aucun système à résoudre. |
| Newton | [`newton.py`](interpolation/newton.py) | [`newton.md`](interpolation/newton.md) | Coefficients obtenus par le tableau des différences divisées, évaluation par le schéma de Horner. Ajouter un point ne remet pas en cause les calculs déjà faits. |

**Pourquoi trois méthodes ?** La méthode directe est la plus intuitive, mais la matrice de Vandermonde devient **mal conditionnée** quand le nombre de points augmente : de petites erreurs d'arrondi produisent de grandes erreurs sur les coefficients. Lagrange évite le système linéaire, mais tous les $L_i$ changent dès qu'on ajoute un point. Newton cumule les deux avantages, ce qui en fait souvent la méthode préférée en pratique.

La fiche [`directe.md`](interpolation/directe.md) démontre le théorème d'existence et d'unicité commun aux trois méthodes ; [`lagrange.md`](interpolation/lagrange.md) traite aussi de l'erreur d'interpolation et du phénomène de Runge.

---

## Partie 3 : intégration numérique

### Le problème commun

Toutes les méthodes approchent la **même intégrale** :

$$I = \int_0^1 e^{-x^2}\,dx$$

La fonction $e^{-x^2}$ n'a pas de primitive qui s'exprime avec les fonctions usuelles : c'est précisément le cas où l'on a besoin d'une méthode numérique. La valeur exacte, qui sert de référence, s'écrit avec la fonction d'erreur :

$$I = \frac{\sqrt{\pi}}{2}\,\mathrm{erf}(1) \approx 0{,}746824132812$$

Dans toutes les méthodes, on découpe $[a, b]$ en $n$ sous-intervalles de même largeur $h = \frac{b-a}{n}$, de bornes $x_i = a + i\,h$.

### Méthode des rectangles à gauche

Code : [`rectangle_gauche.py`](integration_numerique/rectangle_gauche.py) | Théorie : [`rectangle_gauche.md`](integration_numerique/rectangle_gauche.md)

**Principe.** Sur chaque sous-intervalle, on remplace $f$ par la constante $f(x_i)$, sa valeur au **bord gauche**. L'aire sous la courbe devient une somme d'aires de rectangles :

$$I \approx h\,\big[f(x_0) + f(x_1) + \dots + f(x_{n-1})\big]$$

Le point $x_n = b$ n'est pas utilisé.

**Erreur.** Si $f$ est dérivable :

$$|E| \leq \frac{(b-a)\,h}{2}\,\max_{[a,b]} |f'|, \qquad E \approx \frac{h}{2}\,\big(f(a) - f(b)\big)$$

Ici $\max |f'| = \sqrt{2}\,e^{-1/2} \approx 0{,}858$, atteint en $x = \frac{1}{\sqrt{2}}$. Comme $f$ est décroissante, chaque rectangle dépasse la courbe : la méthode **surestime** l'intégrale.

**Résultat** avec $n = 1000$ : $I \approx 0{,}747140$, erreur $+3{,}16 \times 10^{-4}$, sous la borne théorique ($4{,}29 \times 10^{-4}$). L'estimation $\frac{h}{2}(f(a) - f(b))$ donne exactement l'erreur observée.

**À retenir.** Méthode d'**ordre 1** : l'erreur est proportionnelle à $h$. Quand on double $n$, l'erreur est divisée par 2 (le script affiche des rapports de 1,98 à 2,00). Il faut beaucoup de points pour une bonne précision : environ 430 000 sous-intervalles pour garantir une erreur inférieure à $10^{-6}$.

### Méthode des rectangles à droite

Code : [`rectangle_droite.py`](integration_numerique/rectangle_droite.py) | Théorie : [`rectangle_droite.md`](integration_numerique/rectangle_droite.md)

**Principe.** C'est le miroir de la méthode précédente : on remplace $f$ par sa valeur au **bord droit** $f(x_{i+1})$.

$$I \approx h\,\big[f(x_1) + f(x_2) + \dots + f(x_n)\big]$$

Le point $x_0 = a$ n'est pas utilisé. Les deux sommes ne diffèrent que par leurs extrémités : $D_n = R_n + h\,\big(f(b) - f(a)\big)$, où $R_n$ et $D_n$ désignent les sommes à gauche et à droite.

**Erreur.** Même borne que pour les rectangles à gauche, mais une estimation de **signe opposé** :

$$|E| \leq \frac{(b-a)\,h}{2}\,\max_{[a,b]} |f'|, \qquad E \approx \frac{h}{2}\,\big(f(b) - f(a)\big)$$

Comme $f$ est décroissante, chaque rectangle reste sous la courbe : la méthode **sous-estime** l'intégrale.

**Résultat** avec $n = 10$ : $I \approx 0{,}714605$, erreur $-3{,}22 \times 10^{-2}$, sous la borne théorique ($4{,}29 \times 10^{-2}$). Méthode d'**ordre 1**, comme les rectangles à gauche.

**Encadrement.** Pour une fonction monotone, les deux méthodes encadrent la valeur exacte. Ici, avec $n = 10$ :

$$D_{10} \leq I \leq R_{10} \qquad \text{soit} \qquad 0{,}7146 \leq I \leq 0{,}7778$$

C'est une garantie obtenue **sans connaître** $I$.

**Vers la méthode des trapèzes.** Les erreurs à gauche et à droite sont presque opposées, donc leur **moyenne** les fait presque disparaître :

$$T_n = \frac{R_n + D_n}{2} = h\left[\frac{f(x_0)}{2} + f(x_1) + \dots + f(x_{n-1}) + \frac{f(x_n)}{2}\right]$$

C'est la **méthode des trapèzes** : on remplace $f$ par le segment qui relie $f(x_i)$ à $f(x_{i+1})$. Avec $n = 10$, l'erreur tombe à $-6{,}1 \times 10^{-4}$, soit environ 50 fois moins, pour le même nombre d'évaluations de $f$. Les termes en $h$ se compensent et il ne reste qu'une erreur en $h^2$ : la méthode des trapèzes est d'**ordre 2**. Le script affiche cette comparaison.

### Méthode de Simpson

Code : [`simpson.py`](integration_numerique/simpson.py) | Théorie : [`simpson.md`](integration_numerique/simpson.md)

**Principe.** On regroupe les sous-intervalles **deux par deux**. Sur chaque paire $[x_{2j}, x_{2j+2}]$, on remplace $f$ par la **parabole** qui passe par les trois points $x_{2j}$, $x_{2j+1}$, $x_{2j+2}$, et on intègre exactement cette parabole. On obtient :

$$I \approx \frac{h}{3}\,\big[f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \dots + 2f(x_{n-2}) + 4f(x_{n-1}) + f(x_n)\big]$$

Les coefficients suivent le motif $1, 4, 2, 4, \dots, 2, 4, 1$. Le nombre de sous-intervalles $n$ doit être **pair** : le script lève une erreur sinon.

**Erreur.** Si $f$ est de classe $C^4$ :

$$|E| \leq \frac{(b-a)\,h^4}{180}\,\max_{[a,b]} |f^{(4)}|$$

Ici $f^{(4)}(x) = (16x^4 - 48x^2 + 12)\,e^{-x^2}$, dont la valeur absolue est maximale en $x = 0$ : $\max |f^{(4)}| = 12$.

**Résultat.**

| $n$ | Approximation | Erreur | Borne théorique |
|---:|---:|---:|---:|
| 10 | 0,746824948254 | $8{,}15 \times 10^{-7}$ | $6{,}67 \times 10^{-6}$ |
| 100 | 0,746824132894 | $8{,}17 \times 10^{-11}$ | $6{,}67 \times 10^{-10}$ |

**À retenir.** Méthode d'**ordre 4** : l'erreur est proportionnelle à $h^4$. Quand on double $n$, l'erreur est divisée par $2^4 = 16$ (le script affiche des rapports qui tendent vers 16). Bonus : comme l'erreur dépend de $f^{(4)}$, Simpson est **exacte pour les polynômes de degré 3**, alors qu'elle n'utilise que des paraboles.

Pour garantir une erreur inférieure à $10^{-6}$, la borne théorique impose $n \geq 16{,}1$ : comme $n$ doit être pair, **$n = 18$** suffit, contre environ 430 000 pour les rectangles.

### Comparaison des méthodes d'intégration

Même intégrale, même nombre de sous-intervalles ($n = 10$, soit une dizaine d'évaluations de $f$) :

| Méthode | Évaluations de $f$ | Erreur | Ordre | Si $n$ double, l'erreur est divisée par |
|---|---:|---:|---:|---:|
| Rectangles à gauche | 10 | $+3{,}10 \times 10^{-2}$ | 1 | 2 |
| Rectangles à droite | 10 | $-3{,}22 \times 10^{-2}$ | 1 | 2 |
| Trapèzes (moyenne des deux) | 11 | $-6{,}1 \times 10^{-4}$ | 2 | 4 |
| Simpson | 11 | $+8{,}15 \times 10^{-7}$ | 4 | 16 |

Chaque gain d'ordre se paie à peine en calculs, mais améliore énormément la précision. Pour presque le même coût, les trapèzes sont environ 50 fois plus précis que les rectangles, et Simpson environ **750 fois plus précise que les trapèzes** (38 000 fois plus que les rectangles). Même avec 1 000 rectangles à gauche, l'erreur ($3{,}16 \times 10^{-4}$) reste très au-dessus de celle de Simpson avec seulement 10 sous-intervalles.

Les rectangles restent utiles pour comprendre l'idée de l'intégration numérique et, combinés, pour encadrer l'intégrale d'une fonction monotone. En pratique, on leur préfère les méthodes d'ordre plus élevé comme Simpson, à condition que $f$ soit assez régulière.
