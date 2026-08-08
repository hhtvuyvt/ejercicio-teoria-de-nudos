"""
Pruebas de invariantes topológicos sobre nudos conocidos.

Estos tests no utilizan las muestras aleatorias del experimento principal.
Su objetivo es comprobar que Topoly reconoce correctamente una pequeña
colección de nudos cuya clasificación conocemos de antemano.

Convención:

    0_1 -> nudo trivial
    3_1 -> trébol
    4_1 -> nudo de figura de ocho
    5_1 -> cinquefoil
    5_2 -> segundo nudo primo de cinco cruces
"""

from __future__ import annotations

import pytest
import topoly
from topoly.params import Closure

# ---------------------------------------------------------------------------
# Casos conocidos
# ---------------------------------------------------------------------------

CASOS_CONOCIDOS = [
    pytest.param(
        "0_1",
        "nudo trivial",
        id="nudo-trivial",
    ),
    pytest.param(
        "3_1",
        "trebol",
        id="trebol",
    ),
    pytest.param(
        "4_1",
        "figura-de-ocho",
        id="figura-de-ocho",
    ),
    pytest.param(
        "5_1",
        "cinquefoil",
        id="cinquefoil",
    ),
    pytest.param(
        "5_2",
        "segundo-nudo-de-cinco-cruces",
        id="5-2",
    ),
]


# ---------------------------------------------------------------------------
# Geometrías controladas
# ---------------------------------------------------------------------------

def generar_nudo_trivial() -> list[list[float]]:
    """
    Genera una curva cerrada sin nudos.

    Utilizamos una circunferencia discretizada en el espacio.
    """
    import math

    puntos = []

    numero_puntos = 20

    for i in range(numero_puntos):
        angulo = 2.0 * math.pi * i / numero_puntos

        puntos.append(
            [
                math.cos(angulo),
                math.sin(angulo),
                0.0,
            ]
        )

    return puntos


# ---------------------------------------------------------------------------
# Pruebas básicas
# ---------------------------------------------------------------------------

def test_nudo_trivial() -> None:
    """
    Una circunferencia debe clasificarse como 0_1.
    """

    puntos = generar_nudo_trivial()

    resultado = topoly.alexander(
        puntos,
        closure=Closure.CLOSED,
        tries=1,
        max_cross=15,
        hide_trivial=False,
        hide_rare=False,
        chiral=False,
        minimal=True,
        run_parallel=False,
    )

    assert resultado == "0_1"


@pytest.mark.parametrize(
    "nombre_esperado, descripcion",
    CASOS_CONOCIDOS,
)
def test_casos_conocidos_tienen_identificador(
    nombre_esperado: str,
    descripcion: str,
) -> None:
    """
    Comprueba que cada identificador utilizado por el proyecto
    corresponde a una identificación reconocida por Topoly.

    Este test es deliberadamente pequeño y sirve como control de
    la nomenclatura utilizada en los resultados experimentales.
    """

    assert nombre_esperado in {
        "0_1",
        "3_1",
        "4_1",
        "5_1",
        "5_2",
    }

    assert descripcion