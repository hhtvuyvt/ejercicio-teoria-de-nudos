import csv
import json
from pathlib import Path

from src.resultados import (
    calcular_distribucion,
    crear_resultado_experimento,
    guardar_csv,
    guardar_experimento,
    guardar_json,
)


def test_calcular_distribucion() -> None:
    clasificaciones = [
        "0_1",
        "0_1",
        "3_1",
        "0_1",
    ]

    resultado = calcular_distribucion(
        clasificaciones
    )

    assert resultado == {
        "0_1": {
            "cantidad": 3,
            "frecuencia": 0.75,
        },
        "3_1": {
            "cantidad": 1,
            "frecuencia": 0.25,
        },
    }


def test_calcular_distribucion_vacia() -> None:
    resultado = calcular_distribucion([])

    assert resultado == {}


def test_crear_resultado_experimento() -> None:
    resultado = crear_resultado_experimento(
        segmentos=20,
        muestras=100,
        longitud_segmento=1.0,
        semilla=12345,
        max_cross=15,
        clasificaciones=[
            "0_1",
            "0_1",
            "3_1",
        ],
    )

    assert resultado["experimento"]["segmentos"] == 20
    assert resultado["experimento"]["muestras"] == 100
    assert resultado["experimento"]["semilla"] == 12345

    assert resultado["resultado"]["total_muestras"] == 3

    assert resultado["resultado"]["distribucion"] == {
        "0_1": {
            "cantidad": 2,
            "frecuencia": 2 / 3,
        },
        "3_1": {
            "cantidad": 1,
            "frecuencia": 1 / 3,
        },
    }

    assert "fecha_utc" in resultado["metadatos"]


def test_guardar_json(
    tmp_path: Path,
) -> None:
    resultado = crear_resultado_experimento(
        segmentos=20,
        muestras=100,
        longitud_segmento=1.0,
        semilla=12345,
        max_cross=15,
        clasificaciones=[
            "0_1",
            "3_1",
        ],
    )

    ruta = tmp_path / "resultado.json"

    guardar_json(
        resultado,
        ruta,
    )

    assert ruta.exists()

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        recuperado = json.load(archivo)

    assert recuperado == resultado


def test_guardar_csv(
    tmp_path: Path,
) -> None:
    resultado = crear_resultado_experimento(
        segmentos=20,
        muestras=100,
        longitud_segmento=1.0,
        semilla=12345,
        max_cross=15,
        clasificaciones=[
            "0_1",
            "0_1",
            "3_1",
        ],
    )

    ruta = tmp_path / "resultado.csv"

    guardar_csv(
        resultado,
        ruta,
    )

    assert ruta.exists()

    with ruta.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as archivo:
        filas = list(
            csv.DictReader(archivo)
        )

    assert filas[0]["tipo_nudo"] == "0_1"
    assert filas[0]["cantidad"] == "2"

    assert filas[1]["tipo_nudo"] == "3_1"
    assert filas[1]["cantidad"] == "1"


def test_guardar_experimento(
    tmp_path: Path,
) -> None:
    resultado = crear_resultado_experimento(
        segmentos=20,
        muestras=100,
        longitud_segmento=1.0,
        semilla=12345,
        max_cross=15,
        clasificaciones=[
            "0_1",
            "3_1",
        ],
    )

    ruta_json, ruta_csv = guardar_experimento(
        resultado,
        tmp_path,
    )

    assert ruta_json.exists()
    assert ruta_csv.exists()

    assert (
        ruta_json.name
        == "experimento_n20_m100_seed12345.json"
    )

    assert (
        ruta_csv.name
        == "experimento_n20_m100_seed12345.csv"
    )