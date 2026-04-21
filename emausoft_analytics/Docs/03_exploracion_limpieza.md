# 03 — Exploración y limpieza de datos

Este documento explica el proceso de exploración de datos (EDA) y las decisiones de limpieza tomadas para cada fuente.

---

## ¿Qué es el EDA y por qué es importante?

El Análisis Exploratorio de Datos (EDA por sus siglas en inglés) es el primer paso antes de tocar cualquier dato. Consiste en entender la estructura, calidad y contenido de los datos antes de transformarlos.

Sin EDA es muy fácil cometer errores como eliminar columnas importantes, ignorar valores nulos que afectan el análisis o hacer transformaciones incorrectas.

---

## Herramientas utilizadas

Se utilizaron notebooks de Jupyter dentro de VS Code por las siguientes razones:

- Permiten ejecutar el código bloque por bloque y ver los resultados inmediatamente
- Las tablas y gráficas se muestran directamente en el notebook
- Facilitan la experimentación — si algo falla solo se re-ejecuta ese bloque
- Son ideales para la fase de exploración donde se está descubriendo el dato

Una vez que el código funcionó correctamente se trasladó a scripts `.py` limpios en la carpeta `3_scripts/`.

---

## EDA del dataset de ventas

**Archivo:** `2_notebooks/01_exploracion_ventas.ipynb`

### Estructura inicial
```
Filas:    2,823
Columnas: 25
```

### Diagnóstico de calidad

| Columna | Nulos | Decisión |
|---|---|---|
| `ADDRESSLINE2` | 2,521 | Eliminada — 89% nulos, no aporta valor |
| `STATE` | 1,486 | Eliminada — muy incompleta |
| `POSTALCODE` | 76 | Eliminada — no necesaria para el análisis |
| `TERRITORY` | 1,074 | Eliminada — se reemplaza con datos de la API de países |
| `ORDERDATE` | 0 | Convertida de texto a formato fecha |

### Columnas seleccionadas
De las 25 columnas originales se seleccionaron 11:
```
ordernumber, orderdate, productcode, quantityordered,
priceeach, sales, country, customername,
productline, dealsize, status
```

**¿Por qué estas columnas?**
Son las que contienen información relevante para responder las preguntas de negocio. Las columnas eliminadas eran datos de contacto, dirección física o información redundante que no aportan al análisis comercial.

### Conversión de fechas
La columna `ORDERDATE` llegó como texto en formato `MM/DD/YYYY HH:MM`. Se convirtió a formato fecha con:
```python
df['orderdate'] = pd.to_datetime(df['orderdate'])
```

**¿Por qué es importante?**
Sin esta conversión Power BI y PostgreSQL no pueden hacer análisis temporales como agrupar por mes o trimestre.

### Rango de fechas
```
Fecha más antigua: 2003-01-06
Fecha más reciente: 2005-05-31
```
El dataset cubre aproximadamente 2.5 años de ventas.

### Valores únicos relevantes
```
Países:   19
Productos: 109
Órdenes:  307
```

### Duplicados
```
Filas duplicadas: 0
```
No se encontraron filas duplicadas — el dataset estaba limpio en ese aspecto.

---

## EDA de la API de clientes

**Archivo:** `2_notebooks/02_consumo_apis.ipynb`

### Resultado de la API
```
Total registros: 100
Columnas generadas: cliente_id, nombre, ciudad, pais
```

La API devuelve datos en formato JSON anidado. Se extrajo solo la información relevante:
```python
for i, persona in enumerate(data['results']):
    clientes.append({
        'cliente_id': i + 1,
        'nombre': persona['name']['first'] + ' ' + persona['name']['last'],
        'ciudad': persona['location']['city'],
        'pais': persona['location']['country']
    })
```

---

## EDA de la API de países

### Problema encontrado
La API retornó un error 400 al intentar obtener todos los campos:
```json
{"status": 400, "message": "fields query not specified or you're requesting more than 10 fields"}
```

**Solución:** Especificar solo los campos necesarios en el parámetro `fields`:
```python
response = requests.get(
    'https://restcountries.com/v3.1/all',
    params={'fields': 'name,region,subregion,capital'}
)
```

### Normalización de países
Al cruzar los 19 países del dataset de ventas con la API se encontró que 2 no coincidían:

| En el CSV | En la API |
|---|---|
| USA | United States |
| UK | United Kingdom |

Se aplicó un mapeo explícito antes de hacer el cruce:
```python
mapeo_paises = {
    'USA': 'United States',
    'UK': 'United Kingdom'
}
df_ventas['country'] = df_ventas['country'].replace(mapeo_paises)
```

Después del mapeo los 19 países coincidieron perfectamente con la API.

---

## Construcción de la tabla de productos

Como el dataset no tiene una tabla de productos separada se construyó extrayendo los productos únicos:

```python
productos = df[['productcode', 'productline']].drop_duplicates().reset_index(drop=True)
productos.insert(0, 'producto_id', range(1, len(productos) + 1))
```

**Resultado:** 109 productos únicos con su ID numérico y categoría.

---

## Asignación de clientes a ventas

Como las ventas no tienen un cliente natural se usó asignación aleatoria con semilla fija:

```python
np.random.seed(42)
df_ventas['cliente_id'] = np.random.randint(1, 101, size=len(df_ventas))
```

**¿Por qué semilla fija?**
La semilla `42` garantiza reproducibilidad — cada vez que se corre el código se asignan exactamente los mismos clientes a las mismas ventas. Sin semilla fija los resultados cambiarían en cada ejecución.

