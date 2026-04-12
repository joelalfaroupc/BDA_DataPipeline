

import argparse
import io
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

DATASET_ID = "habitatges-us-turistic"
CKAN_BASE = "https://opendata-ajuntament.barcelona.cat/data/api/3/action"
OUTPUT_CSV = "hut_comunicacio_opendata.csv"
RETRY_INTERVAL_SECONDS = 34 * 3600  # 1 dia


def current_quarter() -> tuple[int, int]:
    now = datetime.now(timezone.utc)
    return now.year, (now.month - 1) // 3 + 1


def fetch_zip_url(year: int, quarter: int) -> str | None:
    """Retorna la URL del ZIP del trimestre indicat, o None si no existeix encara."""
    resp = requests.get(f"{CKAN_BASE}/package_show", params={"id": DATASET_ID}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN API error: {data.get('error')}")

    prefix = f"{year}_{quarter}T_hut_comunicacio"
    for resource in data["result"]["resources"]:
        if (resource.get("format") or "").upper() != "ZIP":
            continue
        name = resource.get("name", "") or ""
        url = resource.get("url", "") or ""
        if prefix.lower() in (name + url).lower():
            return resource["url"]
    return None


def download_and_extract(url: str, dest_dir: Path) -> Path:
    """Descarrega el ZIP i extreu el CSV, retornant el Path final."""
    print(f"  → Descarregant: {url}")
    resp = requests.get(url, timeout=120, stream=True)
    resp.raise_for_status()

    raw = io.BytesIO()
    for chunk in resp.iter_content(chunk_size=65_536):
        raw.write(chunk)
    print(f"  → Descarregat: {raw.tell() / 1024:.1f} KB")

    raw.seek(0)
    with zipfile.ZipFile(raw) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise RuntimeError("El ZIP no conté cap fitxer CSV.")
        zf.extract(csv_names[0], dest_dir)
        extracted = dest_dir / csv_names[0]

    final = dest_dir / OUTPUT_CSV
    extracted.replace(final)
    print(f"  → CSV llest: {final}")
    return final


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=None)
    parser.add_argument("--quarter", type=int, choices=[1, 2, 3, 4], default=None)
    parser.add_argument("--dest", type=str, default=".")
    args = parser.parse_args()

    dest_dir = Path(args.dest).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    year, quarter = (args.year, args.quarter) if args.year and args.quarter else current_quarter()
    print(f"[collect_hut] Buscant: {year} T{quarter}")

    while True:
        url = fetch_zip_url(year, quarter)
        if url:
            download_and_extract(url, dest_dir)
            print("[collect_hut] ✓ Completat.")
            break
        print(f"[collect_hut] Encara no publicat. Reintentant en 1 dia...")
        time.sleep(RETRY_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()