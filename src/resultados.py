"""
Persistencia de resultados experimentales.

Este módulo se encarga únicamente de guardar y cargar los resultados
de las simulaciones de nudos.

La estadística y el análisis de probabilidades se implementarán
posteriormente en un módulo separado.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DIRECTORIO_RESULTADOS = Path("resultados")


def guardar_resultado(
    resultado: dict[str, Any],
    nombre_archivo: str,
    directorio: Path = DIRECTORIO_RESULTADOS,
) -> Path:
    """
    Guarda un resultado experimental en formato JSON.

    Parámetros
    ----------
    resultado:
        Diccionario que contiene los datos del experimento.

    nombre_archivo:
        Nombre del archivo JSON que se creará.

    directorio:
        Directorio donde se guardará el resultado.

    Retorna
    -------
    Path
        Ruta completa del archivo creado.
    """

    directorio.mkdir(
        parents=True,
        exist_ok=True,
    )

    datos = dict(resultado)

    datos.setdefault(
        "fecha",
        datetime.now(timezone.utc).isoformat(),
    )

    ruta = directorio / nombre_archivo

    with ruta.open(
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False,
        )

    return ruta


def cargar_resultado(
    ruta: Path,
) -> dict[str, Any]:
    """
    Carga un resultado experimental desde un archivo JSON.

    Parámetros
    ----------
    ruta:
        Ruta del archivo JSON.

    Retorna
    -------
    dict[str, Any]
        Datos almacenados en el archivo.
    """

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        datos = json.load(archivo)

    return datos


def generar_nombre_experimento(
    segmentos: int,
    muestras: int,
    semilla: int | None,
) -> str:
    """
    Genera un nombre reproducible para un experimento.

    Ejemplo
    -------
    experimento_n20_m10000_seed12345.json
    """

    if semilla is None:
        identificador_semilla = "sin_semilla"
    else:
        identificador_semilla = f"seed{semilla}"

    return (
        f"experimento_"
        f"n{segmentos}_"
        f"m{muestras}_"
        f"{identificador_semilla}.json"
    )