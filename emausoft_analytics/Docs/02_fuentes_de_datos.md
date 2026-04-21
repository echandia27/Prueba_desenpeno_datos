# 02 — Fuentes de datos

Este documento explica de dónde viene cada dato del proyecto, por qué se eligió esa fuente y cómo se integra con el resto de la solución.

---

## Visión general

El proyecto integra 4 fuentes de datos diferentes:

| Fuente | Tipo | Resultado |
|---|---|---|
| Kaggle — sales_data_sample.csv | Archivo CSV | Tabla de ventas y productos |
| randomuser.me API | API REST | Tabla de clientes |
| restcountries.com API | API REST | Tabla de regiones geográficas |
| Construcción propia | Derivado del CSV | Tabla de productos |

---

## Fuente 1 — Dataset de ventas (Kaggle)

**URL:** https://www.kaggle.com/datasets/kyanyoga/sample-sales-data

**Archivo:** `sales_data_sample.csv`

**¿Por qué esta fuente?**
Es el núcleo del proyecto. Contiene información transaccional real de ventas con 2,823 registros y 25 columnas. Es la fuente más rica y completa del proyecto.

**¿Qué contiene?**
- Información de órdenes de venta
- Precios y cantidades
- Países de los clientes
- Códigos de productos
- Fechas de las transacciones

**Problemas encontrados:**
- La columna `ORDERDATE` llegó como texto y debía convertirse a formato fecha
- Varias columnas irrelevantes para el análisis (`ADDRESSLINE2`, `STATE`, `POSTALCODE`)
- Los nombres de países `USA` y `UK` no coincidían con los nombres de la API de países
- No contenía clientes explícitos — solo el nombre de la empresa compradora

**Decisiones tomadas:**
- Se seleccionaron solo 11 columnas de las 25 originales
- Se normalizaron los nombres de países para que coincidan con la API
- Se usó `CUSTOMERNAME` para identificar empresas compradoras

---

## Fuente 2 — API de clientes (randomuser.me)

**URL:** https://randomuser.me/api/?results=100

**¿Por qué esta fuente?**
El dataset de ventas no tiene clientes individuales explícitos. Para simular una dimensión de clientes realista se usó esta API que genera personas aleatorias con nombre, ciudad y país.

**¿Qué contiene?**
- Nombre completo
- Ciudad de residencia
- País de residencia

**Decisión de asignación:**
Como las ventas no tienen un cliente_id natural, se tomó la decisión de asignar clientes de forma **aleatoria** con semilla fija (`np.random.seed(42)`). La semilla fija garantiza que el resultado sea siempre el mismo — si volvemos a correr el pipeline los mismos clientes quedan asignados a las mismas ventas.

Esta es una decisión válida en un contexto de prueba donde no existe una relación real entre los datasets. En un ambiente de producción esta asignación vendría de los sistemas transaccionales de la empresa.

**Columnas generadas:**
```
cliente_id | nombre | ciudad | pais
```

---

## Fuente 3 — API de países (restcountries.com)

**URL:** https://restcountries.com/v3.1/all?fields=name,region,subregion,capital

**¿Por qué esta fuente?**
El dataset de ventas solo tiene el nombre del país pero no información geográfica más amplia como continente o subregión. Esta API enriquece los datos geográficos permitiendo análisis por región y continente en el dashboard.

**Problema encontrado:**
La API cambió sus reglas y ahora exige especificar los campos que se quieren obtener. Sin el parámetro `fields` retorna un error 400. La solución fue agregar el parámetro explícitamente:
```python
params={'fields': 'name,region,subregion,capital'}
```

**Normalización de países:**
Los países `USA` y `UK` en el dataset de ventas no coincidían con los nombres de la API (`United States` y `United Kingdom`). Se aplicó un mapeo explícito:
```python
mapeo_paises = {
    'USA': 'United States',
    'UK': 'United Kingdom'
}
```

**Columnas generadas:**
```
pais | continente | subregion | capital
```

---

## Fuente 4 — Tabla de productos (construcción propia)

**¿Por qué construirla?**
El dataset de ventas contiene códigos de producto (`productCode`) pero no una tabla de productos separada. Para cumplir con el modelo estrella y las buenas prácticas de modelado de datos era necesario tener una dimensión de productos independiente.

