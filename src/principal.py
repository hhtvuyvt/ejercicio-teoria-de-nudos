"""
Punto de entrada principal del experimento de nudos.

Este módulo coordina:

1. La configuración del experimento.
2. La generación de un polígono cerrado equidistante.
3. La validación geométrica.
4. La proyección de la curva 3D sobre un plano 2D.
5. La detección de cruces en la proyección.
6. La visualización de la curva y su diagrama proyectado.
7. La ejecución del experimento estadístico.
8. El registro de los resultados experimentales.
"""

from __future__ import annotations

import argparse

from .configuracion import Configuracion
from .cruces import detectar_cruces
from .experimento import ejecutar_experimento
from .generador import (
    generar_poligono,
    inicializar_aleatoriedad,
    validar_poligono,
)
from .proyeccion import proyectar
from .resultados import (
    crear_resultado_experimento,
    guardar_experimento,
)
from .visualizacion import (
    mostrar_poligono,
    mostrar_proyeccion,
)


def construir_parser() -> argparse.ArgumentParser:
    """
    Construye el parser de argumentos de línea de comandos.

    Returns
    -------
    argparse.ArgumentParser
        Parser utilizado por el programa principal.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Experimento con polígonos cerrados "
            "equidistantes y nudos."
        )
    )

    parser.add_argument(
        "--segmentos",
        type=int,
        default=20,
        help="Número de segmentos del polígono.",
    )

    parser.add_argument(
        "--muestras",
        type=int,
        default=1,
        help="Número de muestras que se generarán.",
    )

    parser.add_argument(
        "--longitud",
        type=float,
        default=1.0,
        help="Longitud de cada segmento.",
    )

    parser.add_argument(
        "--semilla",
        type=int,
        default=12345,
        help="Semilla registrada para el experimento.",
    )

    parser.add_argument(
        "--max-cross",
        type=int,
        default=15,
        help=(
            "Número máximo de cruces utilizado "
            "por el clasificador."
        ),
    )

    parser.add_argument(
        "--sin-grafica",
        action="store_true",
        help="No mostrar las gráficas.",
    )

    parser.add_argument(
        "--guardar",
        type=str,
        default="resultados",
        help=(
            "Directorio donde se guardarán los "
            "resultados JSON y CSV."
        ),
    )

    return parser


def mostrar_informacion_configuracion(
    configuracion: Configuracion,
) -> None:
    """
    Muestra en consola la configuración utilizada.
    """

    print("=" * 60)
    print("EXPERIMENTO DE NUDOS ALEATORIOS")
    print("=" * 60)
    print()

    print("Modelo:")
    print("  Polígono cerrado equidistante")
    print()

    print(
        f"Segmentos:          "
        f"{configuracion.numero_segmentos}"
    )

    print(
        f"Muestras:           "
        f"{configuracion.numero_muestras}"
    )

    print(
        f"Longitud:           "
        f"{configuracion.longitud_segmento}"
    )

    print(
        f"Semilla registrada: "
        f"{configuracion.semilla}"
    )

    print(
        f"Máximo de cruces:   "
        f"{configuracion.max_cross}"
    )

    print()


def analizar_primera_muestra(
    configuracion: Configuracion,
) -> None:
    """
    Genera y analiza una primera muestra.

    Esta función se utiliza para inspeccionar visualmente
    el objeto antes de ejecutar el experimento estadístico
    completo.

    El flujo es:

        3D
         ↓
        validación
         ↓
        proyección 2D
         ↓
        detección de cruces
         ↓
        visualización
    """

    inicializar_aleatoriedad(
        configuracion.semilla
    )

    # ----------------------------------------------------------
    # 1. GENERACIÓN
    # ----------------------------------------------------------

    primera_muestra = generar_poligono(
        configuracion.numero_segmentos,
        configuracion.longitud_segmento,
    )

    # ----------------------------------------------------------
    # 2. VALIDACIÓN GEOMÉTRICA
    # ----------------------------------------------------------

    validacion = validar_poligono(
        primera_muestra,
        configuracion.longitud_segmento,
    )

    print(
        "VALIDACIÓN DE LA PRIMERA MUESTRA"
    )

    print("-" * 60)

    print(
        f"Forma correcta:   "
        f"{validacion['forma_correcta']}"
    )

    print(
        f"Segmentos:        "
        f"{validacion['numero_segmentos']}"
    )

    print(
        f"Longitud mínima:  "
        f"{validacion['longitud_minima']:.12f}"
    )

    print(
        f"Longitud máxima:  "
        f"{validacion['longitud_maxima']:.12f}"
    )

    print(
        f"Longitud media:   "
        f"{validacion['longitud_media']:.12f}"
    )

    print(
        f"Error máximo:     "
        f"{validacion['max_error_longitud']:.12e}"
    )

    print(
        f"Equidistante:     "
        f"{validacion['equidistante']}"
    )

    print(
        f"Valores finitos:  "
        f"{validacion['todos_finitos']}"
    )

    print()

    # ----------------------------------------------------------
    # VALIDACIÓN
    # ----------------------------------------------------------

    if not validacion["forma_correcta"]:
        raise RuntimeError(
            "La estructura generada no tiene "
            "forma (N, 3)."
        )

    if not validacion["todos_finitos"]:
        raise RuntimeError(
            "La estructura contiene valores no finitos."
        )

    if not validacion["equidistante"]:
        raise RuntimeError(
            "La estructura no cumple la condición "
            "de segmentos equidistantes."
        )

    # ----------------------------------------------------------
    # 3. PROYECCIÓN 3D → 2D
    # ----------------------------------------------------------

    puntos_2d = proyectar(
        primera_muestra
    )

    print(
        "PROYECCIÓN"
    )

    print("-" * 60)

    print(
        "La curva tridimensional ha sido proyectada "
        "sobre el plano XY."
    )

    print(
        f"Puntos proyectados: "
        f"{len(puntos_2d)}"
    )

    print()

    # ----------------------------------------------------------
    # 4. DETECCIÓN DE CRUCES
    # ----------------------------------------------------------

    cruces = detectar_cruces(
        puntos_2d,
        primera_muestra,
    )

    print(
        "CRUCES DETECTADOS"
    )

    print("-" * 60)

    print(
        f"Número de cruces proyectados: "
        f"{len(cruces)}"
    )

    print()

    if cruces:

        for numero, cruce in enumerate(
            cruces,
            start=1,
        ):
            print(
                f"Cruce {numero}:"
            )

            print(
                f"  Segmentos: "
                f"{cruce.segmento_a} "
                f"y "
                f"{cruce.segmento_b}"
            )

            print(
                f"  Posición A: "
                f"{cruce.parametro_a:.6f}"
            )

            print(
                f"  Posición B: "
                f"{cruce.parametro_b:.6f}"
            )

            print(
                f"  Altura A: "
                f"{cruce.altura_a:.6f}"
            )

            print(
                f"  Altura B: "
                f"{cruce.altura_b:.6f}"
            )

            print(
                f"  Segmento sobre: "
                f"{cruce.segmento_sobre}"
            )

            print(
                f"  Segmento bajo: "
                f"{cruce.segmento_bajo}"
            )

            print()

    else:

        print(
            "No se encontraron cruces "
            "en esta proyección."
        )

        print()

    # ----------------------------------------------------------
    # 5. VISUALIZACIÓN
    # ----------------------------------------------------------

    mostrar_poligono(
        primera_muestra,
        titulo=(
            "Polígono cerrado "
            "equidistante en R³"
        ),
    )

    mostrar_proyeccion(
        puntos_2d,
        cruces,
        titulo=(
            "Proyección y cruces "
            "del diagrama"
        ),
    )


def mostrar_distribucion(
    resultado: dict,
) -> None:
    """
    Muestra en consola la distribución experimental obtenida.
    """

    print()
    print(
        "DISTRIBUCIÓN EXPERIMENTAL"
    )

    print("-" * 60)

    probabilidades = resultado[
        "probabilidades"
    ]

    conteos = resultado[
        "conteos"
    ]

    if not probabilidades:
        print(
            "No se obtuvieron resultados."
        )
        return

    elementos = sorted(
        probabilidades.items(),
        key=lambda elemento: elemento[1],
        reverse=True,
    )

    for tipo, probabilidad in elementos:

        conteo = conteos[tipo]

        print(
            f"{tipo:30s}"
            f"{conteo:8d}"
            f"  "
            f"{probabilidad:.6f}"
        )


def registrar_resultado(
    resultado: dict,
    configuracion: Configuracion,
    directorio: str,
) -> None:
    """
    Convierte y guarda el resultado del experimento.

    Se generan dos archivos:

    - JSON: información completa del experimento.
    - CSV: distribución experimental.
    """

    clasificaciones = [
        muestra["tipo_nudo"]
        for muestra in resultado["muestras"]
    ]

    resultado_archivo = crear_resultado_experimento(
        segmentos=configuracion.numero_segmentos,
        muestras=configuracion.numero_muestras,
        longitud_segmento=(
            configuracion.longitud_segmento
        ),
        semilla=configuracion.semilla,
        max_cross=configuracion.max_cross,
        clasificaciones=clasificaciones,
    )

    ruta_json, ruta_csv = guardar_experimento(
        resultado_archivo,
        directorio=directorio,
    )

    print()
    print("=" * 60)
    print("RESULTADOS REGISTRADOS")
    print("=" * 60)
    print()
    print(
        f"JSON: {ruta_json}"
    )
    print(
        f"CSV:  {ruta_csv}"
    )


def main() -> None:
    """
    Función principal del programa.
    """

    parser = construir_parser()

    argumentos = parser.parse_args()

    # ----------------------------------------------------------
    # CONFIGURACIÓN
    # ----------------------------------------------------------

    configuracion = Configuracion(
        numero_segmentos=argumentos.segmentos,
        numero_muestras=argumentos.muestras,
        longitud_segmento=argumentos.longitud,
        semilla=argumentos.semilla,
        mostrar_grafica=not argumentos.sin_grafica,
        max_cross=argumentos.max_cross,
    )

    configuracion.validar()

    # ----------------------------------------------------------
    # INFORMACIÓN INICIAL
    # ----------------------------------------------------------

    mostrar_informacion_configuracion(
        configuracion
    )

    # ----------------------------------------------------------
    # ANÁLISIS VISUAL
    # ----------------------------------------------------------

    if configuracion.mostrar_grafica:

        analizar_primera_muestra(
            configuracion
        )

    # ----------------------------------------------------------
    # EXPERIMENTO ESTADÍSTICO
    # ----------------------------------------------------------

    resultado = ejecutar_experimento(
        configuracion
    )

    # ----------------------------------------------------------
    # RESULTADOS EN TERMINAL
    # ----------------------------------------------------------

    mostrar_distribucion(
        resultado
    )

    # ----------------------------------------------------------
    # REGISTRO DEL EXPERIMENTO
    # ----------------------------------------------------------

    registrar_resultado(
        resultado,
        configuracion,
        argumentos.guardar,
    )


if __name__ == "__main__":
    main()