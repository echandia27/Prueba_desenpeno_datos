# 05 — Pipeline de carga

Este documento explica cómo funciona el pipeline ETL del proyecto, las decisiones técnicas tomadas y por qué se implementó de esta forma.

---

## ¿Qué es un pipeline ETL?

ETL son las siglas de Extract, Transform, Load — Extraer, Transformar y Cargar. Es el proceso estándar para mover datos desde las fuentes hasta el destino final.

En este proyecto el pipeline hace lo siguiente:

**Extract (Extraer):** Lee los 4 archivos CSV de la carpeta `4_output/`

**Transform (Transformar):** Construye las dimensiones del modelo estrella y genera los IDs correctos para relacionar las tablas

**Load (Cargar):** Inserta los datos en PostgreSQL en el orden correcto respetando las relaciones

---

## Archivo del pipeline

**Ruta:** `3_scripts/cargar_datos.py`

---

## ¿Por qué un script `.py` y no un notebook?

Los notebooks son ideales para exploración pero no para producción. Un script `.py` es más apropiado para la carga porque:

- Se ejecuta desde la terminal con un solo comando
- Es más fácil de automatizar si se necesita ejecutar periódicamente
- No depende de una interfaz gráfica
- Es más fácil de mantener y versionar

---

## Método de inserción — batch con method='multi'

En lugar de insertar los datos fila por fila se usa inserción en lotes:

```python
df.to_sql(
    tabla,
    engine,
    if_exists='append',
    index=False,
    method='multi',
    chunksize=1000
)
```

**¿Por qué este método?**

La inserción fila por fila hace una consulta SQL por cada registro. Para 2,823 ventas eso serían 2,823 viajes de ida y vuelta al servidor. Con `method='multi'` y `chunksize=1000` se hacen bloques de 1,000 registros por consulta — mucho más eficiente.

Este enfoque fue tomado de un pipeline de referencia del proyecto RetailCo donde se demostró que es significativamente más rápido que la inserción individual.

---

## Orden de carga — por qué importa

Las tablas se cargan en este orden específico:

```
1. dim_producto   (sin dependencias)
2. dim_cliente    (sin dependencias)
3. dim_region     (sin dependencias)
4. dim_tiempo     (sin dependencias)
5. fact_ventas    (depende de las 4 anteriores)
```

**¿Por qué este orden?**

`fact_ventas` tiene llaves foráneas que apuntan a las otras 4 tablas. PostgreSQL verifica que los IDs referenciados existan antes de insertar un registro. Si se intenta insertar `fact_ventas` primero PostgreSQL rechazará los datos porque las dimensiones aún están vacías.

---

## Construcción de dim_tiempo en el pipeline

La dimensión de tiempo se construye automáticamente a partir de las fechas de ventas:

```python
ventas['orderdate'] = pd.to_datetime(ventas['orderdate'])
fechas_unicas = ventas['orderdate'].dt.normalize().drop_duplicates().sort_values()

dim_tiempo = pd.DataFrame({
    'fecha'     : fechas_unicas,
    'anio'      : fechas_unicas.dt.year,
    'mes'       : fechas_unicas.dt.month,
    'nombre_mes': fechas_unicas.dt.strftime('%B'),
    'trimestre' : fechas_unicas.dt.quarter,
    'dia'       : fechas_unicas.dt.day
})
```

**¿Por qué `.dt.normalize()`?**
Elimina la parte de la hora de la fecha dejando solo la fecha pura (`2003-01-06` en lugar de `2003-01-06 00:00:00`). Esto evita duplicados por diferencias en la hora.

---

## Construcción de fact_ventas en el pipeline

`fact_ventas` se construye uniendo los IDs de las dimensiones al dataset de ventas:

```python
# Unir region_id
ventas = ventas.merge(
    dim_region[['region_id', 'pais']],
    left_on='country',
    right_on='pais',
    how='left'
)

# Unir tiempo_id
ventas = ventas.merge(
    dim_tiempo[['tiempo_id', 'fecha']],
    left_on='orderdate',
    right_on='fecha',
    how='left'
)
```

Se usa `how='left'` para mantener todos los registros de ventas incluso si no se encuentra una coincidencia en la dimensión.

---

## Variables de entorno con python-dotenv

Las credenciales de la base de datos se guardan en un archivo `.env` y se cargan con `python-dotenv`:

```python
load_dotenv('../.env')

DB_URI = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
```

**¿Por qué variables de entorno?**
Guardar contraseñas directamente en el código es una mala práctica de seguridad. Si el código se sube a un repositorio las contraseñas quedan expuestas. Con `.env` las credenciales están separadas del código y el archivo está en `.gitignore`.

---

## Resultado del pipeline

```
[HH:MM:SS] Iniciando pipeline — Modelo Estrella
=======================================================
[HH:MM:SS] EXTRAER → Leyendo archivos CSV...
[HH:MM:SS]   ventas    → 2,823 filas
[HH:MM:SS]   productos →   109 filas
[HH:MM:SS]   clientes  →   100 filas
[HH:MM:SS]   regiones  →   250 filas
=======================================================
[HH:MM:SS] TRANSFORMAR → Preparando dimensiones...
[HH:MM:SS]   dim_tiempo  → 252 fechas únicas
[HH:MM:SS]   dim_region  → 250 regiones
[HH:MM:SS] TRANSFORMAR → Construyendo fact_ventas...
[HH:MM:SS]   fact_ventas → 2,823 filas
=======================================================
[HH:MM:SS] CARGAR → Insertando en PostgreSQL...
[HH:MM:SS] dim_producto    →  109 filas insertadas ✅
[HH:MM:SS] dim_cliente     →  100 filas insertadas ✅
[HH:MM:SS] dim_region      →  250 filas insertadas ✅
[HH:MM:SS] dim_tiempo      →  252 filas insertadas ✅
[HH:MM:SS] fact_ventas     → 2,823 filas insertadas ✅
=======================================================
[HH:MM:SS] Pipeline completado ✅
```

