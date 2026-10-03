# Dichotomie : fondements théoriques

Code associé : [`dichotomie.py`](dichotomie.py)

## 1. Théorème des valeurs intermédiaires (TVI)

> **Théorème.** Soit $f$ une fonction **continue** sur $[a, b]$ telle que $f(a) \cdot f(b) < 0$. Alors il existe au moins un réel $c \in \,]a, b[$ tel que $f(c) = 0$.

**Idée.** Une fonction continue ne peut pas passer d'une valeur négative à une valeur positive sans traverser zéro : sa courbe se trace « sans lever le crayon ».

**Attention.** Le TVI garantit l'**existence** d'une racine, pas son unicité. La fonction peut s'annuler plusieurs fois entre $a$ et $b$.

## 2. Corollaire : unicité par stricte monotonie

> **Corollaire.** Si de plus $f$ est **strictement monotone** sur $[a, b]$, la racine est **unique**.

**Idée.** Une fonction strictement monotone ne prend jamais deux fois la même valeur, donc elle ne peut pas valoir 0 en deux points différents.

**Application.** Pour $f(x) = x^3 - 2$ sur $[1, 2]$ :

- $f$ est continue (polynôme) ;
- $f(1) = -1 < 0$ et $f(2) = 6 > 0$ ;
- $f'(x) = 3x^2 > 0$, donc $f$ est strictement croissante.

La racine $\alpha = \sqrt[3]{2}$ existe et est unique dans $[1, 2]$.

## 3. Théorème de convergence de la dichotomie

On note $[a_0, b_0] = [a, b]$. À chaque itération $n \geq 1$, on calcule le milieu $m_n$ de $[a_{n-1}, b_{n-1}]$, puis on garde la moitié qui contient le changement de signe.

> **Théorème.** Si $f$ est continue sur $[a, b]$ et $f(a) \cdot f(b) < 0$, la suite des milieux $(m_n)$ converge vers une racine $\alpha$ de $f$, et
> $$|m_n - \alpha| \leq \frac{b - a}{2^n}$$

**Idée de la preuve.**

1. La suite $(a_n)$ est croissante, $(b_n)$ est décroissante, et $b_n - a_n = \frac{b - a}{2^n} \to 0$. Les deux suites sont donc **adjacentes** : elles convergent vers une même limite $\alpha$.
2. Par construction, $f(a_n) \cdot f(b_n) \leq 0$ pour tout $n$. En passant à la limite (par continuité de $f$) : $f(\alpha)^2 \leq 0$, donc $f(\alpha) = 0$.
3. La racine est dans $[a_{n-1}, b_{n-1}]$, et $m_n$ est le milieu de cet intervalle. L'écart entre les deux est donc au plus la moitié de sa largeur : $\frac{b - a}{2^n}$.

## 4. Nombre d'itérations prévu

Pour garantir $|m_n - \alpha| < \varepsilon$, il suffit que $\frac{b - a}{2^n} < \varepsilon$, c'est à dire :

$$n \geq \log_2\left(\frac{b - a}{\varepsilon}\right) = \frac{\ln\left(\frac{b - a}{\varepsilon}\right)}{\ln 2}$$

**Application.** Avec $b - a = 1$ et $\varepsilon = 0{,}01$ : $n \geq \log_2(100) \approx 6{,}64$, donc $n = 7$. C'est exactement ce qu'on observe en lançant le script.

C'est une propriété rare : on connaît le coût du calcul **avant** de le lancer, sans rien savoir d'autre sur $f$ que sa continuité.

## 5. Vitesse de convergence

La borne d'erreur est divisée par 2 à chaque itération : la convergence est **linéaire de rapport $\frac{1}{2}$**.

Pour gagner un chiffre décimal, il faut diviser l'erreur par 10, soit $\log_2(10) \approx 3{,}3$ itérations. C'est lent comparé à Newton (voir [`newton.md`](newton.md)).

## 6. Limites

- **Racines de multiplicité paire.** Si $f$ touche l'axe sans le traverser (comme $f(x) = x^2$ en 0), il n'y a pas de changement de signe et la méthode ne peut pas démarrer.
- **Plusieurs racines.** S'il y en a plusieurs dans $[a, b]$, la méthode en trouve une seule, sans qu'on puisse choisir laquelle.
- **Lenteur.** La méthode n'utilise que le **signe** de $f$, jamais sa valeur ni sa pente. Elle est robuste, mais ignore des informations qui permettraient d'aller plus vite.