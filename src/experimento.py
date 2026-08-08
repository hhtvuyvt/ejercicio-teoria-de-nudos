"""
Ejecución de experimentos y cálculo de frecuencias.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict

from .clasificador import clasificar_nudo
from .configuracion import Configuracion
from .generador import (
    generar_poligono,
    inicializar_aleatoriedad,
    validar_poligono,
)


def ejecutar_experimento(
    configuracion: Configuracion,
) -> dict:
    """
    Genera y clasifica múltiples polígonos.

    Retorna un diccionario con:

    - configuración;
    - número de apariciones de cada tipo;
    - probabilidades experimentales;
    - información de cada muestra.
    """

    configuracion.validar()

    inicializar_aleatoriedad(
        configuracion.semilla
    )

    conteos = Counter()
    muestras = []

    for indice in range(
        configuracion.numero_muestras
    ):
        puntos = generar_poligono(
            configuracion.numero_segmentos,
            configuracion.longitud_segmento,
        )

        validacion = validar_poligono(
            puntos,
            configuracion.longitud_segmento,
        )

        if not validacion["forma_correcta"]:
            raise RuntimeError(
                "La estructura generada no tiene forma (N, 3)."
            )

        if not validacion["todos_finitos"]:
            raise RuntimeError(
                "La estructura contiene valores no finitos."
            )

        if not validacion["equidistante"]:
            raise RuntimeError(
                "La estructura no cumple la condición de "
                "segmentos equidistantes."
            )

        tipo = clasificar_nudo(
            puntos,
            max_cross=configuracion.max_cross,
        )

        tipo_texto = str(tipo)

        conteos[tipo_texto] += 1

        muestras.append(
            {
                "indice": indice,
                "tipo_nudo": tipo_texto,
                "longitud_minima": (
                    validacion["longitud_minima"]
                ),
                "longitud_maxima": (
                    validacion["longitud_maxima"]
                ),
            }
        )

    total = configuracion.numero_muestras

    probabilidades = {
        tipo: conteo / total
        for tipo, conteo in conteos.items()
    }

    return {
        "configuracion": asdict(
            configuracion
        ),
        "conteos": dict(conteos),
        "probabilidades": probabilidades,
        "muestras": muestras,
    }