SYSTEM_PROMPT = """You are an engineering test analyst.
Produce concise, actionable bullets using the data context provided.
Be specific about timestamps, magnitudes, and suspected causes.
Keep to <10 bullets and propose next steps only when justified."""

def user_prompt(segment_meta: dict, stats_text: str) -> str:
    return f"""Context:
- Segment: {segment_meta}
- Stats/Anomalies:
{stats_text}

Task:
Summarise key events and anomalies. Include exact times/values where relevant.
End with a 2-line 'Likely causes' and 'Next steps'."""
