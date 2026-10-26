"""EVIDENCE VAULT — Locally saved HTML, JSON, and text reports"""

import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


class EvidenceVault:
    def save(self, data: dict) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_num = "".join(c for c in data.get("input", "unknown") if c.isdigit())[:12]
        base = REPORTS_DIR / f"{ts}_{safe_num}"

        # JSON
        json_path = base.with_suffix(".json")
        json_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

        # TXT
        txt_path = base.with_suffix(".txt")
        txt_path.write_text(self._to_text(data), encoding="utf-8")

        # HTML
        html_path = base.with_suffix(".html")
        html_path.write_text(self._to_html(data), encoding="utf-8")

        console.print(f"[green]Saved:[/green] {json_path.name} | {txt_path.name} | {html_path.name}")
        return base

    def list_reports(self):
        files = sorted(REPORTS_DIR.glob("*.json"), reverse=True)
        if not files:
            console.print("[yellow]No reports yet.[/yellow]")
            return

        table = Table(title="Evidence Vault", border_style="cyan")
        table.add_column("Timestamp", style="cyan")
        table.add_column("File")
        for f in files[:20]:
            table.add_row(f.stem.split("_")[0], f.name)
        console.print(table)
        console.print(f"\nReports stored in: {REPORTS_DIR}")

    def _to_text(self, data: dict) -> str:
        lines = [f"GhostByte Report — {datetime.now().isoformat()}", "=" * 50]
        for k, v in data.items():
            if isinstance(v, dict):
                lines.append(f"\n[{k.upper()}]")
                for sk, sv in v.items():
                    lines.append(f"  {sk}: {sv}")
            elif isinstance(v, list):
                lines.append(f"\n[{k.upper()}]")
                for item in v:
                    lines.append(f"  • {item}")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)

    def _to_html(self, data: dict) -> str:
        body = "".join(
            f"<h2>{k}</h2><pre>{json.dumps(v, indent=2, default=str)}</pre>"
            for k, v in data.items()
        )
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>GhostByte Report</title>
<style>body{{font-family:system-ui;background:#111;color:#eee;padding:2rem}}
pre{{background:#222;padding:1rem;border-radius:8px;overflow:auto}}</style>
</head><body>
<h1>GhostByte Evidence Report</h1>
<p>Generated: {datetime.now().isoformat()}</p>
{body}
</body></html>"""
