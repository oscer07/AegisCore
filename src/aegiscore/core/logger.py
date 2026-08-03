import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """Sets up a rich-formatted logger for the application."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console, show_path=False)]
    )
    return logging.getLogger("aegiscore")

logger = setup_logger()

def print_banner():
    """Prints the AegisCore application banner."""
    banner = r"""
    ___               _      ______               
   /   |  ___  ____ _(_)____/ ____/___  ________  
  / /| | / _ \/ __ `/ / ___/ /   / __ \/ ___/ _ \ 
 / ___ |/  __/ /_/ / (__  ) /___/ /_/ / /  /  __/ 
/_/  |_|\___/\__, /_/____/\____/\____/_/   \___/  
            /____/                                
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("[dim]Advanced Cybersecurity Toolkit - Defensive Auditing & Reconnaissance[/dim]\n")
