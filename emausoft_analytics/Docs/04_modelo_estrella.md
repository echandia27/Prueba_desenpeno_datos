# 04 — Modelo Estrella

Este documento explica qué es el modelo estrella, por qué se eligió para este proyecto y cómo está implementado.

---

## ¿Qué es el modelo estrella?

El modelo estrella es una forma de organizar los datos en una base de datos pensada específicamente para el análisis y la generación de reportes. Recibe ese nombre porque visualmente se parece a una estrella: hay una tabla central rodeada de tablas de soporte.

Se compone de dos tipos de tablas:

**Tabla de hechos (FACT)**
Contiene los eventos medibles del negocio — en este caso las ventas. Tiene métricas numéricas como el monto vendido, la cantidad y el precio. También contiene las llaves que la conectan con las demás tablas.

**Tablas de dimensiones (DIM)**
Contienen el contexto de los hechos — quién compró, qué se vendió, dónde y cuándo. Son tablas descriptivas que permiten filtrar y agrupar los datos de diferentes maneras.

---

## ¿Por qué usamos el modelo estrella?

Se eligió el modelo estrella por tres razones principales:

**1. Rendimiento en consultas analíticas**
Las herramientas de visualización como Power BI están optimizadas para trabajar con este modelo. Las consultas son más rápidas porque los datos están organizados de forma que evita operaciones complejas.

**2. Facilidad de uso en Power BI**
Power BI detecta y usa automáticamente las relaciones del modelo estrella. Esto permite crear visualizaciones arrastrando campos sin necesidad de escribir código.

**3. Claridad conceptual**
El modelo estrella hace que sea fácil entender qué contiene cada tabla y cómo se relacionan. Cualquier persona del equipo puede entender la estructura sin ser experta en bases de datos.

---

## Estructura implementada

```
                  dim_producto
                  (producto_id)
                       |
                       |
dim_cliente ———— fact_ventas ———— dim_region
(cliente_id)    (tabla central)   (region_id)
                       |
                       |
                  dim_tiempo
                  (tiempo_id)
```

---

## Detalle de cada tabla

### fact_ventas — Tabla de hechos

Es la tabla central del modelo. Contiene los datos de cada línea de venta.

| Columna | Tipo | Descripción |
|---|---|---|
| ordernumber | INTEGER | Número de orden |
| quantityordered | INTEGER | Cantidad vendida |
| priceeach | NUMERIC | Precio unitario |
| sales | NUMERIC | Monto total de la venta |
| status | TEXT | Estado de la orden |
| dealsize | TEXT | Tamaño del negocio (Small/Medium/Large) |
| customername | TEXT | Nombre del cliente empresa |
| producto_id | INTEGER | Llave hacia dim_producto |
| cliente_id | INTEGER | Llave hacia dim_cliente |
| region_id | INTEGER | Llave hacia dim_region |
| tiempo_id | INTEGER | Llave hacia dim_tiempo |

**¿Por qué no tiene la fecha directamente?**
En el modelo estrella las fechas viven en `dim_tiempo`. Esto permite hacer análisis temporales complejos como agrupar por trimestre, mes o día de la semana de forma muy eficiente.

---

### dim_producto — Dimensión de productos

| Columna | Tipo | Descripción |
|---|---|---|
| producto_id | INTEGER | Identificador único (PK) |
| producto_nombre | TEXT | Código del producto |
| categoria | TEXT | Línea de producto |

---

### dim_cliente — Dimensión de clientes

| Columna | Tipo | Descripción |
|---|---|---|
| cliente_id | INTEGER | Identificador único (PK) |
| nombre | TEXT | Nombre completo |
| ciudad | TEXT | Ciudad de residencia |
| pais | TEXT | País de residencia |

---

### dim_region — Dimensión geográfica

| Columna | Tipo | Descripción |
|---|---|---|
| region_id | SERIAL | Identificador único (PK) |
| pais | TEXT | Nombre del país |
| continente | TEXT | Continente |
| subregion | TEXT | Subregión geográfica |
| capital | TEXT | Ciudad capital |

**¿Por qué una dimensión de región separada?**
Permite analizar las ventas desde múltiples perspectivas geográficas: por país, por continente o por subregión. Si esta información estuviera en `fact_ventas` habría datos repetidos en miles de filas.

---

### dim_tiempo — Dimensión de tiempo

| Columna | Tipo | Descripción |
|---|---|---|
| tiempo_id | SERIAL | Identificador único (PK) |
| fecha | DATE | Fecha completa |
| anio | INTEGER | Año |
| mes | INTEGER | Número de mes |
| nombre_mes | TEXT | Nombre del mes |
| trimestre | INTEGER | Trimestre (1-4) |
| dia | INTEGER | Día del mes |

