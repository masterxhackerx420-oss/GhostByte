"""GEO ECHO — Country, numbering region, approximate geographic clues"""

import phonenumbers
from phonenumbers import geocoder, timezone, region_code_for_number
from rich.console import Console
from rich.table import Table

console = Console()


class GeoEcho:
    def run(self, raw: str) -> dict:
        result = {"module": "GEO ECHO", "raw": raw}

        try:
            parsed = phonenumbers.parse(raw, None)
        except phonenumbers.NumberParseException as e:
            result["error"] = str(e)
            console.print(f"[red]Parse error:[/red] {e}")
            return result

        result["country_code"] = parsed.country_code
        result["region_code"] = region_code_for_number(parsed)
        result["country_name"] = geocoder.description_for_number(parsed, "en") or "Unknown"
        result["timezones"] = list(timezone.time_zones_for_number(parsed)) or ["Unknown"]

        # Approximate geographic clue (city/region level only — never precise coordinates)
        result["approx_location"] = result["country_name"]
        result["note"] = "Approximate numbering-region only. Not a live location. No coordinates invented."

        self._display(result)
        return result

    def _display(self, r: dict):
        table = Table(title="GEO ECHO Results", border_style="blue")
        table.add_column("Field", style="cyan")
        table.add_column("Value")
        for k in ["country_code", "region_code", "country_name", "timezones", "approx_location", "note"]:
            if k in r:
                val = ", ".join(r[k]) if isinstance(r[k], list) else str(r[k])
                table.add_row(k.replace("_", " ").title(), val)
        console.print(table)
