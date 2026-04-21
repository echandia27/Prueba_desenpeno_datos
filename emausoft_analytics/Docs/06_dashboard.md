# 06 — Dashboard y hallazgos

Este documento explica la estructura del dashboard construido en Power BI, las decisiones de visualización y los hallazgos del análisis.

---

## Conexión a PostgreSQL

Power BI se conectó directamente a la base de datos PostgreSQL usando el driver Npgsql. Se importaron las 5 tablas del modelo estrella y Power BI detectó automáticamente la mayoría de las relaciones gracias a los nombres de las llaves foráneas.

Las relaciones son todas de tipo **muchos a uno (*:1)**:
- Muchas ventas → un producto
- Muchas ventas → un cliente
- Muchas ventas → una región
- Muchas ventas → un momento en el tiempo

---

## Estructura del dashboard

El dashboard tiene 3 páginas, cada una enfocada en responder un conjunto de preguntas de negocio.

---

## Página 1 — Resumen General

**Preguntas que responde:**
- ¿Cómo han evolucionado las ventas en el tiempo?
- ¿Qué países generan más ingresos?

**Visualizaciones:**

| Visualización | Campos | Propósito |
|---|---|---|
| Tarjeta Total Ventas | `fact_ventas.sales` (suma) | KPI principal del negocio |
| Tarjeta Total Órdenes | `fact_ventas.ordernumber` (conteo distinto) | Volumen de transacciones |
| Tarjeta Unidades Vendidas | `fact_ventas.quantityordered` (suma) | Volumen de productos |
| Tarjeta Precio Promedio | `fact_ventas.priceeach` (promedio) | Ticket promedio |
| Gráfico de líneas | Eje X: fecha, Eje Y: sales | Tendencia temporal de ventas |
| Gráfico de barras | Eje Y: país, Eje X: sales | Ranking de países por ventas |
| Segmentador | `dim_tiempo.anio` | Filtro por año |

---

## Página 2 — Productos y Clientes

**Preguntas que responde:**
- ¿Qué productos tienen mejor desempeño?
- ¿Qué productos tienen menor impacto?
- ¿Qué tipo de clientes generan mayor valor?

**Visualizaciones:**

| Visualización | Campos | Propósito |
|---|---|---|
| Gráfico de barras | Eje Y: categoria, Eje X: sales | Ventas por nombre de producto |
| Gráfico de dona | Leyenda: categoria, Valores: sales | Participación por categoría |
| Gráfico de barras | Eje Y: dealsize, Eje X: sales | Ventas por tamaño de negocio |
| Gráfico de barras | Eje Y: customername, Eje X: sales | Top clientes por ventas |
| Segmentador | `dim_producto.categoria` | Filtro por categoría |


---

## Página 3 — Análisis Geográfico

**Preguntas que responde:**
- ¿Qué regiones presentan bajo rendimiento?
- ¿Existe relación entre ubicación y comportamiento de compra?

**Visualizaciones:**

| Visualización | Campos | Propósito |
|---|---|---|
| Mapa | Ubicación: país, Tamaño: sales | Distribución geográfica de ventas |
| Gráfico de dona | Leyenda: continente, Valores: sales | Participación por continente |
| Gráfico de barras | Eje Y: subregion, Eje X: sales | Ventas por subregión |
| Gráfico de barras apiladas | Eje Y: país, Eje X: sales, Leyenda: categoria | Ventas por país y categoría |
| Segmentador | `dim_region.continente` | Filtro por continente |

---

## Hallazgos del análisis

### Evolución temporal
Las ventas muestran un patrón estacional claro con picos en el último trimestre de cada año. El año 2004 fue el de mayor volumen de ventas del período analizado (2003-2005).

### Geografía
Estados Unidos es el mercado más importante por volumen de ventas, seguido de España y Francia. La región de Europa Occidental concentra la mayor parte de los ingresos fuera de América del Norte.

Las regiones con menor rendimiento son Asia y Oceanía donde hay muy pocos países activos — Japón, Singapur, Australia y Filipinas concentran todo el volumen.

### Productos
La categoría **Classic Cars** es la de mayor impacto en ventas, seguida de **Vintage Cars**. Las categorías de menor impacto son **Trains** y **Ships**.

### Clientes y tamaño de negocio
Los negocios de tamaño **Medium** generan el mayor volumen de ventas, seguidos de **Small**. Los negocios **Large** son pocos pero de alto valor individual.

---

## Recomendaciones al negocio

1. **Reforzar mercados clave:** Estados Unidos, España y Francia concentran la mayor parte de las ventas. Se recomienda invertir en retención y expansión en estos mercados.

2. **Explorar mercados de bajo rendimiento:** Asia y Oceanía tienen presencia pero bajo volumen. Hay oportunidad de crecimiento con estrategias de penetración de mercado enfocadas.

