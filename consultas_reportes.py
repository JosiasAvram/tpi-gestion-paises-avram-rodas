"""
consultas_reportes.py
---------------------
Módulo CONSULTAS Y REPORTES del Trabajo Práctico Integrador.
Autor: Josías Alexis Avram

Responsabilidades de este módulo:
    - Búsqueda de países por nombre (coincidencia parcial).
    - Filtros: por continente, por rango de población y por rango de superficie.
    - Ordenamientos: por nombre, población o superficie (ascendente o descendente).
    - Estadísticas: país con mayor/menor población, promedios y conteo por continente.

Trabaja sobre la estructura definida en 'core_datos.py':
una LISTA de DICCIONARIOS, donde cada país tiene las claves:
    "nombre", "poblacion", "superficie", "continente".

Nota: las funciones de filtro y ordenamiento NO modifican la lista original,
devuelven una lista nueva con el resultado.
"""


# ==========================================================================
#  UTILIDAD PARA MOSTRAR RESULTADOS
# ==========================================================================

def mostrar_paises(paises):
    """
    Imprime por consola una tabla simple con la lista de países recibida.
    Si la lista está vacía, avisa que no hay resultados.
    """
    if not paises:
        print("  (No hay países para mostrar.)")
        return

    # Encabezado de la tabla.
    print(f"\n{'NOMBRE':<20}{'POBLACIÓN':>15}{'SUPERFICIE (km²)':>20}  CONTINENTE")
    print("-" * 72)
    for pais in paises:
        print(f"{pais['nombre']:<20}"
            f"{pais['poblacion']:>15,}"
            f"{pais['superficie']:>20,}"
            f"  {pais['continente']}")
    print("-" * 72)
    print(f"Total: {len(paises)} país(es).\n")


# ==========================================================================
#  BÚSQUEDA POR NOMBRE
# ==========================================================================

def buscar_por_nombre(paises, texto):
    """
    Busca países cuyo nombre CONTENGA el texto ingresado (coincidencia parcial,
    sin distinguir mayúsculas/minúsculas).

    Al ser parcial, también cubre la búsqueda exacta: si se escribe el nombre
    completo (ej. "argentina"), igualmente lo encuentra.

    Devuelve una lista nueva con los países encontrados.
    """
    texto = texto.strip().lower()
    resultado = []
    for pais in paises:
        if texto in pais["nombre"].lower():
            resultado.append(pais)
    return resultado


# ==========================================================================
#  FILTROS
# ==========================================================================

def filtrar_por_continente(paises, continente):
    """
    Devuelve los países cuyo continente coincide (sin distinguir mayúsculas).
    """
    continente = continente.strip().lower()
    return [p for p in paises if p["continente"].lower() == continente]


def filtrar_por_rango_poblacion(paises, minimo, maximo):
    """
    Devuelve los países cuya población está dentro del rango [minimo, maximo]
    (ambos incluidos).
    """
    return [p for p in paises if minimo <= p["poblacion"] <= maximo]


def filtrar_por_rango_superficie(paises, minimo, maximo):
    """
    Devuelve los países cuya superficie está dentro del rango [minimo, maximo]
    (ambos incluidos).
    """
    return [p for p in paises if minimo <= p["superficie"] <= maximo]


def continentes_disponibles(paises):
    """
    Devuelve una lista ordenada con los nombres de continentes presentes
    en los datos. Útil para mostrarle opciones al usuario.
    """
    continentes = set()
    for pais in paises:
        continentes.add(pais["continente"])
    return sorted(continentes)


# ==========================================================================
#  ORDENAMIENTOS
# ==========================================================================

def ordenar_paises(paises, criterio="nombre", ascendente=True):
    """
    Devuelve una lista NUEVA ordenada según el criterio elegido.

    Parámetros:
        criterio   -> "nombre", "poblacion" o "superficie".
        ascendente -> True (menor a mayor / A-Z) o False (mayor a menor / Z-A).

    Si el criterio no es válido, avisa y devuelve la lista sin ordenar (copia).
    """
    criterios_validos = ("nombre", "poblacion", "superficie")
    if criterio not in criterios_validos:
        print(f"[ERROR] Criterio de orden inválido: '{criterio}'. "
            f"Use uno de {criterios_validos}.")
        return list(paises)

    if criterio == "nombre":
        # Para el nombre ordenamos sin distinguir mayúsculas/minúsculas.
        clave = lambda p: p["nombre"].lower()
    else:
        clave = lambda p: p[criterio]

    # reverse=True ordena de mayor a menor (descendente).
    return sorted(paises, key=clave, reverse=not ascendente)


# ==========================================================================
#  ESTADÍSTICAS
# ==========================================================================

def pais_mayor_poblacion(paises):
    """Devuelve el país con MAYOR población, o None si la lista está vacía."""
    if not paises:
        return None
    return max(paises, key=lambda p: p["poblacion"])


def pais_menor_poblacion(paises):
    """Devuelve el país con MENOR población, o None si la lista está vacía."""
    if not paises:
        return None
    return min(paises, key=lambda p: p["poblacion"])


def promedio_poblacion(paises):
    """Devuelve el promedio de población. 0 si la lista está vacía."""
    if not paises:
        return 0
    total = sum(p["poblacion"] for p in paises)
    return total / len(paises)


def promedio_superficie(paises):
    """Devuelve el promedio de superficie. 0 si la lista está vacía."""
    if not paises:
        return 0
    total = sum(p["superficie"] for p in paises)
    return total / len(paises)


def conteo_por_continente(paises):
    """
    Devuelve un diccionario {continente: cantidad_de_paises}.
    """
    conteo = {}
    for pais in paises:
        continente = pais["continente"]
        conteo[continente] = conteo.get(continente, 0) + 1
    return conteo


def mostrar_estadisticas(paises):
    """
    Calcula y muestra por consola TODAS las estadísticas pedidas en la consigna:
        - País con mayor y menor población.
        - Promedio de población y de superficie.
        - Cantidad de países por continente.
    """
    print("\n--- ESTADÍSTICAS ---")
    if not paises:
        print("  No hay datos cargados para calcular estadísticas.")
        return

    mayor = pais_mayor_poblacion(paises)
    menor = pais_menor_poblacion(paises)

    print(f"País con MAYOR población: {mayor['nombre']} ({mayor['poblacion']:,} hab.)")
    print(f"País con MENOR población: {menor['nombre']} ({menor['poblacion']:,} hab.)")
    print(f"Promedio de población : {promedio_poblacion(paises):,.2f} hab.")
    print(f"Promedio de superficie: {promedio_superficie(paises):,.2f} km²")

    print("\nCantidad de países por continente:")
    for continente, cantidad in sorted(conteo_por_continente(paises).items()):
        print(f"  - {continente}: {cantidad}")
    print()
