"""
Geometrías deterministas utilizadas para validar el clasificador.

Estas curvas no forman parte del generador aleatorio del experimento.
Su objetivo es proporcionar casos cuyo tipo topológico conocemos de
antemano.
"""

from __future__ import annotations

import numpy as np


def nudo_trivial(
    numero_puntos: int = 40,
) -> np.ndarray:
    """
    Genera una circunferencia plana que representa el nudo trivial 0_1.

    Parámetros
    ----------
    numero_puntos:
        Número de puntos utilizados para discretizar la circunferencia.

    Retorna
    -------
    np.ndarray
        Coordenadas tridimensionales de la curva.
    """

    if numero_puntos < 4:
        raise ValueError(
            "Se necesitan al menos 4 puntos."
        )

    parametros = np.linspace(
        0.0,
        2.0 * np.pi,
        numero_puntos,
        endpoint=False,
    )

    x = np.cos(parametros)
    y = np.sin(parametros)
    z = np.zeros_like(parametros)

    return np.column_stack(
        (x, y, z)
    )


def trefoil(
    numero_puntos: int = 100,
) -> np.ndarray:
    """
    Genera una representación paramétrica del nudo trefoil 3_1.

    Parámetros
    ----------
    numero_puntos:
        Número de puntos utilizados para discretizar la curva.

    Retorna
    -------
    np.ndarray
        Coordenadas tridimensionales de la curva.
    """

    if numero_puntos < 4:
        raise ValueError(
            "Se necesitan al menos 4 puntos."
        )

    parametros = np.linspace(
        0.0,
        2.0 * np.pi,
        numero_puntos,
        endpoint=False,
    )

    x = (
        np.sin(parametros)
        + 2.0 * np.sin(2.0 * parametros)
    )

    y = (
        np.cos(parametros)
        - 2.0 * np.cos(2.0 * parametros)
    )

    z = -np.sin(
        3.0 * parametros
    )

    return np.column_stack(
        (x, y, z)
    )