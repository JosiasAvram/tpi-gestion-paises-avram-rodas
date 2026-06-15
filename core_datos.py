
# core_datos.py

# Módulo CORE DE DATOS del Trabajo Práctico Integrador.
# Autora: Noelia Maricel Rodas

# Responsabilidades de este módulo:
#     - Lectura y escritura del archivo CSV (con conversión de tipos y manejo de excepciones).
#     - Definición de la estructura de datos base (lista de diccionarios).
#     - Alta (agregar) y modificación (actualizar) de países.
#     - Validaciones de las entradas del usuario.

# Cada país se representa como un diccionario:
#     {
#         "nombre": str,
#         "poblacion": int,
#         "superficie": int,
#         "continente": str
#     }
# La colección completa de países es una LISTA de esos diccionarios.


import csv
import os

# Campos esperados en el archivo CSV (en este orden).
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


#  LECTURA / ESCRITURA DEL CSV
def leer_csv(ruta):
    # Lee el archivo CSV indicado y devuelve una lista de diccionarios.
    # - Convierte 'poblacion' y 'superficie' a int.
    # - Ignora (avisando) las filas con formato incorrecto en lugar de cortar todo el programa.
    # - Maneja el caso de archivo inexistente.
    # Devuelve: lista de diccionarios (puede estar vacía si hay un error grave).
    
    paises = []
    # 1) Verificamos que el archivo exista antes de intentar abrirlo.
    if not os.path.exists(ruta):
        print(f"[ERROR] No se encontró el archivo '{ruta}'.")
        print("        Se iniciará el programa con una lista vacía.")
        return paises

    try:
        # newline="" y encoding utf-8 evitan problemas con acentos y saltos de línea.
        with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            # Validamos que el encabezado tenga las columnas esperadas.
            if lector.fieldnames is None or not _encabezado_valido(lector.fieldnames):
                print("[ERROR] El encabezado del CSV no tiene el formato esperado.")
                print(f"        Se esperaba: {CAMPOS}")
                return paises
            # 2) Recorremos cada fila convirtiendo tipos y validando.
            for numero_fila, fila in enumerate(lector, start=2):  # start=2: fila 1 = encabezado
                pais = _convertir_fila(fila, numero_fila)
                if pais is not None:
                    paises.append(pais)

    except PermissionError:
        print(f"[ERROR] Sin permisos para leer el archivo '{ruta}'.")
    except UnicodeDecodeError:
        print(f"[ERROR] No se pudo decodificar '{ruta}'. Verifique que esté en UTF-8.")
    except Exception as error:
        # Red de seguridad ante cualquier otro problema inesperado.
        print(f"[ERROR] Ocurrió un problema inesperado al leer el CSV: {error}")

    print(f"[OK] Se cargaron {len(paises)} países desde '{ruta}'.")
    return paises


def guardar_csv(ruta, paises):
    # Escribe la lista de países en el archivo CSV (sobrescribe el contenido).
    # Devuelve True si se guardó correctamente, False en caso de error.
    try:
        with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            for pais in paises:
                escritor.writerow(pais)
        print(f"[OK] Datos guardados en '{ruta}'.")
        return True
    except PermissionError:
        print(f"[ERROR] Sin permisos para escribir en '{ruta}'.")
    except Exception as error:
        print(f"[ERROR] No se pudo guardar el archivo: {error}")
    return False


def _encabezado_valido(fieldnames):
    # Función auxiliar: comprueba que el encabezado contenga todos los campos.
    return all(campo in fieldnames for campo in CAMPOS)


