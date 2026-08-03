import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# Define a professional cyber theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green",
    "highlight": "bold yellow"
})

console = Console(theme=custom_theme)

def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """Sets up a professional rich-formatted logger for the application."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console, show_path=False, markup=True)]
    )
    return logging.getLogger("aegiscore")

logger = setup_logger()

def print_banner():
    """Prints a highly professional AegisCore application banner."""
    banner_text = """
    █████╗ ███████╗ ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗
   ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
   ███████║█████╗  ██║  ███╗██║███████╗██║     ██║   ██║██████╔╝█████╗  
   ██╔══██║██╔══╝  ██║   ██║██║╚════██║██║     ██║   ██║██╔══██╗██╔══╝  
   ██║  ██║███████╗╚██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║███████╗
   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    """
    
    panel = Panel(
        Align.center(
            f"[bold cyan]{banner_text}[/bold cyan]\n"
            "[bold white]ADVANCED CYBERSECURITY FRAMEWORK[/bold white]\n"
            "[dim]v2.0.0 | Enterprise Edition[/dim]"
        ),
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(panel)
    console.print()
