"""NUMBER HUNT — Formatting, validation, optional public-web research"""

import phonenumbers
from phonenumbers import PhoneNumberFormat, is_valid_number, is_possible_number, number_type
from urllib.parse import quote_plus
from rich.console import Console
from rich.table import Table

console = Console()


class NumberHunt:
    def run(self, raw: str) -> dict:
        result = {"module": "NUMBER HUNT", "raw": raw}

        try:
            parsed = phonenumbers.parse(raw, None)
        except phonenumbers.NumberParseException as e:
            result["error"] = str(e)
            console.print(f"[red]Parse error:[/red] {e}")
            return result

        result["e164"] = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        result["international"] = phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
        result["national"] = phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL)
        result["is_valid"] = is_valid_number(parsed)
        result["is_possible"] = is_possible_number(parsed)

        ntype = number_type(parsed)
        type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed or Mobile",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
        }
        result["line_type"] = type_map.get(ntype, "Unknown")

        # Public-web research dorks (user must open them)
        q = quote_plus(result["e164"])
        result["web_dorks"] = {
            "google": f"https://www.google.com/search?q={q}",
            "duckduckgo": f"https://duckduckgo.com/?q={q}",
            "truecaller_search": f"https://www.google.com/search?q=site:truecaller.com+{q}",
            "reddit": f"https://www.google.com/search?q=site:reddit.com+{q}",
            "pastebin": f"https://www.google.com/search?q=site:pastebin.com+{q}",
        }

        self._display(result)
        return result

    def _display(self, r: dict):
        table = Table(title="NUMBER HUNT Results", border_style="green")
        table.add_column("Field", style="cyan")
        table.add_column("Value")
        for k in ["e164", "international", "national", "is_valid", "is_possible", "line_type"]:
            if k in r:
                table.add_row(k.replace("_", " ").title(), str(r[k]))
        console.print(table)

        console.print("\n[bold]Public-web research links:[/bold]")
        for name, url in r.get("web_dorks", {}).items():
            console.print(f"  • {name}: {url}")
