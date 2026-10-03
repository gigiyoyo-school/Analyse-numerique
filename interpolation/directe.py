"""Interpolation polynomiale par la méthode directe (système de Vandermonde)."""
import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()


def interpolation_directe(t: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Renvoie les coefficients [a0, a1, ..., an] de P(t) = a0 + a1 t + ... + an t^n."""
    n = len(t)
    # Matrice de Vandermonde : V[i, j] = t_i ** j
    V = np.vander(t, N=n, increasing=True)
    console.print("[bold]Matrice de Vandermonde V :[/]")
    console.print(V)
    return np.linalg.solve(V, y)


def evaluer(coeffs: np.ndarray, x: float) -> float:
    """Évalue P(x) = sum(a_k * x^k)."""
    return sum(a * x**k for k, a in enumerate(coeffs))


if __name__ == "__main__":
    t = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, -1.0])

    coeffs = interpolation_directe(t, y)

    console.print("\n[bold]Coefficients :[/]")
    for k, a in enumerate(coeffs):
        console.print(f"  a{k} = {a:+.4f}")

    termes = " ".join(f"{a:+.2f}·t^{k}" for k, a in enumerate(coeffs))
    console.print(f"\n[bold green]P(t) =[/] {termes}")

    # Vérification sur les points d'interpolation
    table = Table(title="Vérification et évaluation")
    for col in ["t", "f(t) donné", "P(t)"]:
        table.add_column(col, justify="right")
    for ti, yi in zip(t, y):
        table.add_row(f"{ti}", f"{yi}", f"{evaluer(coeffs, ti):.4f}")
    for x in [0.5, 1.5]:
        table.add_row(f"[cyan]{x}[/]", "-", f"[cyan]{evaluer(coeffs, x):.4f}[/]")
    console.print(table)