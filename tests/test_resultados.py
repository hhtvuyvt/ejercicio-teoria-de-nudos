from pathlib import Path

from src.resultados import (
    cargar_resultado,
    generar_nombre_experimento,
    guardar_resultado,
)


def test_generar_nombre_experimento() -> None:
    nombre = generar_nombre_experimento(
        segmentos=20,
        muestras=10000,
        semilla=12345,
    )

    assert nombre == (
        "experimento_n20_m10000_seed12345.json"
    )


def test_generar_nombre_sin_semilla() -> None:
    nombre = generar_nombre_experimento(
        segmentos=20,
        muestras=100,
        semilla=None,
    )

    assert nombre == (
        "experimento_n20_m100_sin_semilla.json"
    )


def test_guardar_y_cargar_resultado(
    tmp_path: Path,
) -> None:
    resultado = {
        "modelo": "Polígono cerrado equidistante",
        "segmentos": 20,
        "muestras": 100,
        "semilla": 12345,
        "distribucion": {
            "0_1": 95,
            "3_1": 5,
        },
    }

    ruta = guardar_resultado(
        resultado,
        "prueba.json",
        directorio=tmp_path,
    )

    assert ruta.exists()

    recuperado = cargar_resultado(ruta)

    assert recuperado["modelo"] == (
        "Polígono cerrado equidistante"
    )
    assert recuperado["segmentos"] == 20
    assert recuperado["muestras"] == 100
    assert recuperado["semilla"] == 12345
    assert recuperado["distribucion"] == {
        "0_1": 95,
        "3_1": 5,
    }