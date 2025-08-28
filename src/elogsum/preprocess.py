import pandas as pd
import numpy as np

def normalise_cols(df: pd.DataFrame, value_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in value_cols:
        mu, sigma = out[c].mean(), out[c].std() or 1.0
        out[f"{c}_z"] = (out[c] - mu) / sigma
    return out

def ensure_time(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    out = df.copy()
    out[time_col] = pd.to_datetime(out[time_col], errors="coerce")
    out = out.dropna(subset=[time_col]).sort_values(time_col)
    return out
