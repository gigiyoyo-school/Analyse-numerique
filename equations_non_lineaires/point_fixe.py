"""Résolution de x^3 - 2 = 0 par la méthode du point fixe (précision 0.01)."""
import math

from rich.console import Console
from rich.table import Table

console = Console()


def g(x: float) -> float:
    """Fonction d'itération : x = sqrt(2/x), contractante sur [1, 2]."""
    return math.sqrt(2 / x)


def point_fixe(g, x0: float, eps: float = 0.01, k: float = math.sqrt(2) / 2, max_iter: int = 100):
    """Itère x_{n+1} = g(x_n) jusqu'à ce que la borne d'erreur soit < eps."""
    table = Table(title="Méthode du point fixe : g(x) = sqrt(2/x)")
    table.add_column("n", justify="right")
    table.add_column("x_n", justify="right")
    table.add_column("|x_n - x_(n-1)|", justify="right")
    table.add_column("Borne d'erreur", justify="right")

    x = x0
    table.add_row("0", f"{x:.6f}", "-", "-")

    for n in range(1, max_iter + 1):
        x_new = g(x)
        ecart = abs(x_new - x)
        borne = k / (1 - k) * ecart  # majoration de |x_n - alpha|
        table.add_row(str(n), f"{x_new:.6f}", f"{ecart:.6f}", f"{borne:.6f}")
        x = x_new
        if borne < eps:
            console.print(table)
            return x, n

    console.print(table)
    raise RuntimeError("Pas de convergence après max_iter itérations")


if __name__ == "__main__":
    racine, n_iter = point_fixe(g, x0=1.0, eps=0.01)
    console.print(f"\n[bold green]Racine approchée :[/] {racine:.4f} (en {n_iter} itérations)")
    console.print(f"[bold]Valeur exacte 2^(1/3) :[/] {2 ** (1 / 3):.4f}")
    console.print(f"[bold]Erreur réelle :[/] {abs(racine - 2 ** (1 / 3)):.6f}")