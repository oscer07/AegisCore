import typer
import os
import hashlib
import re
import json
from pathlib import Path
from aegiscore.core.logger import logger, console
from rich.table import Table

audit_app = typer.Typer(help="Defensive & Auditing Tools")

def hash_file(filepath: str) -> str:
    """Returns the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

@audit_app.command("fim-baseline")
def fim_baseline(
    directory: str = typer.Argument(..., help="Directory to baseline"),
    output: str = typer.Option("baseline.json", help="Output file for the baseline hashes")
):
    """
    Creates a File Integrity Monitor (FIM) baseline by hashing all files in a directory.
    """
    console.print(f"[*] Generating FIM baseline for {directory}")
    baseline = {}
    path = Path(directory)
    
    if not path.exists() or not path.is_dir():
        logger.error(f"[!] Directory {directory} does not exist.")
        raise typer.Exit(code=1)
        
    for file_path in path.rglob("*"):
        if file_path.is_file():
            try:
                baseline[str(file_path)] = hash_file(str(file_path))
            except Exception as e:
                logger.warning(f"[-] Could not hash {file_path}: {e}")
                
    with open(output, 'w') as f:
        json.dump(baseline, f, indent=4)
        
    logger.info(f"[green][+] Baseline generated and saved to {output} ({len(baseline)} files).[/green]")

@audit_app.command("fim-check")
def fim_check(
    directory: str = typer.Argument(..., help="Directory to check"),
    baseline_file: str = typer.Option("baseline.json", help="Baseline JSON file to compare against")
):
    """
    Checks a directory against a previously generated FIM baseline.
    """
    console.print(f"[*] Checking {directory} against baseline {baseline_file}")
    
    if not os.path.exists(baseline_file):
        logger.error(f"[!] Baseline file {baseline_file} not found.")
        raise typer.Exit(code=1)
        
    with open(baseline_file, 'r') as f:
        baseline = json.load(f)
        
    path = Path(directory)
    current_files = set()
    altered_files = []
    new_files = []
    
    for file_path in path.rglob("*"):
        if file_path.is_file():
            current_files.add(str(file_path))
            if str(file_path) in baseline:
                try:
                    current_hash = hash_file(str(file_path))
                    if current_hash != baseline[str(file_path)]:
                        altered_files.append(str(file_path))
                except Exception as e:
                    logger.warning(f"[-] Could not hash {file_path}: {e}")
            else:
                new_files.append(str(file_path))
                
    deleted_files = list(set(baseline.keys()) - current_files)
    
    # Display results
    table = Table(title="File Integrity Monitor Results")
    table.add_column("Status", justify="left")
    table.add_column("File", justify="left")
    
    for file in new_files:
        table.add_row("[yellow]NEW[/yellow]", file)
    for file in altered_files:
        table.add_row("[red]ALTERED[/red]", file)
    for file in deleted_files:
        table.add_row("[magenta]DELETED[/magenta]", file)
        
    if not (new_files or altered_files or deleted_files):
        logger.info("[green][+] No changes detected. Directory matches baseline.[/green]")
    else:
        console.print(table)
        logger.warning(f"[!] Integrity check failed: {len(new_files)} new, {len(altered_files)} altered, {len(deleted_files)} deleted.")

@audit_app.command("static-scan")
def static_scan(
    directory: str = typer.Argument(..., help="Directory of source code to scan")
):
    """
    Scans source code for potential hardcoded secrets and API keys.
    """
    console.print(f"[*] Running static analysis on {directory} for secrets")
    
    # Very basic regex patterns for demonstration
    patterns = {
        "Generic Secret": r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]([^'\"]+)['\"]",
        "AWS Access Key ID": r"(?i)(AKIA[0-9A-Z]{16})",
        "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----"
    }
    
    path = Path(directory)
    findings = 0
    
    for file_path in path.rglob("*"):
        if any(part in str(file_path) for part in ['.git', 'venv', 'node_modules', '__pycache__']):
            continue
            
        if file_path.is_file() and not str(file_path).endswith(('.pyc', '.exe', '.dll', '.whl')):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for secret_type, pattern in patterns.items():
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            logger.warning(f"[red][!] {secret_type} found in {file_path}[/red]")
                            findings += 1
            except Exception:
                pass
                
    if findings == 0:
        logger.info("[green][+] No hardcoded secrets found![/green]")
    else:
        logger.warning(f"[!] Scan complete. Found {findings} potential secrets.")

@audit_app.command("log-analyze")
def log_analyze(
    logfile: str = typer.Argument(..., help="Path to the log file to analyze")
):
    """
    Analyzes an Apache/Nginx access log for basic SQL injection or XSS attempts.
    """
    console.print(f"[*] Analyzing log file {logfile}")
    
    suspicious_patterns = [
        r"(%27)|(')|(--)|(%23)|(#)", # Basic SQLi patterns
        r"(%3C)|(<)|(%3E)|(>)|(script)" # Basic XSS patterns
    ]
    
    try:
        with open(logfile, 'r', errors='ignore') as f:
            lines = f.readlines()
            
        hits = 0
        for i, line in enumerate(lines):
            for pattern in suspicious_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    logger.warning(f"[red][!] Suspicious activity on line {i+1}:[/red] {line.strip()[:100]}...")
                    hits += 1
                    break
        
        if hits == 0:
            logger.info("[green][+] Log looks clean. No basic attacks detected.[/green]")
        else:
            logger.warning(f"[!] Found {hits} suspicious log entries.")
            
    except FileNotFoundError:
        logger.error(f"[!] Log file {logfile} not found.")

@audit_app.command("cloud-audit")
def cloud_audit(
    bucket_name: str = typer.Argument(..., help="The name of the AWS S3 bucket to audit")
):
    """
    Checks if an AWS S3 bucket is publicly accessible.
    """
    import boto3
    from botocore.exceptions import ClientError
    from botocore import UNSIGNED
    from botocore.client import Config
    
    console.print(f"[*] Auditing AWS S3 Bucket: {bucket_name}")
    
    # We use unsigned requests to see if it's open to the public
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
        logger.warning(f"[red][!] HIGH RISK: Bucket '{bucket_name}' is publicly readable![/red]")
        if 'Contents' in response:
            console.print("    [yellow]Sample files exposed:[/yellow]")
            for obj in response['Contents']:
                console.print(f"    - {obj['Key']}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            logger.info(f"[green][+] Bucket '{bucket_name}' is secure against public unauthenticated listing.[/green]")
        elif e.response['Error']['Code'] == 'NoSuchBucket':
            logger.error(f"[-] Bucket '{bucket_name}' does not exist.")
        else:
            logger.error(f"[!] Client error: {e}")
    except Exception as e:
        logger.error(f"[!] Failed to audit bucket: {e}")
