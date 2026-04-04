# Resumen Del Proyecto

## Objetivo

El proyecto implementa una pipeline end-to-end de Data Engineering y Data Analysis sobre Barcelona para estudiar el mercado de Airbnb y su relacion con variables territoriales, turisticas y meteorologicas.

La arquitectura sigue las fases del enunciado:

- `Landing Zone`
- `Formatted Zone`
- `Trusted Zone`
- `Exploitation Zone`
- `Analysis Zone`

La implementacion final esta organizada en notebooks autocontenidos por fase, con outputs guardados dentro de cada `.ipynb` y con artefactos persistidos por zona.

## Fuentes De Datos

Los datasets integrados son:

- `opendatabcn_pics-csv.csv`
- `opendatabcn_allotjament_hotels-csv.csv`
- `dataset_prat_temps_2025-26.csv`
- `listings.csv`
- `neighbourhoods.csv`
- `reviews_airbnb.csv`
- `calendar.csv`
- `2022_renda_disponible_llars_per_persona.csv`
- `hut_comunicacio_opendata.csv`

Estas fuentes cubren:

- puntos de interes y equipamientos
- hoteles
- meteorologia diaria
- oferta Airbnb
- disponibilidad diaria de Airbnb
- relacion barrio-distrito
- reviews agregadas
- renta por persona
- licencias HUT

## Estructura Final Del Proyecto

- [landing_zone](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone)
  Notebook: [landing.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone/landing.ipynb)
- [formatted_zone](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone)
  Notebook: [formatted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted.ipynb)
- [trusted_zone](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone)
  Notebook: [trusted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted.ipynb)
- [exploitation_zone](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone)
  Notebook: [exploitation.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation.ipynb)
- [analysis_zone](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone)
  Notebook: [analysis.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/analysis.ipynb)

Artefactos principales:

- [landing_zone/reports/landing_manifest.json](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone/reports/landing_manifest.json)
- [formatted_zone/formatted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted_zone.duckdb)
- [trusted_zone/trusted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted_zone.duckdb)
- [exploitation_zone/exploitation_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation_zone.duckdb)
- [analysis_zone/reports/analysis_summary.json](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/reports/analysis_summary.json)

## Requisitos Tecnicos

- Python 3
- Java 21
- PySpark
- DuckDB
- Jupyter Notebook
- Matplotlib

Spark se usa en `formatted` y `trusted`, mientras que DuckDB se usa como almacenamiento persistente de las capas relacionales.

## Flujo De Ejecucion

### 1. Landing Zone

El notebook [landing.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone/landing.ipynb) copia los datasets raw a una estructura de ingesta versionada y genera un manifiesto con la ultima ejecucion.

Salida principal:

- copias raw en `landing_zone/raw`
- manifiesto de ejecucion

Para mantener la entrega ligera y trazable, se conserva solo la ultima copia raw de cada dataset.

Ultima ejecucion registrada:

- `run_id`: `20260404T112053Z`

### 2. Formatted Zone

El notebook [formatted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted.ipynb) implementa la homogeneizacion sintactica con Spark.

Operaciones principales:

- lectura de CSV raw
- normalizacion de columnas y tipos
- transformaciones Spark DataFrame
- materializacion en DuckDB

Tablas generadas en [formatted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted_zone.duckdb):

- `pics`
- `hotels`
- `weather`
- `airbnb_listings`
- `airbnb_neighbourhoods`
- `airbnb_reviews`
- `airbnb_calendar`
- `income_2022`
- `hut_licenses`

Conteos actuales:

- `pics`: 1786
- `hotels`: 894
- `weather`: 41597
- `airbnb_listings`: 19410
- `airbnb_neighbourhoods`: 73
- `airbnb_reviews`: 14421
- `airbnb_calendar`: 7084654
- `income_2022`: 1068
- `hut_licenses`: 10730

### 3. Trusted Zone

El notebook [trusted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted.ipynb) implementa la evaluacion de calidad y la limpieza por dataset tambien con Spark.

Operaciones principales:

- validacion de claves y campos obligatorios
- filtrado de coordenadas invalidas
- eliminacion de duplicados
- reconciliacion de distrito-barrio
- limpieza del calendario contra listings validos

La base resultante es [trusted_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted_zone.duckdb) y conserva las mismas tablas que `formatted`.

Conteos validos actuales:

- `pics`: 878
- `hotels`: 446
- `weather`: 20967
- `airbnb_neighbourhoods`: 73
- `airbnb_reviews`: 14421
- `airbnb_listings`: 15276
- `airbnb_calendar`: 5575744
- `income_2022`: 1068
- `hut_licenses`: 10724

### 4. Exploitation Zone

El notebook [exploitation.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation.ipynb) integra semanticamente las tablas de `trusted` y crea las vistas analiticas.

La base final unificada previa al analisis es:

- [exploitation_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation_zone.duckdb)

Esta base no contiene una unica tabla gigante, sino varias tablas analiticas con distinta granularidad, lo que encaja con el enunciado.

