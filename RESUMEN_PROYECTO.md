# Resumen Del Proyecto

## Objetivo

El proyecto implementa una pipeline end-to-end para integrar fuentes heterogeneas sobre Barcelona y construir una base analitica sobre turismo, alojamiento, Airbnb, meteorologia, renta y licencias HUT.

La entrega queda organizada en cinco fases:

- `Landing Zone`
- `Formatted Zone`
- `Trusted Zone`
- `Exploitation Zone`
- `Analysis Zone`

Cada fase tiene su propio notebook autocontenido y sus outputs quedan embebidos en el `.ipynb`. Como artefactos externos solo se conservan los CSV raw de landing y las bases DuckDB de las zonas relacionales.

## Fuentes De Datos

Se integran nueve fuentes:

- puntos de interes de OpenDataBCN
- hoteles de OpenDataBCN
- meteorologia
- listings de Airbnb
- barrios de Airbnb
- reviews de Airbnb
- calendario diario de Airbnb
- renta disponible por persona
- licencias HUT

Los CSV fuente se almacenan de forma versionada en `landing_zone/raw`.

## Estructura De Entrega

- [landing_zone/landing.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone/landing.ipynb)
- [formatted_zone/formatted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted.ipynb)
- [trusted_zone/trusted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted.ipynb)
- [exploitation_zone/exploitation.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation.ipynb)
- [analysis_zone/analysis.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/analysis.ipynb)

Bases persistidas:

- [formatted_zone/formatted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted_zone.duckdb)
- [trusted_zone/trusted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted_zone.duckdb)
- [exploitation_zone/exploitation_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation_zone.duckdb)

## Landing Zone

La fase `landing` conserva los datos tal como llegan, sin transformaciones analiticas.

Que hace:

- localiza cada dataset
- crea una copia raw versionada por timestamp
- deja el inventario de la ingesta como output del notebook

Salida persistida:

- CSV en `landing_zone/raw`

## Formatted Zone

La fase `formatted` implementa la homogeneizacion sintactica usando Spark.

Que hace:

- lee los CSV desde `landing_zone/raw`
- normaliza nombres, tipos y columnas
- genera una tabla por dataset
- persiste el resultado en DuckDB

Base resultante:

- [formatted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted_zone.duckdb)

Tablas:

- `pics`
- `hotels`
- `weather`
- `airbnb_listings`
- `airbnb_neighbourhoods`
- `airbnb_reviews`
- `airbnb_calendar`
- `income_2022`
- `hut_licenses`

## Trusted Zone

La fase `trusted` implementa calidad y limpieza usando Spark.

Que hace:

- lee las tablas de `formatted_zone.duckdb`
- aplica reglas de calidad por dataset
- elimina duplicados
- valida coordenadas y campos obligatorios
- reconcilia listings con barrios/distritos
- filtra el calendario contra listings validos
- persiste las tablas limpias en DuckDB

Base resultante:

- [trusted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted_zone.duckdb)

Mantiene las mismas tablas que `formatted`, pero con calidad mejorada.

## Exploitation Zone

La fase `exploitation` integra semanticamente las tablas limpias de `trusted`.

Base final previa al analisis:

- [exploitation_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation_zone.duckdb)

Esta base no es una unica tabla gigante. Es una base con varias vistas analiticas, cada una con una granularidad distinta.

Tablas principales:

- `district_profile`
- `neighborhood_profile`
- `district_income_profile`
- `neighborhood_income_profile`
- `district_hut_profile`
- `neighborhood_hut_profile`
- `weather_daily`
- `district_day_features`
- `airbnb_listing_enriched`
- `airbnb_zone_features`
- `airbnb_zone_day_features`

Uso de las tablas:

- `airbnb_zone_features`: clustering por zona
- `airbnb_zone_day_features`: prediccion temporal de `booked_rate`
- perfiles de distrito y barrio: contexto territorial, turistico, renta y HUT
- `weather_daily`: contexto meteorologico diario

## Analysis Zone

La fase `analysis` consume exclusivamente `exploitation_zone.duckdb`.

Pipelines implementadas:

- visualizacion descriptiva
- clustering de zonas Airbnb
- prediccion de `booked_rate`

Los resultados se conservan como output del notebook, no como archivos externos.

## Estado Final

El proyecto queda alineado con el enunciado:

- data collector y landing raw
- formatted zone con Spark
- trusted zone con Spark
- exploitation zone como repositorio integrado para analisis
- al menos dos pipelines analiticas
- persistencia en DuckDB
- entrega en notebooks ejecutables y revisables

Nota: las fuentes `income_2022` y `hut_licenses` ya estan integradas en la base de explotacion, aunque la estrategia analitica actual todavia no las usa como variables del clustering o de la prediccion.
