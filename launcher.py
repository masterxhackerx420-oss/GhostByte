"""
GhostByte — Phone Recovery & OSINT Toolkit
Standalone launcher. Does not touch existing GlitchByte tools.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Ensure modules can be imported
sys.path.insert(0, str(Path(__file__).parent))

from modules.number_hunt import NumberHunt
from modules.geo_echo import GeoEcho
from modules.carrier_fang import CarrierFang
from modules.ghost_rescue import GhostRescue
from modules.recovery_shield import RecoveryShield
from modules.evidence_vault import EvidenceVault

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold cyan]GHOSTBYTE[/bold cyan]\n"
        "[dim]Phone Recovery & OSINT Toolkit[/dim]\n"
        "[yellow]Standalone • Repository-ready • No GlitchByte modifications[/yellow]",
        border_style="cyan"
    ))


def main():
    banner()
    vault = EvidenceVault()

    while True:
        table = Table(title="Modules", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=4)
        table.add_column("Module", style="green")
        table.add_column("Description")

        table.add_row("1", "NUMBER HUNT", "Format, validate, public-web research")
        table.add_row("2", "GEO ECHO", "Country, region, geographic clues")
        table.add_row("3", "CARRIER FANG", "Carrier metadata & provider contacts")
        table.add_row("4", "GHOST RESCUE", "Android/iPhone recovery links & guidance")
        table.add_row("5", "RECOVERY SHIELD", "IMEI checklist, SIM suspension, account protection")
        table.add_row("6", "EVIDENCE VAULT", "View / export saved reports")
        table.add_row("0", "EXIT", "Quit")

        console.print(table)
        choice = Prompt.ask("\nSelect module", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")

        if choice == "0":
            console.print("[bold green]GhostByte offline.[/bold green]")
            break

        number = Prompt.ask("Enter phone number (with country code, e.g. +1...)").strip()
        if not number:
            console.print("[red]No number provided.[/red]")
            continue

        report_data = {"input": number}

        if choice == "1":
            report_data.update(NumberHunt().run(number))
        elif choice == "2":
            report_data.update(GeoEcho().run(number))
        elif choice == "3":
            report_data.update(CarrierFang().run(number))
        elif choice == "4":
            report_data.update(GhostRescue().run(number))
        elif choice == "5":
            report_data.update(RecoveryShield().run(number))
        elif choice == "6":
            vault.list_reports()
            continue

        # Auto-save every scan
        vault.save(report_data)
        console.print("\n[dim]Report auto-saved to Evidence Vault.[/dim]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Interrupted.[/bold yellow]")
        sys.exit(0)
