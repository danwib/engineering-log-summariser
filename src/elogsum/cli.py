import argparse
from pathlib import Path
from .config import DEFAULT_TIME_COL
from .ingest import read_any
from .preprocess import ensure_time, normalise_cols
from .anomalies import rolling_spike_flags
from .summarise import segment_summaries
from .report import write_markdown

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--time-col", default=DEFAULT_TIME_COL)
    ap.add_argument("--value-cols", required=True, help="comma-separated")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--chunk-seconds", type=int, default=300)
    args = ap.parse_args()

    df = read_any(args.input)
    value_cols = [c.strip() for c in args.value_cols.split(",") if c.strip()]

    df = ensure_time(df, args.time_col)
    df = normalise_cols(df, value_cols)
    df = rolling_spike_flags(df, value_cols)

    summaries = segment_summaries(df, args.time_col, value_cols, args.chunk_seconds)
    write_markdown(summaries, Path(args.out_dir))

if __name__ == "__main__":
    main()
