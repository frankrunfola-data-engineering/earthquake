# src/earthquake/enrich/gold.py
from __future__ import annotations

import pandas as pd


def silver_to_gold_df(silver_df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple daily rollup. This is your "gold" dataset.
    """
    if silver_df.empty:
        return pd.DataFrame(
            columns=["event_date", "quake_count", "max_magnitude", "avg_magnitude", "min_magnitude"]
        )

    gold = (
        silver_df.groupby("event_date", dropna=False)
        .agg(
            quake_count=("event_id", "count"),
            max_magnitude=("magnitude", "max"),
            avg_magnitude=("magnitude", "mean"),
            min_magnitude=("magnitude", "min"),
        )
        .reset_index()
        .sort_values("event_date", na_position="last")
    )
    return gold
