# 01 — Instalación desde cero

Esta guía explica todo lo que necesitas instalar y configurar para que el proyecto funcione correctamente desde cero.

---

## Requisitos previos

Antes de empezar necesitas tener instalado lo siguiente en tu sistema:

| Software | Versión mínima | Descarga |
|---|---|---|
| Python | 3.10 o superior | https://www.python.org |
| VS Code | Cualquier versión reciente | https://code.visualstudio.com |
| DBeaver Community | Cualquier versión reciente | https://dbeaver.io |
| Power BI Desktop | Cualquier versión reciente | https://powerbi.microsoft.com |
| PostgreSQL | Servidor externo o local | — |

> **Nota para Linux:** El comando de Python en Linux es `python3` en lugar de `python`. Una vez activado el ambiente virtual ambos funcionan igual.

---

## Paso 1 — Clonar o descargar el proyecto

Si tienes Git instalado:
```bash
git clone <url-del-repositorio>
cd emausoft_analytics
```

Si no tienes Git, descarga el proyecto como ZIP y descomprímelo.

---

## Paso 2 — Crear el ambiente virtual

Un ambiente virtual es una carpeta aislada donde se instalan las librerías del proyecto sin afectar el resto del sistema. Es una buena práctica que evita conflictos entre proyectos.

```bash
# En Linux/Mac
python3 -m venv venv

# En Windows
python -m venv venv
```

---

## Paso 3 — Activar el ambiente virtual

Debes activar el ambiente virtual **cada vez** que abras una terminal nueva para trabajar en el proyecto.

```bash
# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

Sabrás que está activo porque verás `(venv)` al inicio de la línea de la terminal.

---

## Paso 4 — Instalar las librerías

Con el ambiente virtual activo instala todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Las librerías principales son:

| Librería | Para qué se usa |
|---|---|
| `pandas` | Manipulación y limpieza de datos |
| `requests` | Consumo de APIs externas |
| `sqlalchemy` | Conexión a la base de datos desde Python |
| `psycopg2-binary` | Driver de PostgreSQL para Python |
| `python-dotenv` | Leer variables de entorno desde el archivo `.env` |
| `jupyter` | Ejecutar los notebooks de exploración |
| `openpyxl` | Soporte para archivos Excel si se necesita |

---

## Paso 5 — Configurar las variables de entorno

Crea un archivo llamado `.env` en la raíz del proyecto con los datos de conexión a PostgreSQL:

```
DB_HOST=<ip-del-servidor>
DB_PORT=5432
DB_NAME=echandia_db
DB_USER=<usuario>
DB_PASSWORD=<contraseña>
```

> **Importante:** El archivo `.env` contiene contraseñas y nunca debe subirse a un repositorio público. El archivo `.gitignore` ya está configurado para ignorarlo.

---

## Paso 6 — Extensiones de VS Code recomendadas

Instala estas extensiones desde el panel de extensiones de VS Code (`Ctrl + Shift + X`):

| Extensión | Para qué sirve |
|---|---|
| Jupyter (Microsoft) | Ejecutar notebooks `.ipynb` dentro de VS Code |
| Python (Microsoft) | Soporte completo para Python |
| SQLTools | Conectar y consultar bases de datos desde VS Code |

---

## Paso 7 — Configurar DBeaver

1. Abre DBeaver
2. Ve a `Archivo → Nueva conexión`
3. Selecciona **PostgreSQL**
4. Llena los datos con las mismas variables del `.env`
5. Haz clic en **Probar conexión** para verificar

---

## Paso 8 — Descargar el dataset de ventas

1. Ve a https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
2. Descarga el archivo `sales_data_sample.csv`
3. Colócalo en la carpeta `1_data/`

---

## Paso 9 — Crear las tablas en PostgreSQL

1. Abre DBeaver y conéctate a la base de datos
2. Abre el archivo `5_db/crear_tablas.sql`
3. Ejecuta el script completo con `Ctrl + A` y luego `Ctrl + Enter`

---

## Paso 10 — Ejecutar el pipeline de carga

Con el ambiente virtual activo y las tablas creadas:

```bash
cd 3_scripts
python cargar_datos.py
```

Si todo está bien verás un resumen como este:

```
[HH:MM:SS] Iniciando pipeline — Modelo Estrella
[HH:MM:SS] dim_producto    → 109 filas insertadas ✅
[HH:MM:SS] dim_cliente     → 100 filas insertadas ✅
[HH:MM:SS] dim_region      → 250 filas insertadas ✅
[HH:MM:SS] dim_tiempo      → 252 filas insertadas ✅
[HH:MM:SS] fact_ventas     → 2,823 filas insertadas ✅
[HH:MM:SS] Pipeline completado ✅
```

---

## Verificación final

Ejecuta esta consulta en DBeaver para confirmar que todo está cargado:

```sql
SELECT 'dim_producto' AS tabla, COUNT(*) AS filas FROM dim_producto
UNION ALL
SELECT 'dim_cliente',  COUNT(*) FROM dim_cliente
UNION ALL
SELECT 'dim_region',   COUNT(*) FROM dim_region
UNION ALL
SELECT 'dim_tiempo',   COUNT(*) FROM dim_tiempo
UNION ALL
SELECT 'fact_ventas',  COUNT(*) FROM fact_ventas;
```

Resultado esperado:

```
dim_producto  |  109
dim_cliente   |  100
dim_region    |  250
dim_tiempo    |  252
fact_ventas   | 2823
```

---

# 01 — Setup from Scratch

This guide explains everything you need to install and configure so the project works correctly from scratch.

---

## Prerequisites

Before starting, you need to have the following installed on your system:

| Software | Minimum Version | Download |
|---|---|---|
| Python | 3.10 or higher | https://www.python.org |
| VS Code | Any recent version | https://code.visualstudio.com |
| DBeaver Community | Any recent version | https://dbeaver.io |
| Power BI Desktop | Any recent version | https://powerbi.microsoft.com |
| PostgreSQL | External or local server | — |

> **Note for Linux:** The Python command on Linux is `python3` instead of `python`. Once the virtual environment is activated, both work the same.

---

## Step 1 — Clone or Download the Project

If you have Git installed:
```bash
git clone <repository-url>
cd emausoft_analytics
```

If you do not have Git, download the project as a ZIP file and extract it.

---

## Step 2 — Create the Virtual Environment

A virtual environment is an isolated folder where the project's libraries are installed without affecting the rest of the system. It is a good practice that prevents conflicts between projects.

```bash
# On Linux/Mac
python3 -m venv venv

