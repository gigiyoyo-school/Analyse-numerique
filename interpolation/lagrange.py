"""Interpolation polynomiale par la méthode de Lagrange."""
from rich.console import Console
from rich.table import Table

console = Console()


def base_lagrange(t_points: list[float], i: int, x: float) -> float:
    """Calcule L_i(x) = prod_{j != i} (x - t_j) / (t_i - t_j)."""
    L = 1.0
    for j, tj in enumerate(t_points):
        if j != i:
            L *= (x - tj) / (t_points[i] - tj)
    return L


def lagrange(t_points: list[float], y_points: list[float], x: float) -> float:
    """Évalue P(x) = sum_i y_i * L_i(x) en affichant le détail du calcul."""
    table = Table(title=f"Polynômes de base en x = {x}")
    for col in ["i", "t_i", "y_i", "L_i(x)", "y_i · L_i(x)"]:
        table.add_column(col, justify="right")

    P = 0.0
    somme_L = 0.0
    for i, (ti, yi) in enumerate(zip(t_points, y_points)):
        Li = base_lagrange(t_points, i, x)
        P += yi * Li
        somme_L += Li
        table.add_row(str(i), f"{ti}", f"{yi}", f"{Li:+.4f}", f"{yi * Li:+.4f}")

    table.add_row("", "", "[bold]Somme[/]", f"[bold]{somme_L:+.4f}[/]", f"[bold]{P:+.4f}[/]")
    console.print(table)
    return P


if __name__ == "__main__":
    t = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, -1.0]

    for x in [0.5, 1.5]:
        P = lagrange(t, y, x)
        console.print(f"[bold green]P({x}) = {P:.4f}[/]\n")