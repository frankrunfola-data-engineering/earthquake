from __future__ import annotations

import pandas as pd

from earthquake.enrich.gold import add_sig_class


def test_sig_class_binning():
    df = pd.DataFrame({"sig": [0, 100, 101, 500, 501]})
    out = add_sig_class(df, low=100.0, high=500.0)

    assert out.loc[0, "sig_class"] == "Low"
    assert out.loc[1, "sig_class"] == "Low"
    assert out.loc[2, "sig_class"] == "Moderate"
    assert out.loc[3, "sig_class"] == "Moderate"
    assert out.loc[4, "sig_class"] == "High"
