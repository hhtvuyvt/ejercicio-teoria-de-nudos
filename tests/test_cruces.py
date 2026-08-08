"""
Pruebas para la detección de cruces en proyecciones planas.
"""

import numpy as np

from src.cruces import (
    Cruce,
    detectar_cruces,
    interseccion_segmentos_2d,
    segmentos_adyacentes,
)

# ============================================================
# PRUEBAS DE ADYACENCIA
# ============================================================


def test_segmento_es_adyacente_a_si_mismo() -> None:
    """
    Un segmento debe considerarse adyacente a sí mismo.
    """

    assert segmentos_adyacentes(
        2,
        2,
        10,
    )


def test_segmentos_consecutivos_son_adyacentes() -> None:
    """
    Dos segmentos consecutivos deben considerarse adyacentes.
    """

    assert segmentos_adyacentes(
        2,
        3,
        10,
    )


def test_segmentos_adyacentes_en_cierre() -> None:
    """
    El primer y último segmento son adyacentes porque
    la curva es cerrada.
    """

    assert segmentos_adyacentes(
        0,
        9,
        10,
    )


def test_segmentos_no_adyacentes() -> None:
    """
    Dos segmentos separados deben no ser adyacentes.
    """

    assert not segmentos_adyacentes(
        0,
        5,
        10,
    )


# ============================================================
# PRUEBAS DE INTERSECCIÓN 2D
# ============================================================


def test_segmentos_que_se_cruzan() -> None:
    """
    Dos segmentos diagonales que se cruzan en su interior
    deben producir una intersección.
    """

    a = np.array([0.0, 0.0])
    b = np.array([1.0, 1.0])

    c = np.array([0.0, 1.0])
    d = np.array([1.0, 0.0])

    resultado = interseccion_segmentos_2d(
        a,
        b,
        c,
        d,
    )

    assert resultado is not None

    t, u = resultado

    assert np.isclose(t, 0.5)
    assert np.isclose(u, 0.5)


def test_segmentos_que_no_se_cruzan() -> None:
    """
    Dos segmentos separados no deben producir una intersección.
    """

    a = np.array([0.0, 0.0])
    b = np.array([1.0, 0.0])

    c = np.array([0.0, 1.0])
    d = np.array([1.0, 1.0])

    resultado = interseccion_segmentos_2d(
        a,
        b,
        c,
        d,
    )

    assert resultado is None


def test_segmentos_paralelos_no_se_cruzan() -> None:
    """
    Segmentos paralelos no deben producir una intersección
    transversal.
    """

    a = np.array([0.0, 0.0])
    b = np.array([1.0, 1.0])

    c = np.array([0.0, 1.0])
    d = np.array([1.0, 2.0])

    resultado = interseccion_segmentos_2d(
        a,
        b,
        c,
        d,
    )

    assert resultado is None


def test_interseccion_en_extremo_no_es_cruce() -> None:
    """
    Una intersección exactamente en un extremo no debe
    considerarse un cruce transversal.
    """

    a = np.array([0.0, 0.0])
    b = np.array([1.0, 0.0])

    c = np.array([1.0, 0.0])
    d = np.array([1.0, 1.0])

    resultado = interseccion_segmentos_2d(
        a,
        b,
        c,
        d,
    )

    assert resultado is None


# ============================================================
# PRUEBAS DE LA CLASE CRUCE
# ============================================================


def test_cruce_identifica_segmento_superior() -> None:
    """
    El segmento con mayor altura debe identificarse como
    el segmento que pasa por encima.
    """

    cruce = Cruce(
        segmento_a=2,
        segmento_b=7,
        parametro_a=0.5,
        parametro_b=0.5,
        punto=np.array([0.5, 0.5]),
        altura_a=2.0,
        altura_b=1.0,
    )

    assert cruce.segmento_sobre == 2
    assert cruce.segmento_bajo == 7


def test_cruce_identifica_segmento_inferior() -> None:
    """
    Si el segundo segmento tiene mayor altura, debe ser
    identificado como el segmento superior.
    """

    cruce = Cruce(
        segmento_a=2,
        segmento_b=7,
        parametro_a=0.5,
        parametro_b=0.5,
        punto=np.array([0.5, 0.5]),
        altura_a=1.0,
        altura_b=2.0,
    )

    assert cruce.segmento_sobre == 7
    assert cruce.segmento_bajo == 2


# ============================================================
# PRUEBAS DE DETECCIÓN DE CRUCES
# ============================================================


def test_detectar_cruces_sin_intersecciones() -> None:
    """
    Una colección de segmentos que no se cruzan debe producir
    una lista vacía.
    """

    puntos_2d = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [2.0, 0.0],
            [3.0, 0.0],
        ]
    )

    puntos_3d = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [2.0, 0.0, 2.0],
            [3.0, 0.0, 3.0],
        ]
    )

    cruces = detectar_cruces(
        puntos_2d,
        puntos_3d,
    )

    assert cruces == []


def test_detectar_un_cruce() -> None:
    """
    Una curva cerrada cuya proyección contiene un único cruce
    transversal debe producir exactamente un Cruce.
    """

    puntos_2d = np.array(
        [
            [-1.0, -1.0],
            [1.0, 1.0],
            [1.0, -1.0],
            [-1.0, 1.0],
        ]
    )

    puntos_3d = np.array(
        [
            [-1.0, -1.0, 0.0],
            [1.0, 1.0, 2.0],
            [1.0, -1.0, 0.0],
            [-1.0, 1.0, 1.0],
        ]
    )

    cruces = detectar_cruces(
        puntos_2d,
        puntos_3d,
    )

    assert len(cruces) == 1

    cruce = cruces[0]

    assert np.allclose(
        cruce.punto,
        [0.0, 0.0],
    )

    assert np.isclose(
        cruce.parametro_a,
        0.5,
    )

    assert np.isclose(
        cruce.parametro_b,
        0.5,
    )


def test_detectar_cruces_ignora_segmentos_adyacentes() -> None:
    """
    Los segmentos que comparten un vértice no deben contarse
    como cruces.
    """

    puntos_2d = np.array(
        [
            [0.0, 0.0],
            [1.0, 1.0],
            [2.0, 0.0],
            [1.0, -1.0],
        ]
    )

    puntos_3d = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0],
            [2.0, 0.0, 2.0],
            [1.0, -1.0, 3.0],
        ]
    )

    cruces = detectar_cruces(
        puntos_2d,
        puntos_3d,
    )

    assert cruces == []