---

## Archivos generados

Al finalizar la limpieza se exportaron 4 archivos a `4_output/`:

| Archivo | Filas | Descripción |
|---|---|---|
| `ventas_limpio.csv` | 2,823 | Ventas limpias con IDs relacionados |
| `productos.csv` | 109 | Productos únicos con ID numérico |
| `clientes.csv` | 100 | Clientes generados desde API |
| `regiones.csv` | 250 | Países con información geográfica |

---

# 03 — Data Exploration and Cleaning

This document explains the data exploration (EDA) process and the cleaning decisions made for each source.

---

## What is EDA and why is it important?

Exploratory Data Analysis (EDA) is the first step before transforming any data. It consists of understanding the structure, quality, and content of the data before changing it.

Without EDA, it is very easy to make mistakes such as deleting important columns, ignoring null values that affect the analysis, or applying incorrect transformations.

---

## Tools Used

Jupyter notebooks inside VS Code were used for the following reasons:

- They allow code to be executed block by block and results to be seen immediately
- Tables and charts are displayed directly in the notebook
- They make experimentation easier; if something fails, only that block needs to be rerun
- They are ideal for the exploration phase, when the data is still being discovered

Once the code worked correctly, it was moved to clean `.py` scripts in the `3_scripts/` folder.

---

## EDA of the Sales Dataset

**File:** `2_notebooks/01_exploracion_ventas.ipynb`

### Initial Structure
```
Rows:    2,823
Columns: 25
```

### Quality Diagnosis

| Column | Nulls | Decision |
|---|---|---|
| `ADDRESSLINE2` | 2,521 | Removed — 89% nulls, no value added |
| `STATE` | 1,486 | Removed — very incomplete |
| `POSTALCODE` | 76 | Removed — not needed for the analysis |
| `TERRITORY` | 1,074 | Removed — replaced with country API data |
| `ORDERDATE` | 0 | Converted from text to date format |

### Selected Columns
Out of the original 25 columns, 11 were selected:
```
ordernumber, orderdate, productcode, quantityordered,
priceeach, sales, country, customername,
productline, dealsize, status
```

**Why these columns?**
They are the ones containing relevant information to answer the business questions. The removed columns were contact details, physical address information, or redundant data that did not contribute to commercial analysis.

### Date Conversion
The `ORDERDATE` column arrived as text in `MM/DD/YYYY HH:MM` format. It was converted to date format with:
```python
df['orderdate'] = pd.to_datetime(df['orderdate'])
```

**Why is this important?**
Without this conversion, Power BI and PostgreSQL cannot perform time-based analysis such as grouping by month or quarter.

### Date Range
```
Oldest date: 2003-01-06
Most recent date: 2005-05-31
```
The dataset covers approximately 2.5 years of sales.

### Relevant Unique Values
```
Countries: 19
Products: 109
Orders:   307
```

### Duplicates
```
Duplicate rows: 0
```
No duplicate rows were found. The dataset was clean in that respect.

---

## EDA of the Customer API

**File:** `2_notebooks/02_consumo_apis.ipynb`

### API Result
```
Total records: 100
Generated columns: cliente_id, nombre, ciudad, pais
```

The API returns data in nested JSON format. Only the relevant information was extracted:
```python
for i, persona in enumerate(data['results']):
    clientes.append({
        'cliente_id': i + 1,
        'nombre': persona['name']['first'] + ' ' + persona['name']['last'],
        'ciudad': persona['location']['city'],
        'pais': persona['location']['country']
    })
```

---

## EDA of the Countries API

### Issue Found
The API returned a 400 error when trying to retrieve all fields:
```json
{"status": 400, "message": "fields query not specified or you're requesting more than 10 fields"}
```

**Solution:** Specify only the required fields in the `fields` parameter:
```python
response = requests.get(
    'https://restcountries.com/v3.1/all',
    params={'fields': 'name,region,subregion,capital'}
)
```

### Country Normalization
When crossing the 19 countries from the sales dataset with the API, 2 of them did not match:

| In the CSV | In the API |
|---|---|
| USA | United States |
| UK | United Kingdom |

An explicit mapping was applied before joining:
```python
mapeo_paises = {
    'USA': 'United States',
    'UK': 'United Kingdom'
}
df_ventas['country'] = df_ventas['country'].replace(mapeo_paises)
```

After the mapping, all 19 countries matched the API correctly.

---

## Building the Products Table

Since the dataset does not have a separate product table, it was built by extracting unique products:

```python
productos = df[['productcode', 'productline']].drop_duplicates().reset_index(drop=True)
productos.insert(0, 'producto_id', range(1, len(productos) + 1))
```

**Result:** 109 unique products with their numeric ID and category.

---

## Assigning Customers to Sales

Since sales do not have a natural customer, random assignment with a fixed seed was used:

```python
np.random.seed(42)
df_ventas['cliente_id'] = np.random.randint(1, 101, size=len(df_ventas))
```

**Why a fixed seed?**
Seed `42` guarantees reproducibility. Every time the code runs, the exact same customers are assigned to the same sales. Without a fixed seed, the results would change with each execution.

---

## Generated Files

At the end of the cleaning process, 4 files were exported to `4_output/`:

| File | Rows | Description |
|---|---|---|
| `ventas_limpio.csv` | 2,823 | Clean sales with related IDs |
| `productos.csv` | 109 | Unique products with numeric ID |
| `clientes.csv` | 100 | Customers generated from API |
| `regiones.csv` | 250 | Countries with geographic information |
