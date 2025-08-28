import pandas as pd
import numpy as np

def rolling_spike_flags(df: pd.DataFrame, cols: list[str], window: int = 51, z=3.0) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        rmean = out[c].rolling(window, min_periods=5, center=True).mean()
        rstd  = out[c].rolling(window, min_periods=5, center=True).std().fillna(1.0)
        out[f"{c}_spike"] = (np.abs(out[c] - rmean) > z * rstd).astype(int)
    out["any_spike"] = out.filter(regex="_spike$").max(axis=1)
    return out

def segment_by_time(df: pd.DataFrame, time_col: str, seconds: int):
    ts = df[time_col].astype("int64") // 10**9
    return (ts - ts.min()) // seconds  # simple bucket id
