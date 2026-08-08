"""
Herramienta de inspección de Topoly.

Se utiliza para conocer exactamente qué invariantes y funciones
están disponibles en la versión instalada de Topoly.
"""

import inspect

import topoly


def main() -> None:
    """Muestra las funciones relevantes disponibles en Topoly."""

    funciones = [
        "alexander",
        "jones",
        "conway",
        "homfly",
        "kauffman",
        "kauffman_bracket",
        "blmho",
        "yamada",
        "aps",
        "writhe",
    ]

    print("FUNCIONES DE TOPOLY")
    print("=" * 60)

    for nombre in funciones:
        funcion = getattr(
            topoly,
            nombre,
            None,
        )

        if funcion is None:
            print(f"{nombre:<20} NO DISPONIBLE")
            continue

        print(f"{nombre:<20} DISPONIBLE")
        print(
            inspect.signature(funcion)
        )

    print("=" * 60)


if __name__ == "__main__":
    main()