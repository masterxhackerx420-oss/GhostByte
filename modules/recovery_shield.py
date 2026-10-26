"""RECOVERY SHIELD — IMEI checklist, SIM suspension, account-protection guidance"""

from rich.console import Console
from rich.panel import Panel

console = Console()


class RecoveryShield:
    def run(self, raw: str) -> dict:
        result = {
            "module": "RECOVERY SHIELD",
            "raw": raw,
            "imei_checklist": [
                "Dial *#06# on the device (if accessible) to display IMEI",
                "Or check original box / receipt / Settings → About",
                "Verify IMEI at https://www.imei.info/ or https://devicecheck.gsma.com/",
                "Confirm it matches the claimed model (TAC prefix check)",
                "Report stolen IMEI to carrier + police so it can be blacklisted"
            ],
            "sim_suspension": [
                "Call carrier immediately and request SIM suspension / replacement",
                "Ask them to block the IMEI on their network (EIR blacklist)",
                "Request a new SIM with the same number if ownership is proven",
                "Monitor account for unauthorized charges"
            ],
            "account_protection": [
                "Change Google / Apple ID password from another device",
                "Enable 2FA / hardware key if not already on",
                "Review recent account activity and signed-in devices",
                "Revoke sessions and app passwords",
                "Update recovery email and phone number"
            ],
            "useful_links": {
                "GSMA Device Check": "https://devicecheck.gsma.com/",
                "IMEI.info": "https://www.imei.info/",
                "Google Account Security": "https://myaccount.google.com/security",
                "Apple ID Security": "https://appleid.apple.com/"
            }
        }

        self._display(result)
        return result

    def _display(self, r: dict):
        console.print(Panel("[bold red]IMEI Checklist[/bold red]", border_style="red"))
        for item in r["imei_checklist"]:
            console.print(f"  • {item}")

        console.print(Panel("[bold orange1]SIM Suspension Guidance[/bold orange1]", border_style="orange1"))
        for item in r["sim_suspension"]:
            console.print(f"  • {item}")

        console.print(Panel("[bold magenta]Account Protection[/bold magenta]", border_style="magenta"))
        for item in r["account_protection"]:
            console.print(f"  • {item}")

        console.print("\n[bold]Useful official links:[/bold]")
        for name, url in r["useful_links"].items():
            console.print(f"  • {name}: {url}")
