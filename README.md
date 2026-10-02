# Barcelona Tourism Data Pipeline

**From heterogeneous urban data to an integrated analytical database and temporal Airbnb analysis.**

University team project for Large-Scale Data Engineering for AI. The pipeline combines tourism, accommodation, weather and socioeconomic data for Barcelona, using five data zones to make ingestion, cleaning, integration and analysis explicit.

## What the project delivers

- Nine source datasets covering points of interest, hotels, weather, Airbnb listings, neighborhoods, reviews and availability calendars, neighborhood income and tourist accommodation licenses.
- Persistent DuckDB databases for formatted, trusted and exploitation data.
- District and neighborhood profiles, enriched listings and daily analytical features.
- Exploratory segmentation and predictive experiments with chronological train/test splits, baselines and error metrics.

The main analytical target is a **calendar non-availability rate**. The code names it `booked_rate`, but unavailable nights can also be owner-blocked: this is an availability proxy, not a count of confirmed bookings.

## How it works

```text
Source CSVs → Landing → Formatted → Trusted → Exploitation → Analysis
                        PySpark transformations / DuckDB persistence
```

| Zone | Implementation | Purpose |
| --- | --- | --- |
| Landing | [landing notebook](landing_zone/landing.ipynb) | Collect and retain source snapshots. |
| Formatted | [formatted notebook](formatted_zone/formatted.ipynb) | Standardize names, types and schemas. |
| Trusted | [trusted notebook](trusted_zone/trusted.ipynb) | Deduplicate, check required fields and coordinates, reconcile territorial identifiers and validate calendar/listing relationships. |
| Exploitation | [exploitation notebook](exploitation_zone/exploitation.ipynb) | Join sources into reusable profiles and daily feature tables. |
| Analysis | [updated analysis](analysis_zone/analysis_updated.ipynb) | Explore neighborhood groups and compare predictive models with a temporal holdout. |

The analytical notebook implements KMeans, linear regression trained by gradient descent and KNN. Feature variants compare calendar, weather, price and combined information. MAE, RMSE and R² are reported against a baseline.

Income and accommodation-license data enrich the integrated database; they are not all used as features in the current prediction experiments.

## Results and evidence

The updated notebook retains experiment outputs. One recorded configuration uses 16,054 training observations and 4,044 test observations, split by date. KNN with 15 neighbors and the combined feature set reports **RMSE 0.0713**, compared with **0.1159** for the baseline on the same split.

These are archived notebook results, not a fresh execution or a general performance guarantee. They predict the availability proxy and do not establish causal effects of weather, price or tourism pressure.

Explore the [extended project summary](RESUMEN_PROYECTO.md) and the [integrated DuckDB database](exploitation_zone/exploitation_zone.duckdb). The [earlier analysis notebook](analysis_zone/analysis.ipynb) is retained for context.

## Run the notebooks

Use Python 3.11 or later, Java compatible with the installed PySpark version, and an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install jupyterlab pyspark duckdb matplotlib
jupyter lab
```

On Windows, activate with `.venv\Scripts\activate`. Dependencies are currently unpinned.

Run the notebooks in the zone order above. Several notebooks resolve paths from the kernel's working directory, which must be the repository root. If the notebook opens with its own folder as the working directory, run this cell before the existing setup cells:

```python
from pathlib import Path
import os

root = next(
    (p for p in (Path.cwd(), *Path.cwd().parents)
     if (p / "landing_zone").is_dir() and (p / "trusted_zone").is_dir()),
    None,
)
if root is None:
    raise RuntimeError("Open the notebook inside BDA_DataPipeline")
os.chdir(root)
```

Versioned source snapshots and databases allow inspection without recollecting every source. Rerunning ingestion can change snapshot dates and downstream results.

## Project context

This repository preserves the university team's implementation and commit history from [K4NG14/BDA_DataPipeline](https://github.com/K4NG14/BDA_DataPipeline). This portfolio edition improves the documentation and navigation.