---

# 05 — Load Pipeline

This document explains how the project's ETL pipeline works, the technical decisions that were made, and why it was implemented this way.

---

## What is an ETL pipeline?

ETL stands for Extract, Transform, Load. It is the standard process used to move data from the sources to the final destination.

In this project, the pipeline does the following:

**Extract:** Reads the 4 CSV files from the `4_output/` folder

**Transform:** Builds the star schema dimensions and generates the correct IDs to relate the tables

**Load:** Inserts the data into PostgreSQL in the correct order while respecting the relationships

---

## Pipeline File

**Path:** `3_scripts/cargar_datos.py`

---

## Why a `.py` script instead of a notebook?

Notebooks are ideal for exploration, but not for production. A `.py` script is more appropriate for the load process because:

- It runs from the terminal with a single command
- It is easier to automate if periodic execution is needed
- It does not depend on a graphical interface
- It is easier to maintain and version

---

## Insertion Method — batch with `method='multi'`

Instead of inserting data row by row, batch insertion is used:

```python
df.to_sql(
    tabla,
    engine,
    if_exists='append',
    index=False,
    method='multi',
    chunksize=1000
)
```

**Why this method?**

Row-by-row insertion performs one SQL query per record. For 2,823 sales, that would mean 2,823 round trips to the server. With `method='multi'` and `chunksize=1000`, blocks of 1,000 records are inserted per query, which is much more efficient.

This approach was taken from a reference pipeline in the RetailCo project, where it was shown to be significantly faster than individual insertion.

---

## Load Order — why it matters

Tables are loaded in this specific order:

```
1. dim_producto   (no dependencies)
2. dim_cliente    (no dependencies)
3. dim_region     (no dependencies)
4. dim_tiempo     (no dependencies)
5. fact_ventas    (depends on the previous 4)
```

**Why this order?**

`fact_ventas` has foreign keys that point to the other 4 tables. PostgreSQL checks that the referenced IDs exist before inserting a record. If `fact_ventas` is inserted first, PostgreSQL will reject the data because the dimensions are still empty.

---

## Building `dim_tiempo` in the pipeline

The time dimension is built automatically from the sales dates:

```python
ventas['orderdate'] = pd.to_datetime(ventas['orderdate'])
fechas_unicas = ventas['orderdate'].dt.normalize().drop_duplicates().sort_values()

dim_tiempo = pd.DataFrame({
    'fecha'     : fechas_unicas,
    'anio'      : fechas_unicas.dt.year,
    'mes'       : fechas_unicas.dt.month,
    'nombre_mes': fechas_unicas.dt.strftime('%B'),
    'trimestre' : fechas_unicas.dt.quarter,
    'dia'       : fechas_unicas.dt.day
})
```

**Why `.dt.normalize()`?**
It removes the time portion of the date, leaving only the pure date (`2003-01-06` instead of `2003-01-06 00:00:00`). This avoids duplicates caused by time differences.

---

## Building `fact_ventas` in the pipeline

`fact_ventas` is built by joining the dimension IDs to the sales dataset:

```python
# Join region_id
ventas = ventas.merge(
    dim_region[['region_id', 'pais']],
    left_on='country',
    right_on='pais',
    how='left'
)

# Join tiempo_id
ventas = ventas.merge(
    dim_tiempo[['tiempo_id', 'fecha']],
    left_on='orderdate',
    right_on='fecha',
    how='left'
)
```

`how='left'` is used to preserve all sales records even if a match is not found in the dimension.

---

## Environment Variables with `python-dotenv`

The database credentials are stored in a `.env` file and loaded with `python-dotenv`:

```python
load_dotenv('../.env')

DB_URI = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
```

**Why environment variables?**
Storing passwords directly in the code is a poor security practice. If the code is uploaded to a repository, the passwords become exposed. With `.env`, the credentials are separated from the code and the file is already listed in `.gitignore`.

---

## Pipeline Result

```
[HH:MM:SS] Starting pipeline — Star Schema
=======================================================
[HH:MM:SS] EXTRACT → Reading CSV files...
[HH:MM:SS]   ventas    → 2,823 rows
[HH:MM:SS]   productos →   109 rows
[HH:MM:SS]   clientes  →   100 rows
[HH:MM:SS]   regiones  →   250 rows
=======================================================
[HH:MM:SS] TRANSFORM → Preparing dimensions...
[HH:MM:SS]   dim_tiempo  → 252 unique dates
[HH:MM:SS]   dim_region  → 250 regions
[HH:MM:SS] TRANSFORM → Building fact_ventas...
[HH:MM:SS]   fact_ventas → 2,823 rows
=======================================================
[HH:MM:SS] LOAD → Inserting into PostgreSQL...
[HH:MM:SS] dim_producto    →  109 rows inserted ✅
[HH:MM:SS] dim_cliente     →  100 rows inserted ✅
[HH:MM:SS] dim_region      →  250 rows inserted ✅
[HH:MM:SS] dim_tiempo      →  252 rows inserted ✅
[HH:MM:SS] fact_ventas     → 2,823 rows inserted ✅
=======================================================
[HH:MM:SS] Pipeline completed ✅
```
