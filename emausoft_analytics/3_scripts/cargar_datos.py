# Emausoft Analytics — Pipeline de carga Modelo Estrella

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os
import sys

# ── Cargar variables de entorno ───
load_dotenv('../.env')

DB_URI = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URI)

def log(mensaje):
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] {mensaje}")

def insertar_batch(df: pd.DataFrame, tabla: str):
    df.to_sql(
        tabla,
        engine,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=1000
    )
    log(f"{tabla:15s} → {len(df):,} filas insertadas ✅")

def cargar():
    log("Iniciando pipeline — Modelo Estrella")
    print("=" * 55)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # ── EXTRAER ──────
    log("EXTRAER → Leyendo archivos CSV...")
    ventas   = pd.read_csv(os.path.join(BASE_DIR, '../4_output/ventas_limpio.csv'))
    productos = pd.read_csv(os.path.join(BASE_DIR, '../4_output/productos.csv'))
    clientes  = pd.read_csv(os.path.join(BASE_DIR, '../4_output/clientes.csv'))
    regiones  = pd.read_csv(os.path.join(BASE_DIR, '../4_output/regiones.csv'))
    log(f"  ventas    → {len(ventas):,} filas")
    log(f"  productos → {len(productos):,} filas")
    log(f"  clientes  → {len(clientes):,} filas")
    log(f"  regiones  → {len(regiones):,} filas")
    print("=" * 55)

    # ── TRANSFORMAR PARA MODELO ESTRELLA ─────
    log("TRANSFORMAR → Preparando dimensiones...")

    # dim_producto — ya está lista
    dim_producto = productos.rename(columns={
        'producto_nombre': 'producto_nombre',
        'categoria': 'categoria'
    })

    # dim_cliente — ya está lista
    dim_cliente = clientes.copy()

    # dim_region — agregar region_id
    dim_region = regiones.copy()
    dim_region.insert(0, 'region_id', range(1, len(dim_region) + 1))

    # dim_tiempo — construir desde las fechas de ventas
    ventas['orderdate'] = pd.to_datetime(ventas['orderdate'])
    fechas_unicas = ventas['orderdate'].dt.normalize().drop_duplicates().sort_values()

    dim_tiempo = pd.DataFrame({
        'fecha'     : fechas_unicas,
        'anio'      : fechas_unicas.dt.year,
        'mes'       : fechas_unicas.dt.month,
        'nombre_mes': fechas_unicas.dt.strftime('%B'),
        'trimestre' : fechas_unicas.dt.quarter,
        'dia'       : fechas_unicas.dt.day
    }).reset_index(drop=True)
    dim_tiempo.insert(0, 'tiempo_id', range(1, len(dim_tiempo) + 1))

    log(f"  dim_tiempo  → {len(dim_tiempo)} fechas únicas")
    log(f"  dim_region  → {len(dim_region)} regiones")

    # fact_ventas — unir los IDs correctos
    log("TRANSFORMAR → Construyendo fact_ventas...")

    # Unir region_id
    ventas = ventas.merge(
        dim_region[['region_id', 'pais']],
        left_on='country',
        right_on='pais',
        how='left'
    ).drop(columns=['pais'])

    # Unir tiempo_id
    ventas = ventas.merge(
        dim_tiempo[['tiempo_id', 'fecha']],
        left_on='orderdate',
        right_on='fecha',
        how='left'
    ).drop(columns=['fecha'])

    # Seleccionar solo columnas de fact_ventas
    fact_ventas = ventas[[
        'ordernumber', 'quantityordered', 'priceeach',
        'sales', 'status', 'dealsize', 'customername',
        'producto_id', 'cliente_id', 'region_id', 'tiempo_id'
    ]]

    log(f"  fact_ventas → {len(fact_ventas):,} filas")
    print("=" * 55)

    # ── CARGAR ───────
    log("CARGAR → Insertando en PostgreSQL...")
    insertar_batch(dim_producto, 'dim_producto')
    insertar_batch(dim_cliente,  'dim_cliente')
    insertar_batch(dim_region,   'dim_region')
    insertar_batch(dim_tiempo,   'dim_tiempo')
    insertar_batch(fact_ventas,  'fact_ventas')

    print("=" * 55)
    log("Pipeline completado ✅")

if __name__ == "__main__":
    cargar()