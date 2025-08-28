from pathlib import Path
import markdown

def write_markdown(summaries, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# Engineering Log Summary\n"]
    for meta, text in summaries:
        lines += [f"## Segment {meta['seg_id']} ({meta['start']} → {meta['end']}, rows={meta['rows']})", "", text, ""]
    md = "\n".join(lines)
    (out_dir / "report.md").write_text(md, encoding="utf-8")
    html = markdown.markdown(md, extensions=["tables"])
    (out_dir / "report.html").write_text(html, encoding="utf-8")
