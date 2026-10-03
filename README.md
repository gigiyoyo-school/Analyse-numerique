# Analyse numérique

Présentation, en Python, des principales méthodes d'analyse numérique vues en cours, chacune illustrée par un exemple complet dont toutes les itérations sont affichées dans un tableau.

Le cœur du projet porte sur la **résolution d'équations non linéaires** $f(x) = 0$. Une seconde partie traite de l'**interpolation polynomiale**.

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

## Structure du projet

```
analyse-numerique/
├── README.md
├── pyproject.toml              # dépendances (numpy, rich)
├── equations_non_lineaires/    # Partie 1 : résoudre f(x) = 0
│   ├── __init__.py
│   ├── dichotomie.py
│   ├── point_fixe.py
│   └── newton.py
└── interpolation/              # Partie 2 : polynôme passant par des points donnés
    ├── __init__.py
    ├── directe.py              # système de Vandermonde
    ├── lagrange.py
    └── newton.py               # différences divisées
```

Chaque fichier est autonome : il contient la méthode, l'exemple et l'affichage des résultats.

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

---

## Partie 1 : équations non linéaires

### Le problème commun

Les trois méthodes résolvent la **même équation**, ce qui permet de les comparer :

$$f(x) = x^3 - 2 = 0 \quad \text{sur } [1, 2], \qquad \text{précision } \varepsilon = 0{,}01$$

La solution exacte est $\alpha = \sqrt[3]{2} \approx 1{,}259921$. Elle existe et est unique sur $[1, 2]$ car $f(1) = -1 < 0$, $f(2) = 6 > 0$ et $f$ est strictement croissante ($f'(x) = 3x^2 > 0$).

### Méthode de dichotomie

Fichier : [`equations_non_lineaires/dichotomie.py`](equations_non_lineaires/dichotomie.py)

**Principe.** Si $f$ est continue et $f(a) \cdot f(b) < 0$, une racine se trouve dans $[a, b]$ (théorème des valeurs intermédiaires). On calcule le milieu $m = \frac{a+b}{2}$ et on garde la moitié de l'intervalle où $f$ change de signe :

- si $f(a) \cdot f(m) < 0$, la racine est dans $[a, m]$ ;
- sinon, elle est dans $[m, b]$.

**Critère d'arrêt.** Après $n$ itérations, l'erreur sur le milieu est au plus $\frac{b-a}{2^n}$. On s'arrête quand cette borne passe sous $\varepsilon$. Le nombre d'itérations est donc **connu à l'avance** :

$$n \geq \log_2\left(\frac{b-a}{\varepsilon}\right) = \log_2(100) \approx 6{,}64 \quad \Rightarrow \quad n = 7$$

**Résultat.** $x \approx 1{,}2578$ en **7 itérations** (erreur réelle : $2{,}1 \times 10^{-3}$).

**À retenir.** Convergence toujours garantie dès que $f(a) \cdot f(b) < 0$, mais lente : on gagne un chiffre binaire par itération (convergence linéaire de rapport $\frac{1}{2}$).

### Méthode du point fixe

Fichier : [`equations_non_lineaires/point_fixe.py`](equations_non_lineaires/point_fixe.py)

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

Fichier : [`equations_non_lineaires/newton.py`](equations_non_lineaires/newton.py)

**Principe.** On remplace la courbe par sa tangente au point $x_n$ et on prend l'intersection de cette tangente avec l'axe des abscisses :

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} = x_n - \frac{x_n^3 - 2}{3x_n^2}$$

**Condition de convergence (Fourier).** Si $f(a) \cdot f(b) < 0$, si $f'$ et $f''$ ne s'annulent pas sur $[a, b]$ et si le point de départ $x_0 \in [a, b]$ vérifie $f(x_0) \cdot f''(x_0) > 0$, la suite converge de façon monotone. Avec $x_0 = 2$ : $f(2) = 6 > 0$ et $f''(2) = 12 > 0$. Le programme affiche un avertissement si cette condition n'est pas remplie.

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

> Les critères d'arrêt ne sont pas identiques (borne d'erreur pour la dichotomie et le point fixe, écart entre deux itérés pour Newton). Si Newton dépasse largement la précision demandée, c'est grâce à sa convergence quadratique : au moment où l'écart entre deux itérés passe sous $\varepsilon$, l'erreur sur le dernier itéré est déjà de l'ordre de son carré.

---

## Partie 2 : interpolation polynomiale

On cherche le polynôme $P$ de degré au plus 2 qui passe par les trois points :

| $t_i$ | 0 | 1 | 2 |
|---|---:|---:|---:|
| $y_i$ | 0 | 1 | −1 |

Les trois méthodes donnent **le même polynôme** (il est unique), écrit dans trois bases différentes :

$$P(t) = \frac{5}{2}\,t - \frac{3}{2}\,t^2, \qquad P(0{,}5) = 0{,}875, \qquad P(1{,}5) = 0{,}375$$

| Méthode | Fichier | Idée |
|---|---|---|
| Directe | [`interpolation/directe.py`](interpolation/directe.py) | On écrit $P(t) = a_0 + a_1 t + a_2 t^2$ et on résout le système de Vandermonde $V a = y$. |
| Lagrange | [`interpolation/lagrange.py`](interpolation/lagrange.py) | $P(x) = \sum_i y_i\, L_i(x)$ avec $L_i(x) = \prod_{j \neq i} \frac{x - t_j}{t_i - t_j}$. Aucun système à résoudre. |
| Newton | [`interpolation/newton.py`](interpolation/newton.py) | Coefficients obtenus par le tableau des différences divisées, évaluation par le schéma de Horner. Ajouter un point ne remet pas en cause les calculs déjà faits. |

**Pourquoi trois méthodes ?** La méthode directe est la plus intuitive, mais la matrice de Vandermonde devient **mal conditionnée** quand le nombre de points augmente : de petites erreurs d'arrondi produisent de grandes erreurs sur les coefficients. Lagrange évite le système linéaire, mais tous les $L_i$ changent dès qu'on ajoute un point. Newton cumule les deux avantages, ce qui en fait la méthode la plus utilisée en pratique.