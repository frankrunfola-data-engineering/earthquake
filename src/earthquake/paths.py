# src/earthquake_pipeline/paths.py
from pathlib import Path

# Base output folders (local dev defaults)
# Override these with env vars later if you want, but keep defaults here.
BRONZE_BASE = Path("data/bronze")
SILVER_BASE = Path("data/silver")
GOLD_BASE   = Path("data/gold")
QUARANTINE_BASE = Path("data/quarantine")

def create_directories() -> None: #Create output folders if missing.
    print("\n  create_directories")
    for dir in [BRONZE_BASE, SILVER_BASE, GOLD_BASE, QUARANTINE_BASE]:
        print(f"    mkdir '{dir}'")
        dir.mkdir(parents=True, exist_ok=True)

def get_bronze_path(day: str) -> str: # Example: data/bronze/2026-01-16_earthquake_data.json    
    path = BRONZE_BASE / f"{day}_earthquake_data.json"
    print(f"\n  get path: {path}")
    return str(path)

def get_silver_path(day: str) -> str: # Example: data/silver/2026-01-16/earthquake_events_silver.csv 
    path = SILVER_BASE / day
    print(f"  create folder: {path}")
    path.mkdir(parents=True, exist_ok=True)
    path = path / "earthquake_events_silver.csv"
    return str(path)

def get_gold_path(day: str) -> str: # Example: data/gold/2026-01-16/earthquake_events_gold.csv    
    path = GOLD_BASE / day
    print(f"  create folder: {path}")
    path.mkdir(parents=True, exist_ok=True)
    path = path / "earthquake_events_gold.csv"
    return str(path)