**¿Por qué construir esta tabla?**
La dimensión de tiempo es una de las más importantes en cualquier modelo analítico. Permite filtrar y agrupar por cualquier nivel temporal — año, trimestre, mes o día — sin necesidad de hacer cálculos en el momento de la consulta.

Se construyó automáticamente a partir de las fechas únicas del dataset de ventas.

---

# 04 — Star Schema

This document explains what the star schema is, why it was chosen for this project, and how it is implemented.

---

## What is the star schema?

The star schema is a way of organizing data in a database specifically designed for analytics and reporting. It gets its name because it visually resembles a star: there is a central table surrounded by supporting tables.

It is composed of two types of tables:

**Fact table (FACT)**
It contains measurable business events, in this case sales. It includes numeric metrics such as sales amount, quantity, and price. It also contains the keys that connect it to the other tables.

**Dimension tables (DIM)**
They contain the context for the facts: who bought, what was sold, where, and when. They are descriptive tables that allow the data to be filtered and grouped in different ways.

---

## Why do we use the star schema?

The star schema was chosen for three main reasons:

**1. Performance in analytical queries**
Visualization tools such as Power BI are optimized to work with this model. Queries run faster because the data is organized in a way that avoids complex operations.

**2. Ease of use in Power BI**
Power BI automatically detects and uses star schema relationships. This makes it possible to create visualizations by dragging fields without writing code.

**3. Conceptual clarity**
The star schema makes it easy to understand what each table contains and how they relate to one another. Anyone on the team can understand the structure without being a database expert.

---

## Implemented Structure

```
                  dim_producto
                  (producto_id)
                       |
                       |
dim_cliente ———— fact_ventas ———— dim_region
(cliente_id)    (central table)  (region_id)
                       |
                       |
                  dim_tiempo
                  (tiempo_id)
```

---

## Details of Each Table

### fact_ventas — Fact table

This is the central table of the model. It contains the data for each sales line.

| Column | Type | Description |
|---|---|---|
| ordernumber | INTEGER | Order number |
| quantityordered | INTEGER | Quantity sold |
| priceeach | NUMERIC | Unit price |
| sales | NUMERIC | Total sales amount |
| status | TEXT | Order status |
| dealsize | TEXT | Deal size (Small/Medium/Large) |
| customername | TEXT | Company customer name |
| producto_id | INTEGER | Key to dim_producto |
| cliente_id | INTEGER | Key to dim_cliente |
| region_id | INTEGER | Key to dim_region |
| tiempo_id | INTEGER | Key to dim_tiempo |

**Why doesn’t it store the date directly?**
In the star schema, dates live in `dim_tiempo`. This enables complex time analysis such as grouping by quarter, month, or day of the week very efficiently.

---

### dim_producto — Product dimension

| Column | Type | Description |
|---|---|---|
| producto_id | INTEGER | Unique identifier (PK) |
| producto_nombre | TEXT | Product code |
| categoria | TEXT | Product line |

---

### dim_cliente — Customer dimension

| Column | Type | Description |
|---|---|---|
| cliente_id | INTEGER | Unique identifier (PK) |
| nombre | TEXT | Full name |
| ciudad | TEXT | City of residence |
| pais | TEXT | Country of residence |

---

### dim_region — Geographic dimension

| Column | Type | Description |
|---|---|---|
| region_id | SERIAL | Unique identifier (PK) |
| pais | TEXT | Country name |
| continente | TEXT | Continent |
| subregion | TEXT | Geographic subregion |
| capital | TEXT | Capital city |

**Why a separate region dimension?**
It allows sales to be analyzed from multiple geographic perspectives: by country, continent, or subregion. If this information were stored in `fact_ventas`, the data would be repeated across thousands of rows.

---

### dim_tiempo — Time dimension

| Column | Type | Description |
|---|---|---|
| tiempo_id | SERIAL | Unique identifier (PK) |
| fecha | DATE | Full date |
| anio | INTEGER | Year |
| mes | INTEGER | Month number |
| nombre_mes | TEXT | Month name |
| trimestre | INTEGER | Quarter (1-4) |
| dia | INTEGER | Day of the month |

**Why build this table?**
The time dimension is one of the most important in any analytical model. It allows filtering and grouping by any time level, year, quarter, month, or day, without needing calculations at query time.

It was built automatically from the unique dates in the sales dataset.

---
