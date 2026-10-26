"""GHOST RESCUE — Android and iPhone recovery links, sound, lost mode, lock guidance"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


class GhostRescue:
    def run(self, raw: str) -> dict:
        result = {
            "module": "GHOST RESCUE",
            "raw": raw,
            "android": {
                "find_my_device": "https://www.google.com/android/find",
                "account": "https://myaccount.google.com/",
                "steps": [
                    "1. Open https://www.google.com/android/find in any browser",
                    "2. Sign in with the Google account linked to the lost phone",
                    "3. Select the device → Play sound / Secure device / Erase device",
                    "4. If lost: enable Lock and display a message with callback number"
                ]
            },
            "iphone": {
                "find_my": "https://www.icloud.com/find",
                "account": "https://appleid.apple.com/",
                "steps": [
                    "1. Open https://www.icloud.com/find in any browser",
                    "2. Sign in with the Apple ID linked to the device",
                    "3. Select the device → Play Sound / Lost Mode / Erase iPhone",
                    "4. Lost Mode locks the device and can display a custom message"
                ]
            },
            "general": [
                "Change passwords for the Google/Apple account immediately",
                "Contact carrier to suspend SIM if theft is suspected",
                "File a police report and provide IMEI if available",
                "Do not pay ransom demands — use official recovery tools only"
            ]
        }

        self._display(result)
        return result

    def _display(self, r: dict):
        console.print(Panel("[bold green]ANDROID — Find My Device[/bold green]", border_style="green"))
        console.print(f"Official link: {r['android']['find_my_device']}")
        for step in r["android"]["steps"]:
            console.print(f"  {step}")

        console.print(Panel("[bold cyan]IPHONE — Find My[/bold cyan]", border_style="cyan"))
        console.print(f"Official link: {r['iphone']['find_my']}")
        for step in r["iphone"]["steps"]:
            console.print(f"  {step}")

        console.print(Panel("[bold yellow]General Recovery Guidance[/bold yellow]", border_style="yellow"))
        for item in r["general"]:
            console.print(f"  • {item}")
