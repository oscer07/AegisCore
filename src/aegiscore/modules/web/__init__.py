import typer
import requests
import asyncio
import aiohttp
from typing import List
from aegiscore.core.logger import logger, console
from bs4 import BeautifulSoup
from rich.table import Table
import urllib.parse

web_app = typer.Typer(help="Web Application Security Tools")

@web_app.command("headers")
def analyze_headers(
    url: str = typer.Argument(..., help="The URL to analyze (include http:// or https://)")
):
    """
    Analyzes HTTP security headers for a given URL.
    """
    console.print(f"[*] Analyzing security headers for {url}")
    
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        security_headers = {
            "Strict-Transport-Security": "Missing HSTS - site may be vulnerable to downgrade attacks.",
            "Content-Security-Policy": "Missing CSP - site may be vulnerable to XSS.",
            "X-Frame-Options": "Missing X-Frame-Options - site may be vulnerable to Clickjacking.",
            "X-Content-Type-Options": "Missing X-Content-Type-Options - vulnerable to MIME-sniffing."
        }
        
        table = Table(title=f"Security Headers for {url}")
        table.add_column("Header", style="cyan")
        table.add_column("Status", style="green")
        
        warnings = 0
        
        for header, warning in security_headers.items():
            if header in headers:
                table.add_row(header, "[green]Present[/green]")
            else:
                table.add_row(header, "[red]Missing[/red]")
                logger.warning(f"[!] {warning}")
                warnings += 1
                
        console.print(table)
        
        if warnings == 0:
            logger.info("[green][+] Excellent! All standard security headers are present.[/green]")
        else:
            logger.warning(f"[!] Found {warnings} missing security headers.")
            
    except requests.RequestException as e:
        logger.error(f"[!] Failed to connect to {url}: {e}")

async def fetch(session: aiohttp.ClientSession, url: str) -> tuple:
    try:
        async with session.get(url, allow_redirects=False, timeout=3) as response:
            return url, response.status
    except Exception:
        return url, 0

async def run_fuzzer(base_url: str, wordlist: List[str]) -> List[str]:
    found = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for word in wordlist:
            url = urllib.parse.urljoin(base_url, word)
            tasks.append(fetch(session, url))
            
        results = await asyncio.gather(*tasks)
        for url, status in results:
            if status in [200, 301, 302, 401, 403]:
                found.append(url)
                logger.info(f"[green][+] Found: {url} (Status: {status})[/green]")
    return found

@web_app.command("fuzz")
def directory_fuzz(
    url: str = typer.Argument(..., help="The target URL"),
    wordlist: str = typer.Option(None, help="Path to a custom wordlist file")
):
    """
    Fuzzes directories and endpoints to find hidden paths.
    """
    console.print(f"[*] Fuzzing directories on {url}")
    
    if not url.endswith('/'):
        url += '/'
        
    words = ["admin", "login", "dashboard", "api", "v1", "backup", ".git", "config", "test"]
    
    if wordlist:
        try:
            with open(wordlist, 'r') as f:
                words = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"[!] Wordlist {wordlist} not found. Using default.")
            
    logger.info(f"[*] Using wordlist with {len(words)} entries.")
    
    try:
        found = asyncio.run(run_fuzzer(url, words))
        if not found:
            logger.info("[-] No hidden directories found.")
        else:
            logger.info(f"[+] Fuzzing complete. Found {len(found)} endpoints.")
    except KeyboardInterrupt:
        logger.warning("[!] Fuzzing interrupted.")

@web_app.command("vuln-scan")
def vuln_scan(
    url: str = typer.Argument(..., help="The target URL to test for basic XSS/SQLi")
):
    """
    Scans URL parameters for basic XSS and SQLi vulnerabilities.
    """
    console.print(f"[*] Scanning {url} for basic vulnerabilities")
    
    if "?" not in url:
        logger.warning("[-] Target URL has no parameters (e.g., ?id=1). Cannot perform basic parameter injection.")
        return
        
    xss_payload = "<script>alert(1)</script>"
    sqli_payload = "'"
    
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    try:
        # Test XSS
        for param in params.keys():
            test_params = params.copy()
            test_params[param] = xss_payload
            test_url = f"{base_url}?{urllib.parse.urlencode(test_params, doseq=True)}"
            
            res = requests.get(test_url, timeout=5)
            if xss_payload in res.text:
                logger.warning(f"[red][!] Potential XSS found in parameter: {param}[/red]")
                
        # Test SQLi
        for param in params.keys():
            test_params = params.copy()
            test_params[param] = sqli_payload
            test_url = f"{base_url}?{urllib.parse.urlencode(test_params, doseq=True)}"
            
            res = requests.get(test_url, timeout=5)
            # Basic check for SQL errors in response
            if any(error in res.text.lower() for error in ["sql syntax", "mysql_fetch", "sqlite3"]):
                logger.warning(f"[red][!] Potential SQLi found in parameter: {param}[/red]")
                
        logger.info("[+] Vulnerability scan complete.")
        
    except requests.RequestException as e:
        logger.error(f"[!] Request failed: {e}")

@web_app.command("scrape")
def scrape_page(
    url: str = typer.Argument(..., help="The URL to scrape (include http:// or https://)")
):
    """
    Crawls a web page to extract links and email addresses.
    """
    import re
    console.print(f"[*] Scraping {url} for links and emails")
    
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract links
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('http'):
                links.add(href)
            elif href.startswith('/'):
                links.add(urllib.parse.urljoin(url, href))
                
        # Extract emails using regex
        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        emails = set(re.findall(email_pattern, response.text))
        
        if links:
            logger.info(f"[green][+] Found {len(links)} links:[/green]")
            for link in sorted(list(links))[:20]: # show top 20
                console.print(f"    - {link}")
            if len(links) > 20:
                console.print("    - ... (more links hidden)")
                
        if emails:
            logger.info(f"[green][+] Found {len(emails)} emails:[/green]")
            for email in emails:
                console.print(f"    - {email}")
        else:
            logger.info("[-] No emails found.")
            
    except requests.RequestException as e:
        logger.error(f"[!] Failed to fetch {url}: {e}")
