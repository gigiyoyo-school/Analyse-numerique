"""Interpolation polynomiale par la méthode de Newton (différences divisées)."""
from rich.console import Console
from rich.table import Table

console = Console()


def differences_divisees(t: list[float], y: list[float]) -> list[list[float]]:
    """Construit le tableau triangulaire : dd[k][i] = f[t_i, ..., t_{i+k}]."""
    n = len(t)
    dd = [list(y)]  # ordre 0
    for k in range(1, n):
        precedent = dd[k - 1]
        ordre_k = [
            (precedent[i + 1] - precedent[i]) / (t[i + k] - t[i])
            for i in range(n - k)
        ]
        dd.append(ordre_k)
    return dd


def afficher_tableau(t: list[float], dd: list[list[float]]) -> None:
    table = Table(title="Tableau des différences divisées")
    table.add_column("t_i", justify="right")
    for k in range(len(dd)):
        table.add_column(f"Ordre {k}", justify="right")
    for i in range(len(t)):
        ligne = [f"{t[i]}"]
        for k in range(len(dd)):
            if i < len(dd[k]):
                valeur = f"{dd[k][i]:+.4f}"
                # Les coefficients de Newton sont sur la première ligne
                ligne.append(f"[bold cyan]{valeur}[/]" if i == 0 else valeur)
            else:
                ligne.append("")
        table.add_row(*ligne)
    console.print(table)


def evaluer_newton(t: list[float], coeffs: list[float], x: float) -> float:
    """Schéma de Horner : P(x) = c0 + (x-t0)(c1 + (x-t1)(c2 + ...))."""
    P = coeffs[-1]
    for k in range(len(coeffs) - 2, -1, -1):
        P = coeffs[k] + (x - t[k]) * P
    return P


if __name__ == "__main__":
    t = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, -1.0]

    dd = differences_divisees(t, y)
    afficher_tableau(t, dd)

    coeffs = [dd[k][0] for k in range(len(dd))]
    console.print("\n[bold]Coefficients de Newton :[/]")
    for k, c in enumerate(coeffs):
        console.print(f"  c{k} = {c:+.4f}")

    termes = [f"{coeffs[0]:+.2f}"]
    for k in range(1, len(coeffs)):
        produit = "".join(f"(t - {t[j]})" for j in range(k))
        termes.append(f"{coeffs[k]:+.2f}·{produit}")
    console.print(f"\n[bold green]P(t) =[/] {' '.join(termes)}\n")

    for x in [0.5, 1.5]:
        console.print(f"[bold green]P({x}) = {evaluer_newton(t, coeffs, x):.4f}[/]")