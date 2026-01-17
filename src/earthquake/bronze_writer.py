
import json
from pathlib import Path
from typing import Any

def bronze_write(raw: Any, bronze_path: str) :
    """
    Write raw JSON-serializable data to the Bronze layer as:
        {bronze_adls}/{start_date}_earthquake_data.json
    Args:
        rawData: JSON-serializable object (e.g., list/dict) to write.
        bronze_adls (str): Base folder path for bronze (local path or mounted ADLS path).
        start_date (str): Date string used in filename (e.g., "2026-01-16").
    Returns:
        bronze_path (str): Full file path written to.
    """
    print("\n  bronze_write()")

    # Write JSON to the file
    with open(bronze_path, 'w',encoding="utf-8") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
