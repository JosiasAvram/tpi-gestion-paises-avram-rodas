"""
main.py
-------
Programa principal del Trabajo Práctico Integrador.
"Gestión de Datos de Países en Python: filtros, ordenamientos y estadísticas".

Integrantes:
    - Josías Alexis Avram  -> módulo consultas_reportes.py
    - Noelia Maricel Rodas -> módulo core_datos.py

Este archivo solo se encarga de mostrar el MENÚ de consola y de conectar
las funciones de los dos módulos. Toda la lógica vive en:
    - core_datos.py        (carga del CSV, alta/modificación, validaciones)
    - consultas_reportes.py (búsquedas, filtros, ordenamientos, estadísticas)
"""

import core_datos as core
import consultas_reportes as cr

# Nombre del archivo de datos que se carga al iniciar y donde se guardan los cambios.
ARCHIVO_CSV = "paises.csv"


# ==========================================================================
#  SUBMENÚES (para opciones con varias alternativas)
# ==========================================================================

def menu_buscar(paises):
    """Búsqueda por nombre (coincidencia parcial, mínimo 3 caracteres)."""
    print("\n--- BUSCAR POR NOMBRE ---")

    # Pedimos el texto y exigimos al menos 3 caracteres.
    # Si no cumple, avisamos y volvemos a pedir (bucle hasta que sea válido).
    while True:
        texto = input("Texto a buscar (mínimo 3 letras): ").strip()
        if len(texto) >= 3:
            break
        print("  -> Debe ingresar al menos 3 caracteres.")

    resultado = cr.buscar_por_nombre(paises, texto)
    cr.mostrar_paises(resultado)


def menu_filtrar(paises):
    """Submenú de filtros: continente, rango de población, rango de superficie."""
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    opcion = core.validar_texto("Elija una opción: ")

    if opcion == "1":
        disponibles = cr.continentes_disponibles(paises)
        print(f"Continentes disponibles: {', '.join(disponibles)}")
        continente = core.validar_texto("Continente: ")
        resultado = cr.filtrar_por_continente(paises, continente)
        cr.mostrar_paises(resultado)

    elif opcion == "2":
        minimo = core.validar_entero_positivo("Población mínima: ")
        maximo = core.validar_entero_positivo("Población máxima: ")
        if minimo > maximo:
            print("[ERROR] El mínimo no puede ser mayor que el máximo.")
            return
        resultado = cr.filtrar_por_rango_poblacion(paises, minimo, maximo)
        cr.mostrar_paises(resultado)

    elif opcion == "3":
        minimo = core.validar_entero_positivo("Superficie mínima (km²): ")
        maximo = core.validar_entero_positivo("Superficie máxima (km²): ")
        if minimo > maximo:
            print("[ERROR] El mínimo no puede ser mayor que el máximo.")
            return
        resultado = cr.filtrar_por_rango_superficie(paises, minimo, maximo)
        cr.mostrar_paises(resultado)

    else:
        print("[ERROR] Opción inválida.")


def menu_ordenar(paises):
    """Submenú de ordenamientos: criterio + ascendente/descendente."""
    print("\n--- ORDENAR PAÍSES ---")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    opcion = core.validar_texto("Elija un criterio: ")

    criterios = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in criterios:
        print("[ERROR] Criterio inválido.")
        return
    criterio = criterios[opcion]

    print("a. Ascendente (menor a mayor / A-Z)")
    print("b. Descendente (mayor a menor / Z-A)")
    sentido = core.validar_texto("Elija el sentido: ").lower()
    ascendente = (sentido != "b")  # cualquier cosa distinta de 'b' = ascendente

    resultado = cr.ordenar_paises(paises, criterio, ascendente)
    cr.mostrar_paises(resultado)


# ==========================================================================
#  MENÚ PRINCIPAL
# ==========================================================================

def mostrar_menu():
    """Imprime el menú principal de opciones."""
    print("=" * 50)
    print("   GESTIÓN DE DATOS DE PAÍSES")
    print("=" * 50)
    print("1. Mostrar todos los países")
    print("2. Agregar país")
    print("3. Actualizar país (población y superficie)")
    print("4. Buscar país por nombre")
    print("5. Filtrar países")
    print("6. Ordenar países")
    print("7. Mostrar estadísticas")
    print("8. Guardar cambios en el CSV")
    print("0. Salir")
    print("-" * 50)


def main():
    """Punto de entrada del programa."""
    # 1) Cargamos los datos del CSV al iniciar (módulo de Noelia).
    paises = core.leer_csv(ARCHIVO_CSV)

    # 2) Bucle principal del menú.
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            cr.mostrar_paises(paises)
        elif opcion == "2":
            core.agregar_pais(paises)
        elif opcion == "3":
            core.actualizar_pais(paises)
        elif opcion == "4":
            menu_buscar(paises)
        elif opcion == "5":
            menu_filtrar(paises)
        elif opcion == "6":
            menu_ordenar(paises)
        elif opcion == "7":
            cr.mostrar_estadisticas(paises)
        elif opcion == "8":
            core.guardar_csv(ARCHIVO_CSV, paises)
        elif opcion == "0":
            # Ofrecemos guardar antes de salir para no perder cambios.
            guardar = input("¿Desea guardar los cambios antes de salir? (s/n): ").strip().lower()
            if guardar == "s":
                core.guardar_csv(ARCHIVO_CSV, paises)
            print("¡Hasta luego!")
            break
        else:
            print("[ERROR] Opción inválida. Intente nuevamente.")

        input("\nPresione ENTER para continuar...")
