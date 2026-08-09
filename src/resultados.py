"""
Registro y análisis de resultados experimentales.

Este módulo se encarga exclusivamente de transformar las clasificaciones
obtenidas durante una simulación en información estadística y almacenarla
en archivos.

No genera nudos ni clasifica curvas.

La separación permite que posteriormente podamos reutilizar estas
funciones para comparar distribuciones P_n(K) y P_m(K).
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path


def calcular_distribucion(
    clasificaciones: Iterable[str],
) -> dict[str, dict[str, float | int]]:
    """
    Calcula la distribución experimental de tipos de nudo.

    Parameters
    ----------
    clasificaciones:
        Secuencia de identificadores de nudos obtenidos durante
        el experimento.

    Returns
    -------
    dict
        Diccionario cuya clave es el identificador del nudo y cuyo
        valor contiene:

        - cantidad: número de apariciones.
        - frecuencia: frecuencia relativa.

    Examples
    --------
    Si las clasificaciones son:

        ["0_1", "0_1", "3_1", "0_1"]

    el resultado será equivalente a:

        {
            "0_1": {
                "cantidad": 3,
                "frecuencia": 0.75,
            },
            "3_1": {
                "cantidad": 1,
                "frecuencia": 0.25,
            },
        }
    """

    clasificaciones_lista = list(clasificaciones)

    total = len(clasificaciones_lista)

    if total == 0:
        return {}

    conteos = Counter(clasificaciones_lista)

    return {
        tipo: {
            "cantidad": cantidad,
            "frecuencia": cantidad / total,
        }
        for tipo, cantidad in sorted(
            conteos.items(),
            key=lambda elemento: (-elemento[1], elemento[0]),
        )
    }


def crear_resultado_experimento(
    *,
    segmentos: int,
    muestras: int,
    longitud_segmento: float,
    semilla: int | None,
    max_cross: int,
    clasificaciones: Iterable[str],
) -> dict:
    """
    Construye la estructura completa que será almacenada.

    Esta estructura contiene tanto los parámetros del experimento como
    la distribución obtenida.
    """

    clasificaciones_lista = list(clasificaciones)

    distribucion = calcular_distribucion(
        clasificaciones_lista
    )

    return {
        "experimento": {
            "modelo": "poligono_cerrado_equidistante",
            "segmentos": segmentos,
            "muestras": muestras,
            "longitud_segmento": longitud_segmento,
            "semilla": semilla,
            "max_cross": max_cross,
        },
        "resultado": {
            "total_muestras": len(clasificaciones_lista),
            "distribucion": distribucion,
        },
        "metadatos": {
            "fecha_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        },
    }


def convertir_resultado_experimento(
    resultado_experimento: dict,
) -> dict:
    """
    Convierte el resultado de experimento.py al formato
    utilizado para almacenar resultados.
    """

    configuracion = resultado_experimento["configuracion"]

    clasificaciones = resultado_experimento[
        "clasificaciones"
    ]

    return crear_resultado_experimento(
        segmentos=configuracion["numero_segmentos"],
        muestras=configuracion["numero_muestras"],
        longitud_segmento=configuracion["longitud_segmento"],
        semilla=configuracion["semilla"],
        max_cross=configuracion["max_cross"],
        clasificaciones=clasificaciones,
    )


def guardar_json(
    resultado: dict,
    ruta: Path,
) -> None:
    """
    Guarda un resultado experimental en formato JSON.
    """

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ruta.open(
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            resultado,
            archivo,
            indent=4,
            ensure_ascii=False,
        )


def guardar_csv(
    resultado: dict,
    ruta: Path,
) -> None:
    """
    Guarda la distribución experimental en formato CSV.

    Cada fila representa un tipo de nudo.
    """

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    distribucion = resultado["resultado"]["distribucion"]

    with ruta.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow(
            [
                "tipo_nudo",
                "cantidad",
                "frecuencia",
            ]
        )

        for tipo, datos in distribucion.items():
            escritor.writerow(
                [
                    tipo,
                    datos["cantidad"],
                    datos["frecuencia"],
                ]
            )


def guardar_experimento(
    resultado: dict,
    directorio: str | Path = "resultados",
) -> tuple[Path, Path]:
    """
    Guarda un experimento tanto en JSON como en CSV.

    El nombre del archivo identifica los parámetros principales del
    experimento para facilitar su localización posterior.

    Returns
    -------
    tuple[Path, Path]
        Rutas del archivo JSON y del archivo CSV.
    """

    directorio = Path(directorio)

    configuracion = resultado["experimento"]

    segmentos = configuracion["segmentos"]
    muestras = configuracion["muestras"]
    semilla = configuracion["semilla"]

    semilla_texto = (
        str(semilla)
        if semilla is not None
        else "sin-seed"
    )

    nombre_base = (
        f"experimento_"
        f"n{segmentos}_"
        f"m{muestras}_"
        f"seed{semilla_texto}"
    )

    ruta_json = directorio / f"{nombre_base}.json"
    ruta_csv = directorio / f"{nombre_base}.csv"

    guardar_json(
        resultado,
        ruta_json,
    )

    guardar_csv(
        resultado,
        ruta_csv,
    )

    return ruta_json, ruta_csv


def imprimir_distribucion(
    distribucion: dict[str, dict[str, float | int]],
) -> None:
    """
    Imprime la distribución experimental en la terminal.
    """

    print()
    print("## DISTRIBUCIÓN EXPERIMENTAL")
    print()

    if not distribucion:
        print("No se obtuvieron clasificaciones.")
        return

    for tipo, datos in distribucion.items():
        print(
            f"{tipo:<10}"
            f"{datos['cantidad']:>10}"
            f"{datos['frecuencia']:>15.6f}"
        )