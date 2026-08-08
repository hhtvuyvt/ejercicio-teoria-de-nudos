"""
Visualización tridimensional y bidimensional de los nudos.

Este módulo no realiza ninguna operación matemática sobre la
topología del nudo. Su única responsabilidad es representar
gráficamente los objetos generados por el experimento.
"""

from __future__ import annotations

from typing import Any, cast

import matplotlib.pyplot as plt
import numpy as np


def mostrar_poligono(
    puntos: np.ndarray,
    titulo: str = "Polígono cerrado equidistante",
) -> None:
    """
    Muestra una poligonal cerrada en tres dimensiones.

    Parameters
    ----------
    puntos:
        Matriz N x 3 con las coordenadas de los vértices.

    titulo:
        Título de la gráfica.
    """

    puntos = np.asarray(
        puntos,
        dtype=float,
    )

    # Añadimos nuevamente el primer punto para representar
    # explícitamente el cierre de la cuerda.
    puntos_cerrados = np.vstack(
        [
            puntos,
            puntos[0],
        ]
    )

    figura = plt.figure(
        figsize=(9, 7)
    )

    eje = cast(
        Any,
        figura.add_subplot(
            111,
            projection="3d",
        ),
    )

    # Curva cerrada.
    eje.plot(
        puntos_cerrados[:, 0],
        puntos_cerrados[:, 1],
        puntos_cerrados[:, 2],
        linewidth=1.5,
    )

    # Vértices.
    #
    # Usamos argumentos con nombre para evitar que Pylance
    # confunda el tercer argumento de scatter() con otra
    # sobrecarga de la función.
    eje.scatter(
        puntos[:, 0],
        puntos[:, 1],
        puntos[:, 2],
        s=12,
    )

    # Marcamos el primer vértice.
    eje.scatter(
        np.array([puntos[0, 0]]),
        np.array([puntos[0, 1]]),
        np.array([puntos[0, 2]]),
        s=60,
        label="Punto inicial",
    )

    eje.set_xlabel("X")
    eje.set_ylabel("Y")
    eje.set_zlabel("Z")

    eje.set_title(
        titulo
    )

    eje.legend()

    plt.tight_layout()
    plt.show()


def mostrar_proyeccion(
    puntos_2d: np.ndarray,
    cruces,
    titulo: str = "Diagrama proyectado",
) -> None:
    """
    Muestra la proyección plana de la curva y sus cruces.

    Parameters
    ----------
    puntos_2d:
        Matriz N x 2 con las coordenadas proyectadas.

    cruces:
        Lista de objetos Cruce generados por el detector.

    titulo:
        Título de la gráfica.
    """

    puntos_2d = np.asarray(
        puntos_2d,
        dtype=float,
    )

    # Cerramos visualmente la poligonal.
    puntos_cerrados = np.vstack(
        [
            puntos_2d,
            puntos_2d[0],
        ]
    )

    _figura, eje = plt.subplots(
        figsize=(9, 7)
    )

    # Dibujamos la curva proyectada.
    eje.plot(
        puntos_cerrados[:, 0],
        puntos_cerrados[:, 1],
        linewidth=1.5,
    )

    # Dibujamos los vértices.
    eje.scatter(
        puntos_2d[:, 0],
        puntos_2d[:, 1],
        s=12,
    )

    # Dibujamos cada cruce encontrado.
    for numero, cruce in enumerate(
        cruces,
        start=1,
    ):
        eje.scatter(
            [cruce.punto[0]],
            [cruce.punto[1]],
            s=60,
        )

        eje.text(
            cruce.punto[0],
            cruce.punto[1],
            f" {numero}",
            fontsize=10,
        )

    # La escala de X e Y debe ser igual.
    # De lo contrario un círculo podría verse como una elipse.
    eje.set_aspect(
        "equal",
        adjustable="box",
    )

    eje.set_title(
        titulo
    )

    eje.set_xlabel("X")
    eje.set_ylabel("Y")

    plt.tight_layout()
    plt.show()