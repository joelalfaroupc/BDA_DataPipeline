# BDA Data Pipeline

Proyecto de Large-Scale Data Engineering for AI centrado en Barcelona, turismo y Airbnb.

La entrega final esta organizada por fases y en formato notebook-only:

- [landing_zone/landing.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone/landing.ipynb)
- [formatted_zone/formatted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted.ipynb)
- [trusted_zone/trusted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted.ipynb)
- [exploitation_zone/exploitation.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation.ipynb)
- [analysis_zone/analysis.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/analysis.ipynb)

Los notebooks conservan sus outputs en las celdas. No se generan reportes JSON externos.

## Artefactos persistidos

- CSV raw versionados solo en `landing_zone/raw`
- [formatted_zone/formatted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted_zone.duckdb)
- [trusted_zone/trusted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted_zone.duckdb)
- [exploitation_zone/exploitation_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation_zone.duckdb)

## Orden recomendado

1. `landing`
2. `formatted`
3. `trusted`
4. `exploitation`
5. `analysis`

## Requisitos

- Python 3
- Java 21 para ejecutar Spark
- PySpark
- DuckDB
- Jupyter Notebook

El resumen extendido esta en [RESUMEN_PROYECTO.md](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/RESUMEN_PROYECTO.md).
