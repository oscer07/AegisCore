import typer
from aegiscore.core.logger import print_banner, logger

from aegiscore.modules.recon import recon_app
from aegiscore.modules.audit import audit_app
from aegiscore.modules.web import web_app
from aegiscore.modules.crypto import crypto_app
from aegiscore.modules.automation import automation_app
from aegiscore.modules.report import report_app

app = typer.Typer(
    name="aegis",
    help="AegisCore - Advanced Cybersecurity Toolkit",
    no_args_is_help=True,
)

# Register sub-modules
app.add_typer(recon_app, name="recon", help="Network & Reconnaissance Tools")
app.add_typer(audit_app, name="audit", help="Defensive & Auditing Tools")
app.add_typer(web_app, name="web", help="Web Application Security Tools")
app.add_typer(crypto_app, name="crypto", help="Cryptography & Password Tools")
app.add_typer(automation_app, name="automation", help="Automation & Workflow Tools")
app.add_typer(report_app, name="report", help="Reporting & Export Tools")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    AegisCore - Advanced Cybersecurity Toolkit
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        logger.info("Welcome to AegisCore. Run 'aegis --help' to see available modules.")

if __name__ == "__main__":
    app()
