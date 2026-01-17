from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from earthquake.transform.silver import features_to_silver_df


def test_features_to_silver_df_basic_columns():
    features = [
        {
            "id": "abc123",
            "geometry": {"coordinates": [-118.5, 34.2, 10.0]},
            "properties": {
                "time": 1730000000000,
                "mag": 4.2,
                "place": "Somewhere",
                "sig": 250,
            },
        }
    ]

    df = features_to_silver_df(features)
    assert list(df.columns) == ["id", "longitude", "latitude", "elevation", "time", "mag", "place", "sig"]
    assert len(df) == 1
    assert df.loc[0, "id"] == "abc123"
    assert df.loc[0, "longitude"] == -118.5
    assert df.loc[0, "latitude"] == 34.2
    assert df.loc[0, "elevation"] == 10.0
    assert pd.notna(df.loc[0, "time"])


def test_features_to_silver_df_empty_returns_empty_df():
    df = features_to_silver_df([])
    assert len(df) == 0
