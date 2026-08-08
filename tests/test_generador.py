"""
Pruebas para la generación y validación de polígonos.
"""

import numpy as np
import pytest

from src.generador import (
    generar_poligono,
    longitudes_segmentos,
    normalizar_curva_cerrada,
    validar_poligono,
)


def test_generar_poligono_tiene_numero_correcto_de_vertices() -> None:
    """
    Un polígono de N segmentos debe tener N vértices únicos.
    """

    puntos = generar_poligono(
        numero_segmentos=20,
        longitud_segmento=1.0,
    )

    assert puntos.shape == (20, 3)


def test_generar_poligono_es_equilongitud() -> None:
    """
    Todos los segmentos deben tener la longitud solicitada.
    """

    puntos = generar_poligono(
        numero_segmentos=20,
        longitud_segmento=1.0,
    )

    longitudes = longitudes_segmentos(
        puntos
    )

    assert len(longitudes) == 20
    assert np.allclose(
        longitudes,
        1.0,
    )


def test_generar_poligono_es_finito() -> None:
    """
    Todas las coordenadas deben ser números finitos.
    """

    puntos = generar_poligono(
        numero_segmentos=20,
        longitud_segmento=1.0,
    )

    assert np.all(
        np.isfinite(puntos)
    )


def test_normalizar_elimina_punto_final_duplicado() -> None:
    """
    Una curva representada como:

        v0, v1, v2, v0

    debe convertirse en:

        v0, v1, v2
    """

    puntos = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0],
        ]
    )

    resultado = normalizar_curva_cerrada(
        puntos
    )

    assert resultado.shape == (3, 3)

    assert np.array_equal(
        resultado[0],
        resultado[-1],
    ) is False


def test_normalizar_no_elimina_puntos_distintos() -> None:
    """
    Si el primer y último punto son diferentes,
    la función no debe eliminar el último punto.
    """

    puntos = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
        ]
    )

    resultado = normalizar_curva_cerrada(
        puntos
    )

    assert resultado.shape == (3, 3)


def test_validar_poligono_confirma_equilongitud() -> None:
    """
    La validación debe reconocer un polígono correctamente generado.
    """

    puntos = generar_poligono(
        numero_segmentos=20,
        longitud_segmento=1.0,
    )

    resultado = validar_poligono(
        puntos,
        longitud_esperada=1.0,
    )

    assert resultado["forma_correcta"] is True
    assert resultado["numero_segmentos"] == 20
    assert resultado["numero_vertices"] == 20
    assert resultado["equidistante"] is True
    assert resultado["todos_finitos"] is True


def test_numero_segmentos_invalido() -> None:
    """
    No se debe permitir un polígono con menos de tres segmentos.
    """

    with pytest.raises(ValueError):
        generar_poligono(
            numero_segmentos=2,
            longitud_segmento=1.0,
        )


def test_longitud_invalida() -> None:
    """
    La longitud de segmento debe ser positiva.
    """

    with pytest.raises(ValueError):
        generar_poligono(
            numero_segmentos=20,
            longitud_segmento=0.0,
        )