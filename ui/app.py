import streamlit as st
import pandas as pd
from pathlib import Path
from src.elogsum.preprocess import ensure_time, normalise_cols
from src.elogsum.anomalies import rolling_spike_flags
from src.elogsum.summarise import segment_summaries
from src.elogsum.report import write_markdown

st.title("Engineering Log Summariser")

uploader = st.file_uploader("Upload CSV/NDJSON/JSON", type=["csv","json","ndjson","jsonl"])
time_col = st.text_input("Time column", value="timestamp")
value_cols = st.text_input("Value columns (comma-separated)", value="temp,voltage")
chunk_seconds = st.number_input("Chunk seconds", value=300, step=60)

if uploader and st.button("Summarise"):
    suffix = Path(uploader.name).suffix
    if suffix == ".csv":
        df = pd.read_csv(uploader)
    else:
        df = pd.read_json(uploader, lines=True)
    df = ensure_time(df, time_col)
    vals = [c.strip() for c in value_cols.split(",")]
    df = normalise_cols(df, vals)
    df = rolling_spike_flags(df, vals)
    summaries = segment_summaries(df, time_col, vals, int(chunk_seconds))
    out_dir = Path("artifacts/ui_run")
    write_markdown(summaries, out_dir)
    st.success("Done. See artifacts/ui_run/report.html")
    st.dataframe(df.head())
