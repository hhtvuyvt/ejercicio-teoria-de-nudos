"""
Prueba de los invariantes topológicos disponibles en Topoly.

El objetivo es observar qué información produce cada invariante
para una misma curva cerrada.
"""

from __future__ import annotations

import numpy as np
import topoly
from topoly.params import Closure, ReduceMethod, Translate


def calcular_invariante(
    nombre: str,
    funcion,
    puntos: np.ndarray,
) -> None:
    """Calcula e imprime un invariante de Topoly."""

    cadena = puntos.tolist()

    try:
        resultado = funcion(
            cadena,
            closure=Closure.CLOSED,
            tries=1,
            reduce_method=ReduceMethod.KMT,
            max_cross=15,
            translate=Translate.YES,
            hide_trivial=False,
            hide_rare=False,
            chiral=False,
            minimal=True,
            run_parallel=False,
        )

        print(f"{nombre:<20}: {resultado}")

    except (TypeError, ValueError, RuntimeError) as error:
        print(
            f"{nombre:<20}: ERROR -> "
            f"{type(error).__name__}: {error}"
        )


def main() -> None:
    """Genera una curva sencilla y calcula varios invariantes."""

    puntos = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
        ],
        dtype=float,
    )

    print("PRUEBA DE INVARIANTES")
    print("=" * 60)

    invariantes = {
        "Alexander": topoly.alexander,
        "Jones": topoly.jones,
        "Conway": topoly.conway,
        "HOMFLY": topoly.homfly,
        "Kauffman bracket": topoly.kauffman_bracket,
        "BLMHO": topoly.blmho,
        "Yamada": topoly.yamada,
        "APS": topoly.aps,
        "Writhe": topoly.writhe,
    }

    for nombre, funcion in invariantes.items():
        calcular_invariante(
            nombre,
            funcion,
            puntos,
        )

    print("=" * 60)


if __name__ == "__main__":
    main()