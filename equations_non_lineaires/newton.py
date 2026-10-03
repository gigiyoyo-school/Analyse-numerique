"""Résolution de x^3 - 2 = 0 par la méthode de Newton (précision 0.01)."""
from rich.console import Console
from rich.table import Table

console = Console()


def f(x: float) -> float:
    return x**3 - 2


def df(x: float) -> float:
    return 3 * x**2


def d2f(x: float) -> float:
    return 6 * x


def newton(f, df, x0: float, eps: float = 0.01, max_iter: int = 100):
    """Itère x_{n+1} = x_n - f(x_n)/f'(x_n) jusqu'à |x_{n+1} - x_n| < eps."""
    # Condition de Fourier : garantit une convergence monotone
    if f(x0) * d2f(x0) <= 0:
        console.print("[yellow]Attention : f(x0)·f''(x0) <= 0, convergence non garantie[/]")

    table = Table(title="Méthode de Newton : f(x) = x^3 - 2")
    for col in ["n", "x_n", "f(x_n)", "|x_n - x_(n-1)|"]:
        table.add_column(col, justify="right")

    x = x0
    table.add_row("0", f"{x:.8f}", f"{f(x):+.8f}", "-")

    for n in range(1, max_iter + 1):
        derivee = df(x)
        if derivee == 0:
            raise ZeroDivisionError("f'(x) = 0 : la tangente est horizontale")

        x_new = x - f(x) / derivee
        ecart = abs(x_new - x)
        table.add_row(str(n), f"{x_new:.8f}", f"{f(x_new):+.8f}", f"{ecart:.8f}")
        x = x_new

        if ecart < eps:
            console.print(table)
            return x, n

    console.print(table)
    raise RuntimeError("Pas de convergence après max_iter itérations")


if __name__ == "__main__":
    racine, n_iter = newton(f, df, x0=2.0, eps=0.01)
    console.print(f"\n[bold green]Racine approchée :[/] {racine:.6f} (en {n_iter} itérations)")
    console.print(f"[bold]Valeur exacte 2^(1/3) :[/] {2 ** (1 / 3):.6f}")
    console.print(f"[bold]Erreur réelle :[/] {abs(racine - 2 ** (1 / 3)):.2e}")