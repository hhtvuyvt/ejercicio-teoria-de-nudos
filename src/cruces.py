"""
Detección de cruces en una proyección plana.

Cada segmento conserva además sus índices tridimensionales para poder
determinar posteriormente cuál rama pasa por encima y cuál por debajo.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Cruce:
    """
    Representa un cruce entre dos segmentos.

    segmento_a:
        Índice del primer segmento.

    segmento_b:
        Índice del segundo segmento.

    parametro_a:
        Posición del cruce dentro del segmento A.

    parametro_b:
        Posición del cruce dentro del segmento B.

    punto:
        Coordenadas 2D del cruce.

    altura_a:
        Coordenada en la dirección de observación de A.

    altura_b:
        Coordenada en la dirección de observación de B.
    """

    segmento_a: int
    segmento_b: int

    parametro_a: float
    parametro_b: float

    punto: np.ndarray

    altura_a: float
    altura_b: float

    @property
    def segmento_sobre(self) -> int:
        """
        Devuelve el segmento que está por encima.
        """

        if self.altura_a > self.altura_b:
            return self.segmento_a

        return self.segmento_b

    @property
    def segmento_bajo(self) -> int:
        """
        Devuelve el segmento que está por debajo.
        """

        if self.altura_a < self.altura_b:
            return self.segmento_a

        return self.segmento_b


def segmentos_adyacentes(
    indice_a: int,
    indice_b: int,
    numero_segmentos: int,
) -> bool:
    """
    Determina si dos segmentos son adyacentes.

    Los segmentos 0 y N-1 también son adyacentes porque la curva
    es cerrada.
    """

    if indice_a == indice_b:
        return True

    if (indice_a + 1) % numero_segmentos == indice_b:
        return True

    return (indice_b + 1) % numero_segmentos == indice_a


def interseccion_segmentos_2d(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    d: np.ndarray,
    tolerancia: float = 1e-10,
) -> tuple[float, float] | None:
    """
    Calcula la intersección de los segmentos AB y CD.

    Retorna:

        (t, u)

    si:

        A + t(B-A) = C + u(D-C)

    con:

        0 <= t <= 1
        0 <= u <= 1

    Si no existe una intersección transversal, devuelve None.
    """

    r = b - a
    s = d - c

    determinante = (
        r[0] * s[1]
        - r[1] * s[0]
    )

    if abs(determinante) <= tolerancia:
        return None

    diferencia = c - a

    t = (
        diferencia[0] * s[1]
        - diferencia[1] * s[0]
    ) / determinante

    u = (
        diferencia[0] * r[1]
        - diferencia[1] * r[0]
    ) / determinante

    if not (
        tolerancia < t < 1.0 - tolerancia
    ):
        return None

    if not (
        tolerancia < u < 1.0 - tolerancia
    ):
        return None

    return t, u


def detectar_cruces(
    puntos_2d: np.ndarray,
    puntos_3d: np.ndarray,
    tolerancia: float = 1e-10,
) -> list[Cruce]:
    """
    Detecta cruces transversales de la proyección.

    La altura de cada segmento se calcula interpolando su coordenada
    en la dirección de observación, que en esta primera implementación
    corresponde a Z.

    Para una proyección arbitraria, posteriormente generalizaremos
    esta parte utilizando la base completa de proyección.
    """

    puntos_2d = np.asarray(
        puntos_2d,
        dtype=float,
    )

    puntos_3d = np.asarray(
        puntos_3d,
        dtype=float,
    )

    numero_segmentos = len(
        puntos_2d
    )

    cruces = []

    for i in range(
        numero_segmentos
    ):
        i_siguiente = (
            i + 1
        ) % numero_segmentos

        a = puntos_2d[i]
        b = puntos_2d[i_siguiente]

        for j in range(
            i + 1,
            numero_segmentos,
        ):
            if segmentos_adyacentes(
                i,
                j,
                numero_segmentos,
            ):
                continue

            j_siguiente = (
                j + 1
            ) % numero_segmentos

            c = puntos_2d[j]
            d = puntos_2d[j_siguiente]

            resultado = interseccion_segmentos_2d(
                a,
                b,
                c,
                d,
                tolerancia,
            )

            if resultado is None:
                continue

            t, u = resultado

            punto = (
                a
                + t * (b - a)
            )

            altura_a = (
                puntos_3d[i, 2]
                + t
                * (
                    puntos_3d[
                        i_siguiente,
                        2,
                    ]
                    - puntos_3d[i, 2]
                )
            )

            altura_b = (
                puntos_3d[j, 2]
                + u
                * (
                    puntos_3d[
                        j_siguiente,
                        2,
                    ]
                    - puntos_3d[j, 2]
                )
            )

            cruces.append(
                Cruce(
                    segmento_a=i,
                    segmento_b=j,
                    parametro_a=t,
                    parametro_b=u,
                    punto=punto,
                    altura_a=float(
                        altura_a
                    ),
                    altura_b=float(
                        altura_b
                    ),
                )
            )

    return cruces