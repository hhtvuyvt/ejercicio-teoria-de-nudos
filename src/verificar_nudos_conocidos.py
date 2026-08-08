"""
Verificación manual de las geometrías de referencia.

Este módulo NO forma parte del experimento estadístico.
Su finalidad es comprobar que las curvas conocidas son reconocidas
correctamente por Topoly antes de incorporarlas a los tests.
"""

from __future__ import annotations

import topoly
from topoly.params import Closure

from tests.nudos_conocidos import (
    nudo_figura_ocho,
    nudo_trebol,
    nudo_trivial,
)


def clasificar(
    nombre: str,
    puntos,
) -> None:
    """
    Clasifica una geometría y muestra el resultado.
    """

    resultado = topoly.alexander(
        puntos,
        closure=Closure.CLOSED,
        tries=1,
        max_cross=30,
        hide_trivial=False,
        hide_rare=False,
        chiral=False,
        minimal=True,
        run_parallel=False,
    )

    print(
        f"{nombre:<20} -> {resultado}"
    )


def main() -> None:
    """
    Ejecuta la verificación de las geometrías conocidas.
    """

    print(
        "VERIFICACIÓN DE NUDOS CONOCIDOS"
    )
    print(
        "=" * 50
    )

    clasificar(
        "Nudo trivial",
        nudo_trivial(),
    )

    clasificar(
        "Trébol",
        nudo_trebol(),
    )

    clasificar(
        "Figura de ocho",
        nudo_figura_ocho(),
    )


if __name__ == "__main__":
    main()