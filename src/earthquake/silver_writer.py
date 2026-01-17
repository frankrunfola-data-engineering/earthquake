import json
from pathlib import Path

import pandas as pd
from earthquake.validate_path import validate_path


def silver_write(bronze_path, silver_path):
    print("\n  silver_write()")
    validate_path(bronze_path)

    # --- Read Bronze JSON ---
    with open(bronze_path, "r", encoding="utf-8") as f:
        raw_features = json.load(f)
    print(f"    ...read from {bronze_path}")

    # --- Normalize features (flatten nested JSON) ---
    df_raw = pd.json_normalize(raw_features)

    # --- Unpack GeoJSON coordinates: [lon, lat, depth] ---
    # USGS stores coordinates as a single list per event, not a list of records.
    coords = df_raw["geometry.coordinates"].apply(pd.Series)
    coords.columns = ["longitude", "latitude", "elevation"]

    # --- Build Silver dataframe (keep only what you need) ---
    time_ms = df_raw["properties.time"] if "properties.time" in df_raw.columns else pd.Series([pd.NA] * len(df_raw))

    df = pd.DataFrame({
        "id": df_raw.get("id"),
        "longitude": coords["longitude"],
        "latitude": coords["latitude"],
        "elevation": coords["elevation"],
        "time": pd.to_datetime(time_ms, unit="ms", errors="coerce"),
        "mag": df_raw.get("properties.mag"),
        "place": df_raw.get("properties.place"),
        "sig": df_raw.get("properties.sig"),
    })

    # --- Basic cleanup ---
    df["longitude"] = df["longitude"].fillna(0)
    df["latitude"] = df["latitude"].fillna(0)

    # --- Write Silver CSV ---
    print(f"    ...save to {silver_path}")
    df.to_csv(silver_path, index=False)

    return df
