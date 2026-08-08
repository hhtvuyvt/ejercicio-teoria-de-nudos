"""
Clasificación topológica inicial de polígonos.

La geometría se genera en generador.py y la clasificación se mantiene
separada para que podamos cambiar posteriormente el método de
identificación sin modificar el generador.

Topoly recibe la estructura como una lista de Python. Nuestro generador
trabaja internamente con numpy.ndarray, por lo que aquí realizamos la
conversión entre ambas representaciones.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import topoly
from topoly.params import (
    Closure,
    ReduceMethod,
    Translate,
)


def clasificar_nudo(
    puntos: np.ndarray,
    max_cross: int = 15,
) -> Any:
    """
    Intenta identificar el tipo de nudo representado por la curva.

    La curva ya está cerrada, por lo que utilizamos Closure.CLOSED.

    El primer método utilizado es el polinomio de Alexander.

    Parameters
    ----------
    puntos:
        Matriz N x 3 con las coordenadas tridimensionales de los
        vértices del polígono.

    max_cross:
        Número máximo de cruces utilizado por el algoritmo de Topoly.

    Returns
    -------
    Any
        Resultado de clasificación producido por Topoly.
    """

    # ----------------------------------------------------------
    # Conversión NumPy -> lista de Python
    # ----------------------------------------------------------
    #
    # Nuestro programa utiliza numpy.ndarray internamente, pero
    # la interfaz de Topoly utilizada actualmente espera una
    # lista o una cadena.
    #
    # tolist() convierte:
    #
    #     np.ndarray
    #
    # en:
    #
    #     list[list[float]]
    #
    estructura = puntos.tolist()

    # ----------------------------------------------------------
    # Clasificación topológica
    # ----------------------------------------------------------
    resultado = topoly.alexander(
        estructura,
        closure=Closure.CLOSED,
        tries=1,
        reduce_method=ReduceMethod.KMT,
        max_cross=max_cross,
        translate=Translate.YES,
        hide_trivial=False,
        hide_rare=False,
        chiral=False,
        minimal=True,
        run_parallel=False,
    )

    return resultado