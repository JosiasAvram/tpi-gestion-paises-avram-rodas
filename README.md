# Gestión de Datos de Países en Python

Trabajo Práctico Integrador (TPI) – **Programación 1**
Tecnicatura Universitaria en Programación (a distancia)

Aplicación de consola en Python para gestionar información de países (nombre, población, superficie y continente) a partir de un archivo CSV, con funciones de alta y modificación, búsquedas, filtros, ordenamientos y estadísticas.

---

## Integrantes y división del trabajo

| Integrante | Módulo | Responsabilidades |
|------------|--------|-------------------|
| **Josías Alexis Avram** | `consultas_reportes.py` | Búsqueda por nombre, filtros (continente, rango de población, rango de superficie), ordenamientos (nombre/población/superficie, asc/desc) y estadísticas. |
| **Noelia Maricel Rodas** | `core_datos.py` | Lectura/escritura del CSV, conversión de tipos y manejo de excepciones, estructura de datos base, alta y actualización de países, validaciones de entrada. |

El archivo `main.py` (menú de consola) integra ambos módulos.

---

## Estructura del proyecto

```
.
├── ejecutar.py             # Punto de entrada: se corre este archivo
├── main.py                 # Menú de consola: integra los dos módulos
├── core_datos.py           # Núcleo de datos (Noelia)
├── consultas_reportes.py   # Consultas y reportes (Josías)
├── paises.csv              # Dataset base
└── README.md
```

Cada país se representa como un **diccionario** y la colección completa es una **lista de diccionarios**:

```python
{
    "nombre": "Argentina",
    "poblacion": 45376763,
    "superficie": 2780400,
    "continente": "América"
}
```

---

## Requisitos

- Python 3.x (no requiere librerías externas, solo módulos estándar `csv` y `os`).

## Cómo ejecutar

1. Clonar el repositorio o descargar la carpeta.
2. Abrir una terminal en la carpeta del proyecto.
3. Asegurarse de que `paises.csv` esté en la misma carpeta que los archivos `.py`.
4. Ejecutar:

```bash
python ejecutar.py
```

---

## Funcionalidades del menú

```
==================================================
   GESTIÓN DE DATOS DE PAÍSES
==================================================
1. Mostrar todos los países
2. Agregar país
3. Actualizar país (población y superficie)
4. Buscar país por nombre
5. Filtrar países
6. Ordenar países
7. Mostrar estadísticas
8. Guardar cambios en el CSV
0. Salir
--------------------------------------------------
```

- **Agregar país:** solicita nombre, población, superficie y continente. No permite campos vacíos ni países duplicados.
- **Actualizar país:** modifica la población y la superficie de un país existente.
- **Buscar por nombre:** coincidencia parcial (ej. `arg` → Argentina) o exacta.
- **Filtrar:** por continente, por rango de población o por rango de superficie.
- **Ordenar:** por nombre, población o superficie, en orden ascendente o descendente.
- **Estadísticas:** país con mayor y menor población, promedio de población, promedio de superficie y cantidad de países por continente.
- **Guardar:** escribe los cambios en `paises.csv`.

---

## Ejemplos de entrada / salida

### Buscar por nombre (coincidencia parcial)

```
Elija una opción: 4
--- BUSCAR POR NOMBRE ---
1. Coincidencia parcial (ej. 'arg' encuentra 'Argentina')
2. Coincidencia exacta
Elija una opción: 1
Texto a buscar: arg

NOMBRE                    POBLACIÓN    SUPERFICIE (km²)  CONTINENTE
------------------------------------------------------------------------
Argentina                45,376,763           2,780,400  América
------------------------------------------------------------------------
Total: 1 país(es).
```

### Estadísticas

```
Elija una opción: 7
--- ESTADÍSTICAS ---
País con MAYOR población: China (1,412,600,000 hab.)
País con MENOR población: Nueva Zelanda (5,084,300 hab.)
Promedio de población : 193,109,658.85 hab.
Promedio de superficie: 3,185,642.58 km²

Cantidad de países por continente:
  - América: 6
  - Asia: 6
  - Europa: 7
  - Oceanía: 2
  - África: 5
```

### Agregar país (validación de entrada)

```
Elija una opción: 2
--- AGREGAR PAÍS ---
Nombre del país: Uruguay
Población (número entero): abc
  -> Entrada inválida. Debe ingresar un número entero.
Población (número entero): 3473730
Superficie en km² (número entero): 176215
Continente: América
[OK] País 'Uruguay' agregado correctamente.
```

---

## Manejo de errores y validaciones

- Lectura robusta del CSV: controla que el archivo exista, valida el encabezado, convierte tipos e **ignora con aviso** las filas mal formadas en lugar de cortar el programa.
- Todas las entradas numéricas usan `try/except` para no caerse ante texto inválido.
- No se permiten campos vacíos ni países duplicados.
- Mensajes claros de éxito (`[OK]`) y error (`[ERROR]` / `[AVISO]`).

---

## Enlaces de la entrega

- **Documentación (PDF):** `informe.pdf` (en la raíz del repositorio).
- **Video demostrativo (10–15 min):** _<pegar aquí el enlace público de YouTube/Drive>_

> Recordatorio: el video debe mostrar a ambos integrantes a cámara al inicio y la demostración de todos los flujos del programa.

---

## Flujo de trabajo en Git

Cada integrante trabaja en su propia rama y luego integra a `main` mediante Pull Request:

```
main
├── feature/core-datos          → Noelia
└── feature/consultas-reportes  → Josías
```
