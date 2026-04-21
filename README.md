# Emausoft Analytics — Solución Analítica End-to-End

## ¿Qué es este proyecto?

Este proyecto construye una solución analítica completa para **Emausoft**, una empresa SaaS que gestiona información comercial de pequeñas y medianas empresas en Latinoamérica.

El objetivo es transformar datos fragmentados e inconsistentes en información útil para la toma de decisiones, a través de un pipeline completo que va desde la extracción de datos hasta un dashboard interactivo.

---

## Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python 3 | Procesamiento y transformación de datos |
| Pandas | Manipulación y limpieza de datos |
| Requests | Consumo de APIs externas |
| SQLAlchemy + Psycopg2 | Conexión y carga a PostgreSQL |
| PostgreSQL | Base de datos relacional |
| DBeaver | Administración de la base de datos |
| Power BI Desktop | Dashboard y visualizaciones |
| VS Code | Entorno de desarrollo |

---

## Estructura del proyecto

```
emausoft_analytics/
├── 1_data/                        # Datos crudos sin modificar
│   └── sales_data_sample.csv      # Dataset de ventas (Kaggle)
├── 2_notebooks/                   # Exploración y análisis
│   ├── 01_exploracion_ventas.ipynb
│   └── 02_consumo_apis.ipynb
├── 3_scripts/                     # Código Python limpio
│   └── cargar_datos.py            # Pipeline ETL
├── 4_output/                      # Tablas limpias exportadas
│   ├── ventas_limpio.csv
│   ├── productos.csv
│   ├── clientes.csv
│   └── regiones.csv
├── 5_db/                          # Scripts de base de datos
│   └── crear_tablas.sql
├── docs/                          # Documentación detallada
│   ├── 01_instalacion.md
│   ├── 02_fuentes_de_datos.md
│   ├── 03_exploracion_limpieza.md
│   ├── 04_modelo_estrella.md
│   ├── 05_pipeline_carga.md
│   └── 06_dashboard.md
├── .env                           # Variables de entorno (no subir a Git)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Flujo del proyecto

```
Fuentes de datos
      ↓
Python (Notebooks) → Exploración y limpieza
      ↓
Python (Script)    → Pipeline ETL
      ↓
PostgreSQL         → Modelo estrella
      ↓
Power BI           → Dashboard interactivo
```

---

## Preguntas de negocio que responde el dashboard

1. ¿Cómo han evolucionado las ventas en el tiempo?
2. ¿Qué países o regiones generan más ingresos?
3. ¿Qué productos tienen mejor desempeño?
4. ¿Qué regiones presentan bajo rendimiento?
5. ¿Qué productos tienen menor impacto en ventas?
6. ¿Qué tipo de clientes generan mayor valor?
7. ¿Existe relación entre ubicación y comportamiento de compra?
8. ¿Qué acciones recomendarías al negocio?

---

## Documentación completa

Para entender cada decisión técnica del proyecto consulta la carpeta `emausoft_analytics/Docs/`:

- [Instalación desde cero](emausoft_analytics/Docs/01_instalacion.md)
- [Fuentes de datos](emausoft_analytics/Docs/02_fuentes_de_datos.md)
- [Exploración y limpieza](emausoft_analytics/Docs/03_exploracion_limpieza.md)
- [Modelo estrella](emausoft_analytics/Docs/04_modelo_estrella.md)
- [Pipeline de carga](emausoft_analytics/Docs/05_pipeline_carga.md)
- [Dashboard](emausoft_analytics/Docs/06_dashboard.md)

---

# Emausoft Analytics — End-to-End Analytics Solution

## What is this project?

This project builds a complete analytics solution for **Emausoft**, a SaaS company that manages commercial information for small and medium-sized businesses in Latin America.

The goal is to transform fragmented and inconsistent data into useful information for decision-making through a full pipeline that goes from data extraction to an interactive dashboard.

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Data processing and transformation |
| Pandas | Data manipulation and cleaning |
| Requests | External API consumption |
| SQLAlchemy + Psycopg2 | PostgreSQL connection and loading |
| PostgreSQL | Relational database |
| DBeaver | Database administration |
| Power BI Desktop | Dashboard and visualizations |
| VS Code | Development environment |

---

## Project Structure

```
emausoft_analytics/
├── 1_data/                        # Raw data without modifications
│   └── sales_data_sample.csv      # Sales dataset (Kaggle)
├── 2_notebooks/                   # Exploration and analysis
│   ├── 01_exploracion_ventas.ipynb
│   └── 02_consumo_apis.ipynb
├── 3_scripts/                     # Clean Python code
│   └── cargar_datos.py            # ETL pipeline
├── 4_output/                      # Exported clean tables
│   ├── ventas_limpio.csv
│   ├── productos.csv
│   ├── clientes.csv
│   └── regiones.csv
├── 5_db/                          # Database scripts
│   └── crear_tablas.sql
├── docs/                          # Detailed documentation
│   ├── 01_instalacion.md
│   ├── 02_fuentes_de_datos.md
│   ├── 03_exploracion_limpieza.md
│   ├── 04_modelo_estrella.md
│   ├── 05_pipeline_carga.md
│   └── 06_dashboard.md
├── .env                           # Environment variables (do not upload)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Project Flow

```
Data sources
      ↓
Python (Notebooks) → Exploration and cleaning
      ↓
Python (Script)    → ETL pipeline
      ↓
PostgreSQL         → Star schema
      ↓
Power BI           → Interactive dashboard
```

---

## Business Questions Answered by the Dashboard

1. How have sales evolved over time?
2. Which countries or regions generate the most revenue?
3. Which products perform best?
4. Which regions show low performance?
5. Which products have the least impact on sales?
6. What type of customers generate the most value?
7. Is there a relationship between location and purchasing behavior?
8. What actions would you recommend to the business?

---

## Full Documentation

To understand each technical decision in the project, review the `emausoft_analytics/Docs/` folder:

- [Setup from scratch](emausoft_analytics/Docs/01_instalacion.md)
- [Data sources](emausoft_analytics/Docs/02_fuentes_de_datos.md)
- [Exploration and cleaning](emausoft_analytics/Docs/03_exploracion_limpieza.md)
- [Star schema](emausoft_analytics/Docs/04_modelo_estrella.md)
- [Load pipeline](emausoft_analytics/Docs/05_pipeline_carga.md)
- [Dashboard](emausoft_analytics/Docs/06_dashboard.md)