**¿Cómo se construyó?**
Se extrajeron los productos únicos del dataset de ventas usando pandas:
```python
productos = df[['productcode', 'productline']].drop_duplicates()
productos.insert(0, 'producto_id', range(1, len(productos) + 1))
```

Se generó un `producto_id` numérico secuencial y se usó `productline` como categoría del producto.

**Limitación:**
Los productos no tienen nombres descriptivos — solo códigos como `S18_3232`. Esto es una limitación del dataset original. En el dashboard se usa la categoría (`productline`) para agrupar productos de forma legible.

**Columnas generadas:**
```
producto_id | producto_nombre | categoria
```

---

# 02 — Data Sources

This document explains where each project dataset comes from, why that source was chosen, and how it integrates with the rest of the solution.

---

## Overview

The project integrates 4 different data sources:

| Source | Type | Result |
|---|---|---|
| Kaggle — sales_data_sample.csv | CSV file | Sales and products table |
| randomuser.me API | REST API | Customers table |
| restcountries.com API | REST API | Geographic regions table |
| Custom construction | Derived from the CSV | Products table |

---

## Source 1 — Sales Dataset (Kaggle)

**URL:** https://www.kaggle.com/datasets/kyanyoga/sample-sales-data

**File:** `sales_data_sample.csv`

**Why this source?**
It is the core of the project. It contains real transactional sales information with 2,823 records and 25 columns. It is the richest and most complete source in the project.

**What does it contain?**
- Sales order information
- Prices and quantities
- Customer countries
- Product codes
- Transaction dates

**Issues found:**
- The `ORDERDATE` column arrived as text and had to be converted to date format
- Several irrelevant columns for analysis (`ADDRESSLINE2`, `STATE`, `POSTALCODE`)
- The country names `USA` and `UK` did not match the country API names
- It did not contain explicit customers, only the name of the purchasing company

**Decisions made:**
- Only 11 of the original 25 columns were selected
- Country names were normalized to match the API
- `CUSTOMERNAME` was used to identify purchasing companies

---

## Source 2 — Customer API (randomuser.me)

**URL:** https://randomuser.me/api/?results=100

**Why this source?**
The sales dataset does not include explicit individual customers. To simulate a realistic customer dimension, this API was used because it generates random people with name, city, and country.

**What does it contain?**
- Full name
- City of residence
- Country of residence

**Assignment decision:**
Since sales do not have a natural `cliente_id`, the decision was made to assign customers **randomly** using a fixed seed (`np.random.seed(42)`). The fixed seed guarantees that the result is always the same. If we run the pipeline again, the same customers remain assigned to the same sales.

This is a valid decision in a test context where there is no real relationship between the datasets. In a production environment, this assignment would come from the company's transactional systems.

**Generated columns:**
```
cliente_id | nombre | ciudad | pais
```

---

## Source 3 — Countries API (restcountries.com)

**URL:** https://restcountries.com/v3.1/all?fields=name,region,subregion,capital

**Why this source?**
The sales dataset only contains the country name, but not broader geographic information such as continent or subregion. This API enriches the geographic data, enabling region- and continent-based analysis in the dashboard.

**Issue found:**
The API changed its rules and now requires explicitly specifying the fields to retrieve. Without the `fields` parameter, it returns a 400 error. The solution was to add the parameter explicitly:
```python
params={'fields': 'name,region,subregion,capital'}
```

**Country normalization:**
The countries `USA` and `UK` in the sales dataset did not match the API names (`United States` and `United Kingdom`). An explicit mapping was applied:
```python
mapeo_paises = {
    'USA': 'United States',
    'UK': 'United Kingdom'
}
```

**Generated columns:**
```
pais | continente | subregion | capital
```

---

## Source 4 — Products Table (custom-built)

**Why build it?**
The sales dataset contains product codes (`productCode`) but not a separate products table. To comply with the star schema and data modeling best practices, it was necessary to create an independent product dimension.

**How was it built?**
Unique products were extracted from the sales dataset using pandas:
```python
productos = df[['productcode', 'productline']].drop_duplicates()
productos.insert(0, 'producto_id', range(1, len(productos) + 1))
```

A sequential numeric `producto_id` was generated and `productline` was used as the product category.

**Limitation:**
The products do not have descriptive names, only codes such as `S18_3232`. This is a limitation of the original dataset. In the dashboard, the category (`productline`) is used to group products in a readable way.

**Generated columns:**
```
producto_id | producto_nombre | categoria
```
