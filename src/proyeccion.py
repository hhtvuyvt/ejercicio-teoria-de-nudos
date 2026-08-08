"""
Proyección de una curva poligonal tridimensional sobre un plano 2D.

La proyección es necesaria porque un diagrama de nudo se obtiene al
observar la curva espacial desde una dirección determinada.

Una buena dirección de proyección debe evitar casos degenerados como:

- varios vértices proyectándose exactamente sobre el mismo punto;
- un segmento proyectándose sobre otro;
- tres o más segmentos participando en el mismo cruce.
"""

from __future__ import annotations

import numpy as np


def normalizar(vector: np.ndarray) -> np.ndarray:
    """
    Devuelve el vector normalizado.

    Parameters
    ----------
    vector:
        Vector tridimensional.

    Returns
    -------
    numpy.ndarray
        Vector unitario.
    """

    vector = np.asarray(
        vector,
        dtype=float,
    )

    norma = np.linalg.norm(vector)

    if norma == 0:
        raise ValueError(
            "No se puede normalizar el vector cero."
        )

    return vector / norma


def construir_base_proyeccion(
    direccion: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Construye una base ortonormal adaptada a una dirección de observación.

    La dirección indica hacia dónde estamos mirando.

    Retorna:

        eje_x,
        eje_y,
        eje_z

    donde eje_z coincide con la dirección de observación.
    """

    eje_z = normalizar(direccion)

    # Elegimos un vector auxiliar que no sea paralelo
    # a la dirección de observación.
    if abs(eje_z[0]) < 0.9:
        auxiliar = np.array(
            [1.0, 0.0, 0.0]
        )
    else:
        auxiliar = np.array(
            [0.0, 1.0, 0.0]
        )

    eje_x = np.cross(
        auxiliar,
        eje_z,
    )

    eje_x = normalizar(
        eje_x
    )

    eje_y = np.cross(
        eje_z,
        eje_x,
    )

    eje_y = normalizar(
        eje_y
    )

    return eje_x, eje_y, eje_z


def proyectar(
    puntos: np.ndarray,
    direccion: np.ndarray | None = None,
) -> np.ndarray:
    """
    Proyecta una curva 3D sobre un plano 2D.

    Parameters
    ----------
    puntos:
        Matriz N x 3 con las coordenadas tridimensionales.

    direccion:
        Dirección desde la que observamos la curva.

        Si no se proporciona, usamos el eje Z.

    Returns
    -------
    numpy.ndarray
        Matriz N x 2 con las coordenadas proyectadas.
    """

    puntos = np.asarray(
        puntos,
        dtype=float,
    )

    if puntos.ndim != 2 or puntos.shape[1] != 3:
        raise ValueError(
            "Se esperaba una matriz de forma (N, 3)."
        )

    if direccion is None:
        direccion = np.array(
            [0.0, 0.0, 1.0]
        )

    eje_x, eje_y, _ = construir_base_proyeccion(
        direccion
    )

    coordenadas_x = puntos @ eje_x
    coordenadas_y = puntos @ eje_y

    return np.column_stack(
        [
            coordenadas_x,
            coordenadas_y,
        ]
    )