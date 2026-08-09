"""
Ejecución automatizada de múltiples experimentos.

Este módulo coordina varias ejecuciones del experimento estadístico
sin repetir manualmente los comandos de principal.py.

No genera nudos directamente ni realiza análisis estadístico.
"""

from __future__ import annotations

from pathlib import Path

from .configuracion import Configuracion
from .experimento import ejecutar_experimento
from .resultados import convertir_resultado_experimento, guardar_experimento


def ejecutar_bateria(
    configuraciones: list[Configuracion],
    directorio: str | Path = "resultados",
) -> list[dict]:
    """
    Ejecuta una batería de experimentos y guarda sus resultados.

    Parameters
    ----------
    configuraciones:
        Lista de configuraciones que se ejecutarán.

    directorio:
        Directorio donde se almacenarán los resultados.

    Returns
    -------
    list[dict]
        Lista de resultados experimentales.

    Raises
    ------
    ValueError
        Si la lista de configuraciones está vacía.
    """

    if not configuraciones:
        raise ValueError(
            "La batería debe contener al menos "
            "una configuración."
        )

    resultados = []

    for configuracion in configuraciones:
        configuracion.validar()

        print()
        print("=" * 60)
        print("EJECUTANDO EXPERIMENTO")
        print("=" * 60)

        print(
            f"Segmentos: {configuracion.numero_segmentos}"
        )
        print(
            f"Muestras:  {configuracion.numero_muestras}"
        )
        print(
            f"Semilla:   {configuracion.semilla}"
        )

        resultado = ejecutar_experimento(
            configuracion
        )

        resultado_guardable = convertir_resultado_experimento(
            resultado
        )

        rutas = guardar_experimento(
            resultado_guardable,
            directorio=directorio,
        )

        print(
            f"JSON: {rutas[0]}"
        )
        print(
            f"CSV:  {rutas[1]}"
        )

        resultados.append(resultado)

    return resultados


def construir_bateria_inicial() -> list[Configuracion]:
    """
    Construye la primera batería experimental.

    Se utilizan 20 segmentos y diferentes tamaños de muestra
    para estudiar la estabilidad de la distribución experimental.
    """

    muestras = [
        100,
        1_000,
        10_000,
        100_000,
    ]

    return [
        Configuracion(
            numero_segmentos=20,
            numero_muestras=numero_muestras,
            longitud_segmento=1.0,
            semilla=12345,
            mostrar_grafica=False,
            max_cross=15,
        )
        for numero_muestras in muestras
    ]


def main() -> None:
    """
    Punto de entrada para ejecutar la batería inicial.
    """

    configuraciones = construir_bateria_inicial()

    ejecutar_bateria(
        configuraciones
    )


if __name__ == "__main__":
    main()