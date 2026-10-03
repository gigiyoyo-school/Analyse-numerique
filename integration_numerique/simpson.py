"""Intégrale de exp(-x^2) sur [0, 1] par la méthode de Simpson composite."""
import math

from rich.console import Console
from rich.table import Table

console = Console()


def f(x: float) -> float:
    return math.exp(-x**2)


def coefficient(i: int, n: int) -> int:
    """Motif 1, 4, 2, 4, 2, ..., 2, 4, 1."""
    if i == 0 or i == n:
        return 1
    return 4 if i % 2 == 1 else 2


def simpson(f, a: float, b: float, n: int, afficher: bool = False) -> float:
    """I ≈ h/3 * [f0 + 4 f1 + 2 f2 + 4 f3 + ... + 4 f_{n-1} + f_n], n pair."""
    if n % 2 != 0:
        raise ValueError("Simpson exige un nombre pair d'intervalles")
    h = (b - a) / n

    table = Table(title=f"Simpson : n = {n}, h = {h}")
    for col in ["i", "x_i", "f(x_i)", "Coef", "Coef × f(x_i)"]:
        table.add_column(col, justify="right")

    somme = 0.0
    for i in range(n + 1):  # cette fois, x_n = b est utilisé
        x = a + i * h
        c = coefficient(i, n)
        somme += c * f(x)
        table.add_row(str(i), f"{x:.2f}", f"{f(x):.6f}", str(c), f"{c * f(x):.6f}")

    table.add_row("", "", "", "[bold]Somme[/]", f"[bold]{somme:.6f}[/]")
    if afficher:
        console.print(table)
    return h / 3 * somme


if __name__ == "__main__":
    a, b = 0.0, 1.0
    exacte = math.sqrt(math.pi) / 2 * math.erf(1)  # √π/2 · erf(1)
    max_d4f = 12  # max de |f''''(x)| = |(16x^4 - 48x^2 + 12) e^{-x^2}| sur [0, 1], atteint en x = 0

    simpson(f, a, b, 10, afficher=True)

    resume = Table(title="Simpson comparé à la valeur exacte")
    for col in ["n", "Approximation", "Erreur", "Erreur relative", "Borne théorique"]:
        resume.add_column(col, justify="right")
    for n in [10, 100]:
        h = (b - a) / n
        approx = simpson(f, a, b, n)
        erreur = approx - exacte
        borne = (b - a) * h**4 / 180 * max_d4f
        resume.add_row(str(n), f"{approx:.12f}", f"{erreur:+.2e}",
                       f"{abs(erreur) / exacte:.2e}", f"{borne:.2e}")
    console.print()
    console.print(resume)
    console.print(f"[bold]Valeur exacte :[/] {exacte:.12f}")

    # Ordre de la méthode : l'erreur est divisée par ~16 quand n double
    ordre = Table(title="Évolution de l'erreur avec n")
    for col in ["n", "Erreur", "Rapport"]:
        ordre.add_column(col, justify="right")
    err_prec = None
    for n in [2, 4, 8, 16, 32]:
        err = simpson(f, a, b, n) - exacte
        rapport = f"{err_prec / err:.2f}" if err_prec else "-"
        ordre.add_row(str(n), f"{err:+.2e}", rapport)
        err_prec = err
    console.print()
    console.print(ordre)