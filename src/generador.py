"""
Generación y validación de polígonos cerrados equidistantes.

La generación se realiza mediante Topoly.

Representación interna
----------------------

Una curva cerrada de N segmentos se almacena internamente como N
vértices únicos:

    v0
    v1
    ...
    v(N-1)

El segmento entre v(N-1) y v0 se considera implícitamente el último
segmento de la curva.

Algunas funciones externas, como Topoly, pueden representar una curva
cerrada repitiendo el primer punto al final:

    v0
    v1
    ...
    v(N-1)
    v0

Esta representación se normaliza antes de entrar al resto del programa.
"""

from __future__ import annotations

import random

import numpy as np
import topoly


def inicializar_aleatoriedad(semilla: int) -> None:
    """
    Inicializa los generadores de aleatoriedad de Python y NumPy.

    Parameters
    ----------
    semilla:
        Semilla utilizada por los generadores disponibles en nuestro
        programa.

    Notes
    -----
    Topoly no expone directamente una semilla mediante la interfaz
    utilizada actualmente por este proyecto. Por tanto, todavía no
    afirmamos que esta función haga reproducibles exactamente las
    estructuras generadas internamente por Topoly.
    """

    random.seed(semilla)
    np.random.seed(semilla)


def normalizar_curva_cerrada(
    puntos: np.ndarray,
) -> np.ndarray:
    """
    Convierte una curva cerrada a nuestra representación interna.

    Si el primer y último punto son iguales, elimina la última copia.

    Por ejemplo:

        [v0, v1, v2, v3, v0]

    se convierte en:

        [v0, v1, v2, v3]

    Esto permite que una curva de N segmentos tenga exactamente N
    vértices almacenados.

    Parameters
    ----------
    puntos:
        Coordenadas de la curva.

    Returns
    -------
    numpy.ndarray
        Curva normalizada.
    """

    puntos = np.asarray(
        puntos,
        dtype=float,
    )

    if len(puntos) < 2:
        raise ValueError(
            "La curva debe contener al menos dos puntos."
        )

    # Algunas representaciones de curvas cerradas repiten el primer
    # punto al final. Lo eliminamos para trabajar internamente con
    # los vértices únicos.
    if np.allclose(
        puntos[0],
        puntos[-1],
    ):
        puntos = puntos[:-1]

    return puntos


def generar_poligono(
    numero_segmentos: int,
    longitud_segmento: float = 1.0,
) -> np.ndarray:
    """
    Genera un polígono cerrado equidistante.

    Parameters
    ----------
    numero_segmentos:
        Número de segmentos que tendrá el polígono.

    longitud_segmento:
        Longitud deseada para cada segmento.

    Returns
    -------
    numpy.ndarray
        Matriz de forma (N, 3), donde N es el número de segmentos.

    Notes
    -----
    La representación devuelta contiene únicamente los vértices
    únicos. El último segmento se interpreta como:

        último_vértice -> primer_vértice
    """

    if numero_segmentos < 3:
        raise ValueError(
            "El polígono debe tener al menos 3 segmentos."
        )

    if longitud_segmento <= 0:
        raise ValueError(
            "La longitud del segmento debe ser positiva."
        )

    estructuras = list(
        topoly.generate_loop(
            numero_segmentos,
            1,
            bond_length=longitud_segmento,
            print_with_index=False,
            output="list",
        )
    )

    if not estructuras:
        raise RuntimeError(
            "Topoly no devolvió ninguna estructura."
        )

    puntos = np.asarray(
        estructuras[0],
        dtype=float,
    )

    # ----------------------------------------------------------
    # Normalización de la representación cerrada
    # ----------------------------------------------------------

    puntos = normalizar_curva_cerrada(
        puntos
    )

    # ----------------------------------------------------------
    # Validación básica de la estructura recibida
    # ----------------------------------------------------------

    if puntos.ndim != 2 or puntos.shape[1] != 3:
        raise RuntimeError(
            "La estructura generada no tiene forma (N, 3). "
            f"Forma recibida: {puntos.shape}"
        )

    if len(puntos) != numero_segmentos:
        raise RuntimeError(
            "El número de vértices obtenido después de normalizar "
            "la curva no coincide con el número de segmentos "
            "solicitado. "
            f"Esperados: {numero_segmentos}. "
            f"Obtenidos: {len(puntos)}."
        )

    return puntos


def longitudes_segmentos(
    puntos: np.ndarray,
) -> np.ndarray:
    """
    Calcula las longitudes de todos los segmentos del polígono.

    El último segmento conecta explícitamente el último vértice con
    el primero.

    Si existen N vértices:

        v0 -> v1
        v1 -> v2
        ...
        v(N-2) -> v(N-1)
        v(N-1) -> v0

    Por tanto se obtienen exactamente N longitudes.
    """

    puntos = np.asarray(
        puntos,
        dtype=float,
    )

    if puntos.ndim != 2 or puntos.shape[1] != 3:
        raise ValueError(
            "Se esperaba una matriz de forma (N, 3)."
        )

    siguientes = np.roll(
        puntos,
        -1,
        axis=0,
    )

    diferencias = (
        siguientes - puntos
    )

    return np.linalg.norm(
        diferencias,
        axis=1,
    )


def validar_poligono(
    puntos: np.ndarray,
    longitud_esperada: float,
    tolerancia: float = 1e-8,
) -> dict:
    """
    Valida las propiedades geométricas básicas del polígono.

    Parameters
    ----------
    puntos:
        Coordenadas de los vértices.

    longitud_esperada:
        Longitud que debería tener cada segmento.

    tolerancia:
        Error máximo permitido.

    Returns
    -------
    dict
        Información de validación.
    """

    puntos = np.asarray(
        puntos,
        dtype=float,
    )

    longitudes = longitudes_segmentos(
        puntos
    )

    errores = np.abs(
        longitudes - longitud_esperada
    )

    return {
        "forma_correcta": (
            puntos.ndim == 2
            and puntos.shape[1] == 3
        ),
        "numero_segmentos": len(longitudes),
        "numero_vertices": len(puntos),
        "longitud_minima": float(
            longitudes.min()
        ),
        "longitud_maxima": float(
            longitudes.max()
        ),
        "longitud_media": float(
            longitudes.mean()
        ),
        "max_error_longitud": float(
            errores.max()
        ),
        "equidistante": bool(
            np.all(
                errores <= tolerancia
            )
        ),
        "todos_finitos": bool(
            np.all(
                np.isfinite(puntos)
            )
        ),
    }