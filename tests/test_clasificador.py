"""
Pruebas para la clasificación topológica de nudos.

Estas pruebas verifican tanto el comportamiento de nuestra función
clasificar_nudo() como su comunicación con Topoly.
"""

import numpy as np
import pytest

from src import clasificador
from tests.geometria_conocida import (
    nudo_trivial,
    trefoil,
)

# ============================================================
# DATOS DE PRUEBA
# ============================================================


def poligono_simple() -> np.ndarray:
    """
    Devuelve un polígono cerrado sencillo.

    La geometría se utiliza únicamente para comprobar que la función
    recibe y transmite correctamente los datos hacia Topoly.
    """

    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
        ]
    )


# ============================================================
# PRUEBAS DE LA INTERFAZ DEL CLASIFICADOR
# ============================================================


def test_clasificar_nudo_devuelve_resultado_de_topoly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    clasificar_nudo() debe devolver directamente el resultado
    producido por Topoly.
    """

    resultado_esperado = "0_1"

    def fake_alexander(*args, **kwargs):
        return resultado_esperado

    monkeypatch.setattr(
        clasificador.topoly,
        "alexander",
        fake_alexander,
    )

    resultado = clasificador.clasificar_nudo(
        poligono_simple()
    )

    assert resultado == resultado_esperado


def test_clasificador_envia_la_curva_a_topoly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    La misma geometría recibida por clasificar_nudo() debe ser
    enviada a Topoly.
    """

    puntos = poligono_simple()

    argumentos = {}

    def fake_alexander(*args, **kwargs):
        argumentos["args"] = args
        argumentos["kwargs"] = kwargs
        return "0_1"

    monkeypatch.setattr(
        clasificador.topoly,
        "alexander",
        fake_alexander,
    )

    clasificador.clasificar_nudo(puntos)

    assert len(argumentos["args"]) >= 1
    assert np.array_equal(
        argumentos["args"][0],
        puntos,
    )


def test_clasificador_utiliza_cierre_cerrado(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Nuestro modelo genera una curva cerrada, por lo que el
    clasificador debe utilizar Closure.CLOSED.
    """

    argumentos = {}

    def fake_alexander(*args, **kwargs):
        argumentos["kwargs"] = kwargs
        return "0_1"

    monkeypatch.setattr(
        clasificador.topoly,
        "alexander",
        fake_alexander,
    )

    clasificador.clasificar_nudo(
        poligono_simple()
    )

    assert (
        argumentos["kwargs"]["closure"]
        == clasificador.Closure.CLOSED
    )


def test_clasificador_utiliza_kmt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    El clasificador debe utilizar KMT como método de reducción,
    tal como definimos en nuestro modelo actual.
    """

    argumentos = {}

    def fake_alexander(*args, **kwargs):
        argumentos["kwargs"] = kwargs
        return "0_1"

    monkeypatch.setattr(
        clasificador.topoly,
        "alexander",
        fake_alexander,
    )

    clasificador.clasificar_nudo(
        poligono_simple()
    )

    assert (
        argumentos["kwargs"]["reduce_method"]
        == clasificador.ReduceMethod.KMT
    )


def test_clasificador_transmite_max_cross(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    max_cross debe transmitirse a Topoly sin modificarlo.
    """

    argumentos = {}

    def fake_alexander(*args, **kwargs):
        argumentos["kwargs"] = kwargs
        return "0_1"

    monkeypatch.setattr(
        clasificador.topoly,
        "alexander",
        fake_alexander,
    )

    clasificador.clasificar_nudo(
        poligono_simple(),
        max_cross=25,
    )

    assert argumentos["kwargs"]["max_cross"] == 25


# ============================================================
# PRUEBAS DE MANEJO DE ERRORES
# ============================================================
def test_clasificador_propaga_error_de_topoly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Si Topoly produce una excepción, el clasificador no debe
    ocultarla silenciosamente.
    """

    def fake_alexander(*args, **kwargs):
        raise RuntimeError(
            "Error simulado de Topoly"
        )

    monkeypatch.setattr(
        clasificador.topoly,
        "alexander",
        fake_alexander,
    )

    with pytest.raises(
        RuntimeError,
        match="Error simulado de Topoly",
    ):
        clasificador.clasificar_nudo(
            poligono_simple()
        )


def test_clasificador_reconoce_nudo_trivial() -> None:
    """
    Una circunferencia plana debe clasificarse como el nudo trivial 0_1.
    """

    puntos = nudo_trivial()

    resultado = clasificador.clasificar_nudo(
        puntos
    )

    assert resultado == "0_1"


def test_clasificador_reconoce_trefoil() -> None:
    """
    Una representación conocida del trefoil debe clasificarse
    como el nudo 3_1.
    """

    puntos = trefoil()

    resultado = clasificador.clasificar_nudo(
        puntos
    )

    assert resultado == "3_1"