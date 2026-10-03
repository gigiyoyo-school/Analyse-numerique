"""Résolution de x^3 - 2 = 0 par la méthode de dichotomie (précision 0.01)."""
import math

from rich.console import Console
from rich.table import Table

console = Console()


def f(x: float) -> float:
    return x**3 - 2


def dichotomie(f, a: float, b: float, eps: float = 0.01, max_iter: int = 100):
    """Réduit [a, b] de moitié jusqu'à ce que l'erreur sur le milieu soit < eps."""
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) et f(b) doivent être de signes opposés")

    # Nombre d'itérations prévu par la théorie : (b - a) / 2^n < eps
    n_theorique = math.ceil(math.log2((b - a) / eps))
    console.print(f"[bold]Nombre d'itérations prévu :[/] {n_theorique}\n")

    table = Table(title="Méthode de dichotomie : f(x) = x^3 - 2")
    for col in ["n", "a", "b", "m", "f(m)", "(b - a)/2"]:
        table.add_column(col, justify="right")

    for n in range(1, max_iter + 1):
        m = (a + b) / 2
        demi_largeur = (b - a) / 2  # erreur maximale si on retient m
        table.add_row(str(n), f"{a:.6f}", f"{b:.6f}", f"{m:.6f}",
                      f"{f(m):+.6f}", f"{demi_largeur:.6f}")

        if f(m) == 0 or demi_largeur < eps:
            console.print(table)
            return m, n

        if f(a) * f(m) < 0:
            b = m  # la racine est dans [a, m]
        else:
            a = m  # la racine est dans [m, b]

    console.print(table)
    raise RuntimeError("Pas de convergence après max_iter itérations")


if __name__ == "__main__":
    racine, n_iter = dichotomie(f, a=1.0, b=2.0, eps=0.01)
    console.print(f"\n[bold green]Racine approchée :[/] {racine:.4f} (en {n_iter} itérations)")
    console.print(f"[bold]Valeur exacte 2^(1/3) :[/] {2 ** (1 / 3):.4f}")
    console.print(f"[bold]Erreur réelle :[/] {abs(racine - 2 ** (1 / 3)):.6f}")