# On Windows
python -m venv venv
```

---

## Step 3 — Activate the Virtual Environment

You must activate the virtual environment **every time** you open a new terminal to work on the project.

```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

You will know it is active because you will see `(venv)` at the beginning of the terminal line.

---

## Step 4 — Install the Libraries

With the virtual environment active, install all project dependencies:

```bash
pip install -r requirements.txt
```

The main libraries are:

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation and cleaning |
| `requests` | External API consumption |
| `sqlalchemy` | Database connection from Python |
| `psycopg2-binary` | PostgreSQL driver for Python |
| `python-dotenv` | Read environment variables from the `.env` file |
| `jupyter` | Run exploration notebooks |
| `openpyxl` | Support for Excel files if needed |

---

## Step 5 — Configure Environment Variables

Create a file named `.env` in the project root with the PostgreSQL connection information:

```
DB_HOST=<server-ip>
DB_PORT=5432
DB_NAME=echandia_db
DB_USER=<user>
DB_PASSWORD=<password>
```

> **Important:** The `.env` file contains passwords and should never be uploaded to a public repository. The `.gitignore` file is already configured to ignore it.

---

## Step 6 — Recommended VS Code Extensions

Install these extensions from the VS Code extensions panel (`Ctrl + Shift + X`):

| Extension | Purpose |
|---|---|
| Jupyter (Microsoft) | Run `.ipynb` notebooks inside VS Code |
| Python (Microsoft) | Full Python support |
| SQLTools | Connect to and query databases from VS Code |

---

## Step 7 — Configure DBeaver

1. Open DBeaver
2. Go to `File → New connection`
3. Select **PostgreSQL**
4. Fill in the data using the same values from `.env`
5. Click **Test connection** to verify

---

## Step 8 — Download the Sales Dataset

1. Go to https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
2. Download the file `sales_data_sample.csv`
3. Place it in the `1_data/` folder

---

## Step 9 — Create the Tables in PostgreSQL

1. Open DBeaver and connect to the database
2. Open the file `5_db/crear_tablas.sql`
3. Run the full script with `Ctrl + A` and then `Ctrl + Enter`

---

## Step 10 — Run the Load Pipeline

With the virtual environment active and the tables created:

```bash
cd 3_scripts
python cargar_datos.py
```

If everything is correct, you will see a summary like this:

```
[HH:MM:SS] Starting pipeline — Star Schema
[HH:MM:SS] dim_producto    → 109 rows inserted ✅
[HH:MM:SS] dim_cliente     → 100 rows inserted ✅
[HH:MM:SS] dim_region      → 250 rows inserted ✅
[HH:MM:SS] dim_tiempo      → 252 rows inserted ✅
[HH:MM:SS] fact_ventas     → 2,823 rows inserted ✅
[HH:MM:SS] Pipeline completed ✅
```

---

## Final Verification

Run this query in DBeaver to confirm that everything was loaded:

```sql
SELECT 'dim_producto' AS tabla, COUNT(*) AS filas FROM dim_producto
UNION ALL
SELECT 'dim_cliente',  COUNT(*) FROM dim_cliente
UNION ALL
SELECT 'dim_region',   COUNT(*) FROM dim_region
UNION ALL
SELECT 'dim_tiempo',   COUNT(*) FROM dim_tiempo
UNION ALL
SELECT 'fact_ventas',  COUNT(*) FROM fact_ventas;
```

Expected result:

```
dim_producto  |  109
dim_cliente   |  100
dim_region    |  250
dim_tiempo    |  252
fact_ventas   | 2823
```
