import typer
import asyncio
from typing import List, Optional
from aegiscore.core.logger import logger, console
from rich.progress import Progress
import socket

recon_app = typer.Typer(help="Network & Reconnaissance Tools")

async def scan_port(ip: str, port: int, timeout: float = 1.0) -> Optional[int]:
    """Attempts to connect to a specific port asynchronously."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return port
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

async def run_port_scan(ip: str, start_port: int, end_port: int) -> List[int]:
    """Runs the asynchronous port scan."""
    open_ports = []
    
    with Progress() as progress:
        task = progress.add_task(f"[cyan]Scanning {ip}...", total=(end_port - start_port + 1))
        
        # We chunk tasks to avoid opening too many sockets at once
        chunk_size = 500
        for i in range(start_port, end_port + 1, chunk_size):
            chunk_end = min(i + chunk_size, end_port + 1)
            tasks = [scan_port(ip, p) for p in range(i, chunk_end)]
            results = await asyncio.gather(*tasks)
            
            for result in results:
                if result:
                    open_ports.append(result)
                    logger.info(f"[green][+] Port {result} is open[/green]")
            
            progress.update(task, advance=chunk_size)
            
    return open_ports

@recon_app.command("port-scan")
def port_scan(
    ip: str = typer.Argument(..., help="The IP address to scan"),
    start: int = typer.Option(1, help="Starting port"),
    end: int = typer.Option(1024, help="Ending port")
):
    """
    Perform a fast asynchronous port scan on a target IP.
    """
    console.print(f"[*] Starting port scan on {ip} ({start}-{end})")
    try:
        open_ports = asyncio.run(run_port_scan(ip, start, end))
        if not open_ports:
            logger.info("[-] No open ports found in the specified range.")
        else:
            logger.info(f"[+] Scan complete. Found {len(open_ports)} open ports.")
    except KeyboardInterrupt:
        logger.warning("[!] Scan interrupted by user.")

@recon_app.command("banner")
def banner_grab(
    ip: str = typer.Argument(..., help="The target IP address"),
    port: int = typer.Argument(..., help="The target port")
):
    """
    Connects to an open port and grabs the service banner to identify software.
    """
    console.print(f"[*] Grabbing banner from {ip}:{port}")
    try:
        s = socket.socket()
        s.settimeout(3.0)
        s.connect((ip, port))
        
        # Send a basic payload for services that require a request first (like HTTP)
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        if banner:
            logger.info(f"[green][+] Banner from {port}:[/green]\n{banner}")
        else:
            logger.info("[-] No banner returned.")
    except Exception as e:
        logger.error(f"[!] Failed to grab banner: {e}")
    finally:
        s.close()
        
@recon_app.command("osint")
def osint_gather(
    target: str = typer.Argument(..., help="Domain name or IP address")
):
    """
    Gathers basic OSINT information about a target.
    """
    console.print(f"[*] Gathering OSINT for {target}")
    import requests
    
    # Example: Query the free ip-api for geolocation info
    try:
        response = requests.get(f"http://ip-api.com/json/{target}")
        data = response.json()
        if data.get('status') == 'success':
            logger.info(f"[green][+] OSINT Data:[/green]")
            for key, value in data.items():
                console.print(f"    [bold]{key.capitalize()}[/bold]: {value}")
        else:
            logger.error("[!] Failed to retrieve OSINT data or invalid target.")
    except Exception as e:
        logger.error(f"[!] Error making OSINT request: {e}")

@recon_app.command("subdomains")
def subdomains_enum(
    domain: str = typer.Argument(..., help="The target domain (e.g., example.com)")
):
    """
    Finds hidden subdomains using public OSINT APIs (like crt.sh).
    """
    console.print(f"[*] Enumerating subdomains for {domain}")
    import requests
    
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data:
                name_value = entry.get('name_value', '')
                if '*' not in name_value: # skip wildcards
                    subdomains.update(name_value.split('\n'))
            
            if subdomains:
                logger.info(f"[green][+] Found {len(subdomains)} subdomains:[/green]")
                for sub in sorted(subdomains):
                    console.print(f"    - {sub}")
            else:
                logger.info("[-] No subdomains found.")
        else:
            logger.error(f"[!] Failed to fetch data from crt.sh (Status {response.status_code})")
    except Exception as e:
        logger.error(f"[!] Request failed: {e}")

@recon_app.command("pcap")
def parse_pcap(
    pcap_file: str = typer.Argument(..., help="Path to the .pcap file to analyze")
):
    """
    Analyzes a PCAP network capture file for basic anomalies or plaintext data.
    """
    console.print(f"[*] Analyzing PCAP file: {pcap_file}")
    try:
        from scapy.all import rdpcap, TCP, Raw
        packets = rdpcap(pcap_file)
        logger.info(f"[*] Loaded {len(packets)} packets.")
        
        found = 0
        for pkt in packets:
            if pkt.haslayer(TCP) and pkt.haslayer(Raw):
                payload = pkt[Raw].load.decode('utf-8', errors='ignore')
                # Basic check for FTP auth or HTTP Basic Auth
                if "USER " in payload or "PASS " in payload or "Authorization: Basic" in payload:
                    logger.warning(f"[red][!] Plaintext credentials detected in packet![/red]\n{payload[:100].strip()}...")
                    found += 1
                    
        if found == 0:
            logger.info("[green][+] No obvious plaintext credentials found in this PCAP.[/green]")
        else:
            logger.warning(f"[!] Found {found} packets with potential plaintext credentials.")
            
    except ImportError:
        logger.error("[!] Scapy is not installed. Run 'pip install scapy' to use this feature.")
    except Exception as e:
        logger.error(f"[!] Failed to parse PCAP: {e}")
