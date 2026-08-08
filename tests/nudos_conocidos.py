"""
Colección de nudos conocidos para pruebas.

Este módulo contiene polígonos tridimensionales cerrados que utilizamos
como casos de referencia para validar el clasificador topológico.

IMPORTANTE
----------
Estas curvas no forman parte del experimento aleatorio. Son casos
controlados cuya clase topológica conocemos de antemano.

Convención utilizada por Topoly:

    0_1 -> nudo trivial
    3_1 -> trébol
    4_1 -> figura de ocho
"""

from __future__ import annotations

import numpy as np


def nudo_trivial(
    numero_puntos: int = 32,
) -> np.ndarray:
    """
    Genera una circunferencia cerrada.

    Una circunferencia es una representación del nudo trivial 0_1.

    Parámetros
    ----------
    numero_puntos:
        Número de vértices utilizados para discretizar la circunferencia.

    Retorna
    -------
    np.ndarray
        Array de forma (numero_puntos, 3).
    """

    if numero_puntos < 3:
        raise ValueError(
            "numero_puntos debe ser como mínimo 3."
        )

    angulos = np.linspace(
        0.0,
        2.0 * np.pi,
        numero_puntos,
        endpoint=False,
    )

    x = np.cos(angulos)
    y = np.sin(angulos)
    z = np.zeros(numero_puntos)

    return np.column_stack(
        (x, y, z)
    )


def nudo_trebol(
    numero_puntos: int = 100,
) -> np.ndarray:
    """
    Genera una discretización del trébol 3_1.

    Se utiliza una parametrización tridimensional del trébol y se
    discretiza uniformemente en el parámetro.

    Parámetros
    ----------
    numero_puntos:
        Número de vértices de la discretización.

    Retorna
    -------
    np.ndarray
        Array de forma (numero_puntos, 3).
    """

    if numero_puntos < 3:
        raise ValueError(
            "numero_puntos debe ser como mínimo 3."
        )

    t = np.linspace(
        0.0,
        2.0 * np.pi,
        numero_puntos,
        endpoint=False,
    )

    x = (
        np.sin(t)
        + 2.0 * np.sin(2.0 * t)
    )

    y = (
        np.cos(t)
        - 2.0 * np.cos(2.0 * t)
    )

    z = -np.sin(3.0 * t)

    return np.column_stack(
        (x, y, z)
    )


def nudo_figura_ocho(
    numero_puntos: int = 100,
) -> np.ndarray:
    """
    Genera una discretización de un nudo de figura de ocho 4_1.

    Se utiliza una parametrización estándar de la figura de ocho.

    Parámetros
    ----------
    numero_puntos:
        Número de vértices de la discretización.

    Retorna
    -------
    np.ndarray
        Array de forma (numero_puntos, 3).
    """

    if numero_puntos < 3:
        raise ValueError(
            "numero_puntos debe ser como mínimo 3."
        )

    t = np.linspace(
        0.0,
        2.0 * np.pi,
        numero_puntos,
        endpoint=False,
    )

    x = (
        (2.0 + np.cos(2.0 * t))
        * np.cos(3.0 * t)
    )

    y = (
        (2.0 + np.cos(2.0 * t))
        * np.sin(3.0 * t)
    )

    z = np.sin(4.0 * t)

    return np.column_stack(
        (x, y, z)
    )