3. **Apostar por Classic Cars:** Es la categoría más rentable. Se recomienda ampliar el catálogo y asegurar disponibilidad de inventario.

4. **Revisar categorías de bajo impacto:** Trains y Ships tienen muy bajo volumen. Se debe evaluar si son rentables o si los recursos se pueden redirigir a categorías más fuertes.

5. **Aprovechar la estacionalidad:** Los picos de ventas en el último trimestre del año son una oportunidad para campañas de marketing anticipadas y gestión de inventario.

6. **Atención a clientes Medium:** Son el segmento que más volumen genera. Programas de fidelización dirigidos a este segmento podrían tener alto impacto en los ingresos.

---

# 06 — Dashboard and Findings

This document explains the structure of the dashboard built in Power BI, the visualization decisions, and the key findings from the analysis.

---

## PostgreSQL Connection

Power BI was connected directly to the PostgreSQL database using the Npgsql driver. The 5 tables from the star schema were imported, and Power BI automatically detected most of the relationships thanks to the foreign key names.

The relationships are all **many-to-one (*:1)**:
- Many sales → one product
- Many sales → one customer
- Many sales → one region
- Many sales → one point in time

---

## Dashboard Structure

The dashboard has 3 pages, each focused on answering a set of business questions.

---

## Page 1 — Executive Summary

**Questions it answers:**
- How have sales evolved over time?
- Which countries generate the most revenue?

**Visualizations:**

| Visualization | Fields | Purpose |
|---|---|---|
| Total Sales Card | `fact_ventas.sales` (sum) | Main business KPI |
| Total Orders Card | `fact_ventas.ordernumber` (distinct count) | Transaction volume |
| Units Sold Card | `fact_ventas.quantityordered` (sum) | Product volume |
| Average Price Card | `fact_ventas.priceeach` (average) | Average ticket |
| Line chart | X-axis: date, Y-axis: sales | Sales time trend |
| Bar chart | Y-axis: country, X-axis: sales | Country sales ranking |
| Slicer | `dim_tiempo.anio` | Year filter |

---

## Page 2 — Products and Customers

**Questions it answers:**
- Which products perform best?
- Which products have the lowest impact?
- What type of customers generate the most value?

**Visualizations:**

| Visualization | Fields | Purpose |
|---|---|---|
| Bar chart | Y-axis: categoria, X-axis: sales | Sales by product category |
| Donut chart | Legend: categoria, Values: sales | Category share |
| Bar chart | Y-axis: dealsize, X-axis: sales | Sales by deal size |
| Bar chart | Y-axis: customername, X-axis: sales | Top customers by sales |
| Slicer | `dim_producto.categoria` | Category filter |

---

## Page 3 — Geographic Analysis

**Questions it answers:**
- Which regions show low performance?
- Is there a relationship between location and purchasing behavior?

**Visualizations:**

| Visualization | Fields | Purpose |
|---|---|---|
| Map | Location: country, Size: sales | Geographic sales distribution |
| Donut chart | Legend: continente, Values: sales | Share by continent |
| Bar chart | Y-axis: subregion, X-axis: sales | Sales by subregion |
| Stacked bar chart | Y-axis: country, X-axis: sales, Legend: categoria | Sales by country and category |
| Slicer | `dim_region.continente` | Continent filter |

---

## Analysis Findings

### Time Evolution
Sales show a clear seasonal pattern with peaks in the last quarter of each year. The year 2004 had the highest sales volume in the analyzed period (2003-2005).

### Geography
The United States is the most important market by sales volume, followed by Spain and France. Western Europe concentrates most of the revenue outside North America.

The lowest-performing regions are Asia and Oceania, where there are very few active countries. Japan, Singapore, Australia, and the Philippines account for all the volume.

### Products
The **Classic Cars** category has the greatest impact on sales, followed by **Vintage Cars**. The lowest-impact categories are **Trains** and **Ships**.

### Customers and Deal Size
**Medium** deals generate the highest sales volume, followed by **Small** deals. **Large** deals are fewer in number but have high individual value.

---

## Business Recommendations

1. **Strengthen key markets:** The United States, Spain, and France account for most sales. Investing in retention and expansion in these markets is recommended.

2. **Explore low-performing markets:** Asia and Oceania have presence but low volume. There is growth potential with focused market penetration strategies.

3. **Invest in Classic Cars:** It is the most profitable category. Expanding the catalog and ensuring inventory availability is recommended.

4. **Review low-impact categories:** Trains and Ships have very low volume. Their profitability should be evaluated, or resources should be redirected to stronger categories.

5. **Take advantage of seasonality:** Sales peaks in the last quarter of the year create an opportunity for early marketing campaigns and inventory planning.

6. **Focus on Medium customers:** This segment generates the highest volume. Loyalty programs targeted at this segment could have a strong impact on revenue.
