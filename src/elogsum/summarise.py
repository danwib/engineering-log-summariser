import pandas as pd
from .anomalies import rolling_spike_flags, segment_by_time
from .prompts import SYSTEM_PROMPT, user_prompt
from .llm import complete

def segment_summaries(df: pd.DataFrame, time_col: str, value_cols: list[str], chunk_seconds: int):
    df_seg = df.copy()
    df_seg["seg_id"] = segment_by_time(df_seg, time_col, chunk_seconds)
    all_summaries = []
    for seg_id, seg in df_seg.groupby("seg_id"):
        stats = seg[value_cols].describe().to_string()
        if "any_spike" in seg.columns:
            spike_rate = seg["any_spike"].mean()
            stats += f"\nspike_rate={spike_rate:.3f}"
        meta = {"seg_id": int(seg_id),
                "start": seg[time_col].min().isoformat(),
                "end": seg[time_col].max().isoformat(),
                "rows": len(seg)}
        summary = complete(SYSTEM_PROMPT, user_prompt(meta, stats))
        all_summaries.append((meta, summary))
    return all_summaries
