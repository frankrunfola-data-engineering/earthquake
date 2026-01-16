""" 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File:    run_all.py
Author:  Frank Runfola
Date:    11/1/2025
-------------------------------------------------------------------------------
Description:
  One-command runner for the tiny Medallion pipeline.
  This is OPTIONAL — you can run the notebooks instead.
  But scripts are nice for CI or quick demos.
-------------------------------------------------------------------------------
Run from the project root:
  cd "/c/Users/fr54938/Documents/DE/earthquake"
  python -m scripts.run_all
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1] #get repo folder (./earthquake)
sys.path.insert(0, str(PROJECT_ROOT)) # Add repo folder to Python's import search path

from datetime import date, timedelta
from earthquake.paths import (ensure_medallion_dirs,get_bronze_path,get_silver_path,get_gold_path)
from earthquake.extract_raw import extract_raw
from earthquake.bronze_writer import bronze_write
from earthquake.silver_writer import silver_write
from earthquake.gold_writer import gold_write

def main() -> None:

    start_date = (date.today() - timedelta(1)).isoformat()
    end_date = date.today().isoformat()

    ensure_medallion_dirs()

    bronze_path = get_bronze_path(start_date)
    silver_path = get_silver_path(start_date)
    gold_path   = get_gold_path(start_date)

    raw = extract_raw(start_date, end_date)
    bronze_path = bronze_write(raw, bronze_path)
    df = silver_write(bronze_path, silver_path)
    gold_write(df,gold_path)

if __name__ == "__main__":
    main()
