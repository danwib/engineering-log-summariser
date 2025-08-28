import pandas as pd
from pathlib import Path

def read_any(path: str | Path) -> pd.DataFrame:
    p = Path(path)
    if p.suffix.lower() in {".csv"}:
        return pd.read_csv(p)
    if p.suffix.lower() in {".json"}:
        return pd.read_json(p, lines=True)
    if p.suffix.lower() in {".ndjson", ".jsonl"}:
        return pd.read_json(p, lines=True)
    raise ValueError(f"Unsupported file type: {p.suffix}")
