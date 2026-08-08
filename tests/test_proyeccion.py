"""
Pruebas para la proyección de curvas tridimensionales.
"""

import numpy as np

from src.proyeccion import proyectar


def test_proyeccion_xy_conserva_numero_de_puntos() -> None:
    """
    La proyección XY debe conservar el número de vértices.
    """

    puntos = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
        ]
    )

    resultado = proyectar(
        puntos,
        direccion=np.array([0.0, 0.0, 1.0])
    )

    assert resultado.shape == (3, 2)


def test_proyeccion_xy_no_depende_de_la_coordenada_z() -> None:
    """
    Al proyectar sobre un plano perpendicular al eje Z,
    cambiar únicamente la coordenada Z no debe cambiar
    la posición proyectada.
    """

    puntos = np.array(
        [
            [1.0, 2.0, 100.0],
            [1.0, 2.0, 200.0],
        ]
    )

    resultado = proyectar(
        puntos,
        direccion=np.array([0.0, 0.0, 1.0]),
    )

    assert np.allclose(
        resultado[0],
        resultado[1],
    )