Tablas generadas:

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

Granularidades:

- `listing`: `airbnb_listing_enriched`
- `zona`: `airbnb_zone_features`
- `zona-dia`: `airbnb_zone_day_features`
- `distrito`: perfiles de distrito
- `barrio`: perfiles de barrio
- `dia`: `weather_daily`
- `distrito-dia`: `district_day_features`

Conteos actuales:

- `district_profile`: 10
- `neighborhood_profile`: 74
- `district_income_profile`: 10
- `neighborhood_income_profile`: 73
- `district_hut_profile`: 10
- `neighborhood_hut_profile`: 65
- `weather_daily`: 290
- `district_day_features`: 2900
- `airbnb_listing_enriched`: 15276
- `airbnb_zone_features`: 71
- `airbnb_zone_day_features`: 25954

## Analisis Implementado

El notebook [analysis.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/analysis.ipynb) consume exclusivamente [exploitation_zone.duckdb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation_zone.duckdb).

### 1. Visualizacion

Se generan graficas descriptivas para explorar:

- zonas con mayor `avg_price`
- evolucion diaria de `temperature_avg`

Salidas:

- [analysis_zone/visualization/airbnb_avg_price_by_zone.png](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/visualization/airbnb_avg_price_by_zone.png)
- [analysis_zone/visualization/daily_temperature.png](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/visualization/daily_temperature.png)
- [analysis_zone/visualization/airbnb_zone_top10.csv](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/visualization/airbnb_zone_top10.csv)

### 2. Clustering

Se segmentan las zonas Airbnb usando `airbnb_zone_features`.

Variables principales:

- `avg_price`
- `median_price`
- `avg_rating`
- `avg_accommodates`
- `avg_bedrooms`
- `avg_availability_365`
- `entire_home_ratio`
- `private_room_ratio`
- `superhost_ratio`
- `instant_bookable_ratio`
- `avg_review_count`
- `neighborhood_tourism_asset_score`
- `district_tourism_asset_score`

Resultado actual:

- `55` zonas clusterizadas
- `k = 4`

Salidas:

- [analysis_zone/clustering/airbnb_zone_clusters.csv](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/clustering/airbnb_zone_clusters.csv)
- [analysis_zone/clustering/cluster_summary.json](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/clustering/cluster_summary.json)
- [analysis_zone/clustering/cluster_avg_price.png](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/clustering/cluster_avg_price.png)

### 3. Prediccion

Se implementa una pipeline de regresion sobre `airbnb_zone_day_features` para predecir `booked_rate`.

Target:

- `booked_rate`

Features usadas:

- `avg_calendar_price`
- `avg_minimum_nights`
- `listing_count`
- `neighborhood_tourism_asset_score`
- `district_tourism_asset_score`
- `temperature_avg`
- `humidity_avg`
- `radiation_avg`
- `wind_speed_avg`
- `rain_total`
- `month`
- `day_of_week`
- `is_weekend`

Modelos comparados:

- `baseline_mean`
- `linear_regression`
- `knn_regression_k_15`

Mejor modelo actual:

- `knn_regression_k_15`
- `RMSE = 0.068605`
- `MAE = 0.054031`
- `R2 = 0.567266`

Salidas:

- [analysis_zone/prediction/model_comparison.json](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/prediction/model_comparison.json)
- [analysis_zone/prediction/booked_rate_predictions.csv](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/prediction/booked_rate_predictions.csv)
- [analysis_zone/prediction/rmse_comparison.png](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/prediction/rmse_comparison.png)
- [analysis_zone/prediction/best_model_prediction_sample.png](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/prediction/best_model_prediction_sample.png)
- [analysis_zone/models/best_booked_rate_model.pkl](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/models/best_booked_rate_model.pkl)

## Estado De Entrega

La parte de Data Engineering previa al analisis queda alineada con el enunciado en estos puntos:

- `Landing` con ingesta raw persistida
- `Formatted` implementada con Spark
- `Trusted` implementada con Spark
- `Exploitation` como base unificada final para consumo analitico
- al menos dos pipelines analiticas
- persistencia de resultados, graficas y modelo

## Orden Recomendado De Revision

Para revisar el proyecto de forma rapida:

1. abrir [landing.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/landing_zone/landing.ipynb)
2. abrir [formatted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/formatted_zone/formatted.ipynb)
3. abrir [trusted.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/trusted_zone/trusted.ipynb)
4. abrir [exploitation.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/exploitation_zone/exploitation.ipynb)
5. abrir [analysis.ipynb](/Users/joelalfaro/Documents/UPC/Q6/BDA/PROYECTO/analysis_zone/analysis.ipynb)

## Nota Final

La estrategia analitica actual todavia no incorpora `income_2022` ni `hut_licenses` como features del clustering o de la prediccion. Estas dos fuentes ya estan integradas en la backbone de datos y quedan disponibles para una posible evolucion final del analisis.

Los notebooks quedan ejecutados y con outputs persistidos dentro de cada `.ipynb`, lo que facilita la revision visual durante la entrega.
