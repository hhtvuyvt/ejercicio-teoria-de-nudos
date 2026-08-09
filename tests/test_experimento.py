from src.configuracion import Configuracion
from src.experimento import ejecutar_experimento


def test_experimento_conserva_clasificaciones() -> None:
    configuracion = Configuracion(
        numero_segmentos=20,
        numero_muestras=5,
        longitud_segmento=1.0,
        semilla=12345,
        max_cross=15,
        mostrar_grafica=False,
    )

    resultado = ejecutar_experimento(
        configuracion
    )

    clasificaciones = resultado[
        "clasificaciones"
    ]

    assert len(clasificaciones) == 5

    assert all(
        isinstance(tipo, str)
        for tipo in clasificaciones
    )


def test_conteos_coinciden_con_clasificaciones() -> None:
    configuracion = Configuracion(
        numero_segmentos=20,
        numero_muestras=20,
        longitud_segmento=1.0,
        semilla=12345,
        max_cross=15,
        mostrar_grafica=False,
    )

    resultado = ejecutar_experimento(
        configuracion
    )

    clasificaciones = resultado[
        "clasificaciones"
    ]

    conteos = resultado["conteos"]

    assert sum(conteos.values()) == len(
        clasificaciones
    )

    assert len(clasificaciones) == 20