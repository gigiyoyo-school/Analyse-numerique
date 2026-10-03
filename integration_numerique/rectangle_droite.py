"""Intégrale de exp(-x^2) sur [0, 1] par la méthode des rectangles à droite."""

import math

from rich.console import Console
from rich.table import Table

from integration_numerique.rectangle_gauche import rectangle_gauche

console = Console()


def f(x: float) -> float:
    return math.exp(-(x**2))


def rectangle_droite(f, a: float, b: float, n: int, afficher: bool = False) -> float:
    """I ≈ h * [f(x_1) + f(x_2) + ... + f(x_n)], avec h = (b - a) / n."""
    h = (b - a) / n

    table = Table(title=f"Rectangles à droite : n = {n}, h = {h}")
    for col in ["i", "x_i", "f(x_i)", "Aire h·f(x_i)"]:
        table.add_column(col, justify="right")

    somme = 0.0
    for i in range(1, n + 1):  # le point x_0 = a n'est pas utilisé
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
    a, b, n = 0.0, 1.0, 10
    h = (b - a) / n

    approx = rectangle_droite(f, a, b, n, afficher=True)

    # Pas de primitive usuelle : la valeur exacte s'exprime avec erf
    exacte = math.sqrt(math.pi) / 2 * math.erf(1)

    erreur = approx - exacte
    # max de |f'(x)| = |-2x e^{-x^2}|, atteint en x = 1/sqrt(2)
    max_df = math.sqrt(2) * math.exp(-0.5)
    borne = (b - a) * h / 2 * max_df
    estimation = h / 2 * (f(b) - f(a))

    console.print(f"\n[bold green]Approximation :[/]        {approx:.6f}")
    console.print(f"[bold]Valeur exacte :[/]        {exacte:.6f}  (√π/2 · erf(1))")
    console.print(
        f"[bold]Erreur :[/]               {erreur:+.6f}  ({abs(erreur) / exacte:.2%})"
    )
    console.print(f"[bold]Borne théorique :[/]      {borne:.6f}")
    console.print(f"[bold]Estimation h/2·(f(b)-f(a)) :[/] {estimation:+.6f}")

    # Comparaison gauche / droite : erreurs de signes opposés
    gauche = rectangle_gauche(f, a, b, n)
    moyenne = (gauche + approx) / 2
    comp = Table(title="Gauche, droite et leur moyenne (n = 10)")
    for col in ["Méthode", "Approximation", "Erreur"]:
        comp.add_column(col, justify="right")
    comp.add_row("Rectangles à gauche", f"{gauche:.6f}", f"{gauche - exacte:+.6f}")
    comp.add_row("Rectangles à droite", f"{approx:.6f}", f"{approx - exacte:+.6f}")
    comp.add_row("Moyenne des deux", f"{moyenne:.6f}", f"{moyenne - exacte:+.6f}")
    console.print()
    console.print(comp)

    # Ordre de la méthode : l'erreur est divisée par ~2 quand n double
    ordre = Table(title="Évolution de l'erreur avec n")
    for col in ["n", "Approximation", "Erreur", "Rapport"]:
        ordre.add_column(col, justify="right")
    err_prec = None
    for k in [10, 20, 40, 80, 160]:
        approx_k = rectangle_droite(f, a, b, k)
        err_k = approx_k - exacte
        rapport = f"{err_prec / err_k:.2f}" if err_prec else "-"
        ordre.add_row(str(k), f"{approx_k:.6f}", f"{err_k:+.6f}", rapport)
        err_prec = err_k
    console.print()
    console.print(ordre)
