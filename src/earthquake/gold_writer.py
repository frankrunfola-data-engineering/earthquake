from earthquake.io_utils import get_country_code
import pandas as pd
from earthquake.validate_path  import  validate_path

def gold_write(df, gold_path):
    """
    Enrich a Silver dataframe into Gold (country_code + sig_class) and write to CSV.
    Expects columns: latitude, longitude, sig
    """
    print("\n  gold_write()")
    validate_path(gold_path)
    # --- Enrichment: country code (uses your existing get_country_code function) ---
    country_codes = []
    for lat, lon in zip(df["latitude"], df["longitude"]):
        country_codes.append(get_country_code(lat, lon))

    df["country_code"] = country_codes

    # --- Enrichment: significance class ---
    # Bucket numeric `sig` (significance) score into human-friendly categories.
    # Bins are ranges:
    #   (-inf, 100]   -> "Low"
    #   (100, 500]    -> "Moderate"
    #   (500, inf]    -> "High"
    sig_bins = [-float("inf"), 100, 500, float("inf")]
    
    # Labels line up with the bin intervals above (must be exactly 1 fewer than number of bin edges)
    sig_labels = ["Low", "Moderate", "High"]

    # Create a new categorical column `sig_class` based on which bin each `sig` value falls into
    df["sig_class"] = pd.cut(df["sig"], bins=sig_bins,labels=sig_labels)

    # --- Write Gold output ---
    print(f"    ...write to {gold_path}")
    df.to_csv(gold_path, index=False)

    print("\n")
    
    return gold_path
