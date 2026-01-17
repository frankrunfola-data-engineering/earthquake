""" 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File:    src/earthquake/pipeline.py
Author:  Frank Runfola
Date:    11/1/2025
-------------------------------------------------------------------------------
Description:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .extract.usgs import fetch_features
from .transform.silver import features_to_silver_df
from .enrich.gold import silver_to_gold_df
from .io.fs import write_json, write_csv
from .io.paths import MedallionPaths, build_paths


@dataclass(frozen=True)
class PipelineResult:
    run_date: date
    paths: MedallionPaths
    records_bronze: int
    records_silver: int
    records_gold: int


def _count_bronze(payload: Any) -> int:
    # USGS payload typically: {"features": [...]}
    if isinstance(payload, dict) and isinstance(payload.get("features"), list):
        return len(payload["features"])
    if isinstance(payload, list):
        return len(payload)
    return 0


def run_pipeline(*, config: PipelineConfig) -> PipelineResult:
    run_date = date.today()

    lookback = getattr(config, "lookback_days", 1) or 1
    end_date = run_date
    start_date = end_date - timedelta(days=int(lookback))

    # Paths (assumes your build_paths supports these args)
    output_dir = Path(getattr(config, "output_dir", "data"))
    paths = build_paths(output_dir=output_dir, run_date=run_date)

    # Bronze
    bronze = fetch_features(
        base_url=config.base_url,
        start_date=start_date,
        end_date=end_date,
    )
    paths.bronze_dir.mkdir(parents=True, exist_ok=True)
    write_json(bronze, paths.bronze_dir / "usgs_features.json")

    # Silver
    silver_df = features_to_silver_df(bronze, run_date=run_date)
    paths.silver_dir.mkdir(parents=True, exist_ok=True)
    write_csv(silver_df, paths.silver_dir / "earthquakes_silver.csv")

    # Gold
    gold_df = silver_to_gold_df(silver_df)
    paths.gold_dir.mkdir(parents=True, exist_ok=True)
    write_csv(gold_df, paths.gold_dir / "earthquakes_gold.csv")

    return PipelineResult(
        run_date=run_date,
        paths=paths,
        records_bronze=_count_bronze(bronze),
        records_silver=len(silver_df),
        records_gold=len(gold_df),
    )
