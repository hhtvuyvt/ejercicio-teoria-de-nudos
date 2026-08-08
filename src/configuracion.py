"""
Configuración del experimento de nudos aleatorios.
"""

from dataclasses import dataclass


@dataclass
class Configuracion:
    """
    Parámetros utilizados durante una ejecución.

    Atributos
    ----------
    numero_segmentos:
        Número de segmentos del polígono.

    numero_muestras:
        Cantidad de polígonos que se generarán.

    longitud_segmento:
        Longitud de cada segmento.

    semilla:
        Semilla registrada para el experimento.

    mostrar_grafica:
        Indica si se debe mostrar la primera muestra.

    max_cross:
        Límite de cruces utilizado durante la clasificación.
    """

    numero_segmentos: int = 20
    numero_muestras: int = 1
    longitud_segmento: float = 1.0
    semilla: int = 12345
    mostrar_grafica: bool = True
    max_cross: int = 15

    def validar(self) -> None:
        """Comprueba que la configuración sea válida."""

        if self.numero_segmentos < 3:
            raise ValueError(
                "El número de segmentos debe ser al menos 3."
            )

        if self.numero_muestras < 1:
            raise ValueError(
                "El número de muestras debe ser al menos 1."
            )

        if self.longitud_segmento <= 0:
            raise ValueError(
                "La longitud de cada segmento debe ser positiva."
            )

        if self.max_cross < 1:
            raise ValueError(
                "max_cross debe ser positivo."
            )