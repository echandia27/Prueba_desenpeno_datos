-- EMAUSOFT ANALYTICS — Modelo Estrella
-- PostgreSQL

-- Dimensión producto
CREATE TABLE IF NOT EXISTS dim_producto (
    producto_id      INTEGER PRIMARY KEY,
    producto_nombre  TEXT NOT NULL,
    categoria        TEXT
);

-- Dimensión cliente
CREATE TABLE IF NOT EXISTS dim_cliente (
    cliente_id  INTEGER PRIMARY KEY,
    nombre      TEXT NOT NULL,
    ciudad      TEXT,
    pais        TEXT
);

-- Dimensión región
CREATE TABLE IF NOT EXISTS dim_region (
    region_id   SERIAL PRIMARY KEY,
    pais        TEXT NOT NULL,
    continente  TEXT,
    subregion   TEXT,
    capital     TEXT
);

-- Dimensión tiempo
CREATE TABLE IF NOT EXISTS dim_tiempo (
    tiempo_id   SERIAL PRIMARY KEY,
    fecha       DATE NOT NULL UNIQUE,
    anio        INTEGER,
    mes         INTEGER,
    nombre_mes  TEXT,
    trimestre   INTEGER,
    dia         INTEGER
);

-- Tabla de hechos — fact_ventas
-- Solo contiene métricas e IDs que apuntan a las dimensiones
CREATE TABLE IF NOT EXISTS fact_ventas (
    ordernumber      INTEGER,
    quantityordered  INTEGER,
    priceeach        NUMERIC,
    sales            NUMERIC,
    status           TEXT,
    dealsize         TEXT,
    customername     TEXT,
    producto_id      INTEGER,
    cliente_id       INTEGER,
    region_id        INTEGER,
    tiempo_id        INTEGER,
    FOREIGN KEY (producto_id) REFERENCES dim_producto(producto_id),
    FOREIGN KEY (cliente_id)  REFERENCES dim_cliente(cliente_id),
    FOREIGN KEY (region_id)   REFERENCES dim_region(region_id),
    FOREIGN KEY (tiempo_id)   REFERENCES dim_tiempo(tiempo_id)
);