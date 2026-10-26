"""CARRIER FANG — Carrier metadata and provider-contact guidance"""

import phonenumbers
from phonenumbers import carrier
from rich.console import Console
from rich.table import Table

console = Console()

# Common provider support links / numbers (public info only)
CARRIER_CONTACTS = {
    "verizon": {"name": "Verizon", "support": "https://www.verizon.com/support/", "lost": "1-800-922-0204"},
    "t-mobile": {"name": "T-Mobile", "support": "https://www.t-mobile.com/support/", "lost": "1-800-937-8997"},
    "at&t": {"name": "AT&T", "support": "https://www.att.com/support/", "lost": "1-800-331-0500"},
    "sprint": {"name": "Sprint / T-Mobile", "support": "https://www.t-mobile.com/support/", "lost": "1-888-211-4727"},
    "vodafone": {"name": "Vodafone", "support": "https://www.vodafone.com/help", "lost": "Check local site"},
    "orange": {"name": "Orange", "support": "https://www.orange.com/en/support", "lost": "Check local site"},
    "jio": {"name": "Jio", "support": "https://www.jio.com/en-in/support", "lost": "198"},
    "airtel": {"name": "Airtel", "support": "https://www.airtel.in/support", "lost": "121"},
}


class CarrierFang:
    def run(self, raw: str) -> dict:
        result = {"module": "CARRIER FANG", "raw": raw}

        try:
            parsed = phonenumbers.parse(raw, None)
        except phonenumbers.NumberParseException as e:
            result["error"] = str(e)
            console.print(f"[red]Parse error:[/red] {e}")
            return result

        carrier_name = carrier.name_for_number(parsed, "en") or "Unknown / Ported"
        result["original_carrier"] = carrier_name
        result["note"] = (
            "Carrier shown is the original allocation (prefix-based). "
            "Number portability means the current carrier may differ. "
            "Contact the carrier directly for definitive info."
        )

        # Try to match known contact
        lower = carrier_name.lower()
        matched = None
        for key, info in CARRIER_CONTACTS.items():
            if key in lower:
                matched = info
                break
        result["provider_contact"] = matched or {
            "guidance": "Search '[carrier] lost phone support' or visit the official carrier website."
        }

        self._display(result)
        return result

    def _display(self, r: dict):
        table = Table(title="CARRIER FANG Results", border_style="yellow")
        table.add_column("Field", style="cyan")
        table.add_column("Value")
        table.add_row("Original Carrier", r.get("original_carrier", "N/A"))
        table.add_row("Note", r.get("note", ""))
        console.print(table)

        contact = r.get("provider_contact", {})
        if "name" in contact:
            console.print(f"\n[bold]Provider guidance:[/bold] {contact['name']}")
            console.print(f"  Support: {contact.get('support')}")
            console.print(f"  Lost/stolen line: {contact.get('lost')}")
        else:
            console.print(f"\n[bold]Guidance:[/bold] {contact.get('guidance')}")
