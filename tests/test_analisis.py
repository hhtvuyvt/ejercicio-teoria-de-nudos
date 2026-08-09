from pathlib import Path

import pytest

from src.analisis import (
    cargar_resultado,
    comparar_distribuciones,
    extraer_configuracion,
    extraer_distribucion,
    extraer_evolucion,
    graficar_evolucion,
    listar_resultados,
    resumir_resultados,
)


def crear_resultado_prueba(
    ruta: Path,
    *,
    segmentos: int = 20,
    muestras: int = 100,
    semilla: int = 12345,
) -> None:
    """
    Crea un archivo JSON mínimo para las pruebas.
    """

    contenido = {
        "experimento": {
            "modelo": "poligono_cerrado_equidistante",
            "segmentos": segmentos,
            "muestras": muestras,
            "longitud_segmento": 1.0,
            "semilla": semilla,
            "max_cross": 15,
        },
        "resultado": {
            "total_muestras": muestras,
            "distribucion": {
                "0_1": {
                    "cantidad": 95,
                    "frecuencia": 0.95,
                },
                "3_1": {
                    "cantidad": 5,
                    "frecuencia": 0.05,
                },
            },
        },
        "metadatos": {
            "fecha_utc": "2026-01-01T00:00:00+00:00",
        },
    }

    import json

    ruta.write_text(
        json.dumps(
            contenido,
            indent=4,
        ),
        encoding="utf-8",
    )


def test_cargar_resultado(
    tmp_path: Path,
) -> None:
    """
    Verifica que un resultado JSON puede cargarse.
    """

    ruta = (
        tmp_path
        / "resultado.json"
    )

    crear_resultado_prueba(
        ruta
    )

    resultado = cargar_resultado(
        ruta
    )

    assert resultado[
        "experimento"
    ][
        "segmentos"
    ] == 20

    assert resultado[
        "resultado"
    ][
        "total_muestras"
    ] == 100


def test_cargar_resultado_archivo_inexistente(
    tmp_path: Path,
) -> None:
    """
    Cargar un archivo inexistente debe producir
    FileNotFoundError.
    """

    ruta = (
        tmp_path
        / "no_existe.json"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        cargar_resultado(
            ruta
        )


def test_extraer_distribucion() -> None:
    """
    Verifica que se extraen correctamente las
    frecuencias experimentales.
    """

    resultado = {
        "resultado": {
            "distribucion": {
                "0_1": {
                    "cantidad": 95,
                    "frecuencia": 0.95,
                },
                "3_1": {
                    "cantidad": 5,
                    "frecuencia": 0.05,
                },
            }
        }
    }

    distribucion = (
        extraer_distribucion(
            resultado
        )
    )

    assert distribucion == {
        "0_1": 0.95,
        "3_1": 0.05,
    }


def test_extraer_configuracion() -> None:
    """
    Verifica que se obtiene correctamente la
    configuración del experimento.
    """

    resultado = {
        "experimento": {
            "segmentos": 20,
            "muestras": 100,
            "semilla": 12345,
        }
    }

    configuracion = (
        extraer_configuracion(
            resultado
        )
    )

    assert configuracion[
        "segmentos"
    ] == 20

    assert configuracion[
        "muestras"
    ] == 100

    assert configuracion[
        "semilla"
    ] == 12345


def test_listar_resultados(
    tmp_path: Path,
) -> None:
    """
    Verifica que solamente se encuentran
    archivos JSON de resultados.
    """

    crear_resultado_prueba(
        tmp_path
        / "resultado_a.json"
    )

    crear_resultado_prueba(
        tmp_path
        / "resultado_b.json"
    )

    (
        tmp_path
        / "no_es_resultado.txt"
    ).write_text(
        "archivo de prueba",
        encoding="utf-8",
    )

    resultados = listar_resultados(
        tmp_path
    )

    assert len(resultados) == 2

    assert all(
        ruta.suffix == ".json"
        for ruta in resultados
    )


def test_listar_resultados_directorio_inexistente(
    tmp_path: Path,
) -> None:
    """
    Un directorio inexistente debe devolver
    una lista vacía.
    """

    directorio = (
        tmp_path
        / "no_existe"
    )

    resultados = listar_resultados(
        directorio
    )

    assert resultados == []


def test_resumir_resultados(
    tmp_path: Path,
) -> None:
    """
    Verifica que varios resultados pueden
    convertirse en un resumen.
    """

    ruta = (
        tmp_path
        / "resultado.json"
    )

    crear_resultado_prueba(
        ruta,
        segmentos=20,
        muestras=100,
        semilla=12345,
    )

    resumen = resumir_resultados(
        [ruta]
    )

    assert len(resumen) == 1

    experimento = resumen[0]

    assert experimento[
        "segmentos"
    ] == 20

    assert experimento[
        "muestras"
    ] == 100

    assert experimento[
        "semilla"
    ] == 12345

    assert experimento[
        "distribucion"
    ] == {
        "0_1": 0.95,
        "3_1": 0.05,
    }


def test_resumir_varios_resultados(
    tmp_path: Path,
) -> None:
    """
    Verifica que pueden analizarse varios
    experimentos simultáneamente.
    """

    ruta_1 = (
        tmp_path
        / "resultado_1.json"
    )

    ruta_2 = (
        tmp_path
        / "resultado_2.json"
    )

    crear_resultado_prueba(
        ruta_1,
        muestras=100,
    )

    crear_resultado_prueba(
        ruta_2,
        muestras=1000,
    )

    resumen = resumir_resultados(
        [
            ruta_1,
            ruta_2,
        ]
    )

    assert len(resumen) == 2

    assert resumen[0][
        "muestras"
    ] == 100

    assert resumen[1][
        "muestras"
    ] == 1000   


def test_comparar_distribuciones_rellena_tipos_faltantes() -> None:
    resumen = [
        {
            "segmentos": 20,
            "muestras": 100,
            "semilla": 12345,
            "distribucion": {
                "0_1": 0.95,
                "3_1": 0.05,
            },
        },
        {
            "segmentos": 20,
            "muestras": 1000,
            "semilla": 12345,
            "distribucion": {
                "0_1": 0.97,
                "3_1": 0.027,
                "4_1": 0.002,
                "TMC": 0.001,
            },
        },
    ]

    comparacion = comparar_distribuciones(
        resumen
    )

    assert len(comparacion) == 2

    assert comparacion[0]["0_1"] == 0.95
    assert comparacion[0]["3_1"] == 0.05
    assert comparacion[0]["4_1"] == 0.0
    assert comparacion[0]["TMC"] == 0.0

    assert comparacion[1]["0_1"] == 0.97
    assert comparacion[1]["3_1"] == 0.027
    assert comparacion[1]["4_1"] == 0.002
    assert comparacion[1]["TMC"] == 0.001


def test_extraer_evolucion() -> None:
    comparacion = [
        {
            "segmentos": 20,
            "muestras": 1000,
            "semilla": 12345,
            "0_1": 0.97,
            "3_1": 0.027,
        },
        {
            "segmentos": 20,
            "muestras": 100,
            "semilla": 12345,
            "0_1": 0.95,
            "3_1": 0.05,
        },
    ]

    evolucion = extraer_evolucion(
        comparacion,
        "0_1",
    )

    assert evolucion == [
        (100, 0.95),
        (1000, 0.97),
    ]


def test_graficar_evolucion_sin_datos() -> None:
    graficar_evolucion(
        [],
        "0_1",
    )