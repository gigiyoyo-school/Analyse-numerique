"""Intégrale de exp(-x^2) sur [0, 1] par la méthode des rectangles à gauche."""

import math

from rich.console import Console
from rich.table import Table

console = Console()


def f(x: float) -> float:
    return math.exp(-(x**2))


def rectangle_gauche(f, a: float, b: float, n: int, afficher: bool = False) -> float:
    """I ≈ h * [f(x_0) + f(x_1) + ... + f(x_{n-1})], avec h = (b - a) / n."""
    h = (b - a) / n

    table = Table(title=f"Rectangles à gauche : n = {n}, h = {h}")
    for col in ["i", "x_i", "f(x_i)", "Aire h·f(x_i)"]:
        table.add_column(col, justify="right")

    somme = 0.0
    for i in range(n):  # le point x_n = b n'est pas utilisé
        x = a + i * h
        fx = f(x)
        somme += fx
        table.add_row(str(i), f"{x:.3f}", f"{fx:.6f}", f"{h * fx:.6f}")

    table.add_row(
        "", "[bold]Somme[/]", f"[bold]{somme:.6f}[/]", f"[bold]{h * somme:.6f}[/]"
    )
    if afficher:
        console.print(table)
    return h * somme


if __name__ == "__main__":
    a, b, n = 0.0, 1.0, 1000
    h = (b - a) / n

    # Détail du calcul sur un petit n, lisible à l'écran
    rectangle_gauche(f, a, b, 10, afficher=True)

    approx = rectangle_gauche(f, a, b, n)

    # Pas de primitive usuelle : la valeur exacte s'exprime avec erf
    exacte = math.sqrt(math.pi) / 2 * math.erf(1)

    erreur = approx - exacte
    # max de |f'(x)| = |-2x e^{-x^2}|, atteint en x = 1/sqrt(2)
    max_df = math.sqrt(2) * math.exp(-0.5)
    borne = (b - a) * h / 2 * max_df
    estimation = h / 2 * (f(a) - f(b))

    console.print(f"\n[bold green]Approximation :[/]        {approx:.6f}")
    console.print(f"[bold]Valeur exacte :[/]        {exacte:.6f}  (√π/2 · erf(1))")
    console.print(
        f"[bold]Erreur :[/]               {erreur:+.6f}  ({abs(erreur) / exacte:.2%})"
    )
    console.print(f"[bold]Borne théorique :[/]      {borne:.6f}")
    console.print(f"[bold]Estimation h/2·(f(a)-f(b)) :[/] {estimation:.6f}")

    # Ordre de la méthode : l'erreur est divisée par ~2 quand n double
    table = Table(title="Évolution de l'erreur avec n")
    for col in ["n", "Approximation", "Erreur", "Rapport"]:
        table.add_column(col, justify="right")
    erreur_prec = None
    for k in [10, 20, 40, 80, 160]:
        h_k = (b - a) / k
        approx_k = h_k * sum(f(a + i * h_k) for i in range(k))
        err_k = approx_k - exacte
        rapport = f"{erreur_prec / err_k:.2f}" if erreur_prec else "-"
        table.add_row(str(k), f"{approx_k:.6f}", f"{err_k:.6f}", rapport)
        erreur_prec = err_k
    console.print()
    console.print(table)
