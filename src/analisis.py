"""
Análisis de resultados experimentales de nudos.

Este módulo lee los resultados almacenados por resultados.py y permite
comparar diferentes experimentos sin volver a ejecutar las simulaciones.

Funciones principales:

- cargar_resultado:
    Carga un archivo JSON de resultados.

- listar_resultados:
    Encuentra los resultados disponibles en un directorio.

- extraer_distribucion:
    Obtiene las frecuencias de los tipos de nudo.

- resumir_resultados:
    Construye una tabla resumida de varios experimentos.

- graficar_distribucion:
    Genera una gráfica de las frecuencias experimentales.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt


def cargar_resultado(
    ruta: str | Path,
) -> dict:
    """
    Carga un resultado experimental desde un archivo JSON.
    """

    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo de resultados: {ruta}"
        )

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(archivo)


def listar_resultados(
    directorio: str | Path = "resultados",
) -> list[Path]:
    """
    Devuelve los archivos JSON de resultados disponibles.

    Los archivos se ordenan por número de segmentos y, dentro de
    cada cantidad de segmentos, por número de muestras.
    """

    directorio = Path(directorio)

    if not directorio.exists():
        return []

    archivos = list(
        directorio.glob("*.json")
    )

    def clave_orden(ruta: Path) -> tuple[int, int]:
        resultado = cargar_resultado(ruta)
        configuracion = extraer_configuracion(
            resultado
        )

        return (
            int(configuracion["segmentos"]),
            int(configuracion["muestras"]),
        )

    return sorted(
        archivos,
        key=clave_orden,
    )


def extraer_distribucion(
    resultado: dict,
) -> dict[str, float]:
    """
    Extrae las frecuencias de los tipos de nudo.

    Parameters
    ----------
    resultado:
        Resultado cargado desde JSON.

    Returns
    -------
    dict[str, float]
        Diccionario con la frecuencia de cada tipo de nudo.
    """

    distribucion = resultado[
        "resultado"
    ][
        "distribucion"
    ]

    return {
        tipo: float(datos["frecuencia"])
        for tipo, datos in distribucion.items()
    }


def extraer_configuracion(
    resultado: dict,
) -> dict:
    """
    Extrae la configuración del experimento.
    """

    return resultado[
        "experimento"
    ]


def resumir_resultados(
    rutas: Sequence[str | Path],
) -> list[dict]:
    """
    Construye un resumen de varios experimentos.

    Cada elemento contiene:

    - segmentos;
    - muestras;
    - semilla;
    - distribución.
    """

    resumen = []

    for ruta in rutas:

        resultado = cargar_resultado(
            ruta
        )

        configuracion = extraer_configuracion(
            resultado
        )

        distribucion = extraer_distribucion(
            resultado
        )

        resumen.append(
            {
                "segmentos": configuracion[
                    "segmentos"
                ],
                "muestras": configuracion[
                    "muestras"
                ],
                "semilla": configuracion[
                    "semilla"
                ],
                "distribucion": distribucion,
            }
        )

    return resumen


def comparar_distribuciones(
    resumen: list[dict],
) -> list[dict]:
    """
    Construye una tabla comparativa de las distribuciones.

    Cada fila representa un experimento y contiene:

    - segmentos;
    - muestras;
    - semilla;
    - frecuencia de cada tipo de nudo.

    Los tipos de nudo que no aparecen en un experimento reciben
    frecuencia 0.0.
    """

    if not resumen:
        return []

    tipos = sorted(
        {
            tipo
            for experimento in resumen
            for tipo in experimento["distribucion"]
        }
    )

    comparacion = []

    for experimento in resumen:

        fila = {
            "segmentos": experimento["segmentos"],
            "muestras": experimento["muestras"],
            "semilla": experimento["semilla"],
        }

        distribucion = experimento[
            "distribucion"
        ]

        for tipo in tipos:
            fila[tipo] = distribucion.get(
                tipo,
                0.0,
            )

        comparacion.append(fila)

    return comparacion


def extraer_evolucion(
    comparacion: list[dict],
    tipo_nudo: str,
) -> list[tuple[int, float]]:
    """
    Extrae la evolución de la frecuencia de un tipo de nudo.

    Cada elemento de la lista contiene:

    - número de muestras;
    - frecuencia experimental.

    Los resultados se ordenan por número de muestras.
    """

    evolucion = []

    for experimento in comparacion:
        frecuencia = float(
            experimento.get(
                tipo_nudo,
                0.0,
            )
        )

        evolucion.append(
            (
                int(experimento["muestras"]),
                frecuencia,
            )
        )

    return sorted(
        evolucion,
        key=lambda elemento: elemento[0],
    )


def graficar_evolucion(
    evolucion: list[tuple[int, float]],
    tipo_nudo: str,
) -> None:
    """
    Genera una gráfica de la frecuencia de un tipo de nudo
    en función del número de muestras.
    """

    if not evolucion:
        print(
            "No hay datos para generar la gráfica."
        )
        return

    muestras = [
        elemento[0]
        for elemento in evolucion
    ]

    frecuencias = [
        elemento[1]
        for elemento in evolucion
    ]

    figura, eje = plt.subplots()

    eje.plot(
        muestras,
        frecuencias,
        marker="o",
    )

    eje.set_title(
        f"Evolución experimental de {tipo_nudo}"
    )

    eje.set_xlabel(
        "Número de muestras"
    )

    eje.set_ylabel(
        "Frecuencia experimental"
    )

    eje.set_xscale("log")
    eje.set_ylim(0, 1)

    eje.grid(True)

    figura.tight_layout()

    plt.show()


def imprimir_resumen(
    resumen: list[dict],
) -> None:
    """
    Imprime un resumen de los experimentos.
    """

    if not resumen:
        print(
            "No hay resultados para analizar."
        )
        return

    print()
    print(
        "ANÁLISIS DE RESULTADOS"
    )
    print(
        "=" * 70
    )

    for experimento in resumen:

        print()

        print(
            f"Segmentos: "
            f"{experimento['segmentos']}"
        )

        print(
            f"Muestras:  "
            f"{experimento['muestras']}"
        )

        print(
            f"Semilla:   "
            f"{experimento['semilla']}"
        )

        print()

        distribucion = experimento[
            "distribucion"
        ]

        for tipo, frecuencia in sorted(
            distribucion.items(),
            key=lambda elemento: (
                -elemento[1],
                elemento[0],
            ),
        ):
            print(
                f"  {tipo:<10}"
                f"{frecuencia:>12.6%}"
            )


def graficar_distribucion(
    resultado: dict,
    titulo: str = (
        "Distribución experimental de nudos"
    ),
) -> None:
    """
    Genera una gráfica de barras de la distribución.

    La gráfica muestra la frecuencia experimental
    de cada tipo de nudo.
    """

    distribucion = extraer_distribucion(
        resultado
    )

    if not distribucion:
        print(
            "No hay datos para generar la gráfica."
        )
        return

    tipos = list(
        distribucion.keys()
    )

    frecuencias = [
        distribucion[tipo]
        for tipo in tipos
    ]

    figura, eje = plt.subplots()

    eje.bar(
        tipos,
        frecuencias,
    )

    eje.set_title(
        titulo
    )

    eje.set_xlabel(
        "Tipo de nudo"
    )

    eje.set_ylabel(
        "Frecuencia experimental"
    )

    eje.set_ylim(
        0,
        1,
    )

    figura.tight_layout()

    plt.show()


def main() -> None:
    """
    Punto de entrada del módulo de análisis.
    """

    rutas = listar_resultados()

    if not rutas:
        print(
            "No se encontraron resultados "
            "en la carpeta 'resultados'."
        )
        return

    resumen = resumir_resultados(
        rutas
    )

    imprimir_resumen(
        resumen
    )

    # Para comenzar utilizamos el último
    # resultado disponible.
    resultado = cargar_resultado(
        rutas[-1]
    )

    graficar_distribucion(
        resultado
    )


if __name__ == "__main__":
    main()