def _convertir_fila(fila, numero_fila):
    # Función auxiliar: convierte una fila del CSV (dict de strings) en un país válido.
    # Devuelve el diccionario del país o None si la fila tiene errores.
    try:
        nombre = fila["nombre"].strip()
        continente = fila["continente"].strip()
        poblacion_texto = fila["poblacion"].strip()
        superficie_texto = fila["superficie"].strip()

        # Ningún campo puede estar vacío.
        if not nombre or not continente or not poblacion_texto or not superficie_texto:
            print(f"[AVISO] Fila {numero_fila} ignorada: hay campos vacíos.")
            return None

        # Conversión de tipos: población y superficie deben ser enteros.
        poblacion = int(poblacion_texto)
        superficie = int(superficie_texto)

        if poblacion < 0 or superficie < 0:
            print(f"[AVISO] Fila {numero_fila} ignorada: valores negativos.")
            return None

        return {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente,
        }

    except (ValueError, TypeError):
        print(f"[AVISO] Fila {numero_fila} ignorada: 'poblacion' o 'superficie' no son números.")
        return None
    except KeyError as falta:
        print(f"[AVISO] Fila {numero_fila} ignorada: falta la columna {falta}.")
        return None


#  VALIDACIONES DE ENTRADA
def validar_texto(mensaje):
    # Pide texto por consola y se asegura de que no esté vacío.
    # Repite hasta obtener una entrada válida. Devuelve el texto limpio.
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  -> La entrada no puede estar vacía. Intente nuevamente.")


def validar_entero_positivo(mensaje):
    # Pide un número entero positivo por consola.
    # Repite hasta obtener un valor válido. Devuelve el entero.
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero < 0:
                print("  -> Debe ingresar un número positivo (0 o mayor).")
                continue
            return numero
        except ValueError:
            print("  -> Entrada inválida. Debe ingresar un número entero.")


def existe_pais(paises, nombre):
    # Devuelve True si ya existe un país con ese nombre (sin distinguir
    # mayúsculas/minúsculas). Sirve para evitar duplicados.
    nombre = nombre.strip().lower()
    for pais in paises:
        if pais["nombre"].lower() == nombre:
            return True
    return False


def buscar_indice(paises, nombre):
    # Devuelve el índice del país cuyo nombre coincide exactamente
    # (sin distinguir mayúsculas), o -1 si no existe.
    nombre = nombre.strip().lower()
    for i, pais in enumerate(paises):
        if pais["nombre"].lower() == nombre:
            return i
    return -1


#  ALTA Y MODIFICACIÓN DE PAÍSES
def agregar_pais(paises):
    # Solicita los datos de un nuevo país por consola, los valida y lo agrega
    # a la lista. No permite campos vacíos ni países duplicados.

    # Modifica la lista 'paises' en el lugar (in place).
    # Devuelve True si se agregó, False si se canceló por duplicado.
    print("\n--- AGREGAR PAÍS ---")
    nombre = validar_texto("Nombre del país: ")

    # Evitamos duplicados.
    if existe_pais(paises, nombre):
        print(f"[ERROR] El país '{nombre}' ya existe en la lista.")
        return False

    poblacion = validar_entero_positivo("Población (número entero): ")
    superficie = validar_entero_positivo("Superficie en km² (número entero): ")
    continente = validar_texto("Continente: ")

    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }
    paises.append(nuevo_pais)
    print(f"[OK] País '{nombre}' agregado correctamente.")
    return True


def actualizar_pais(paises):
    # Permite actualizar la POBLACIÓN y la SUPERFICIE de un país existente.
    # Busca el país por nombre exacto.

    # Modifica la lista 'paises' en el lugar (in place).
    # Devuelve True si se actualizó, False si no se encontró el país.
    print("\n--- ACTUALIZAR PAÍS ---")
    nombre = validar_texto("Nombre del país a actualizar: ")

    indice = buscar_indice(paises, nombre)
    if indice == -1:
        print(f"[ERROR] No se encontró el país '{nombre}'.")
        return False

    pais = paises[indice]
    print(f"Datos actuales -> Población: {pais['poblacion']:,} | "
        f"Superficie: {pais['superficie']:,} km²")

    nueva_poblacion = validar_entero_positivo("Nueva población: ")
    nueva_superficie = validar_entero_positivo("Nueva superficie en km²: ")

    pais["poblacion"] = nueva_poblacion
    pais["superficie"] = nueva_superficie
    print(f"[OK] País '{pais['nombre']}' actualizado correctamente.")
    return True
