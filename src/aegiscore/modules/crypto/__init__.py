import typer
import hashlib
import base64
import urllib.parse
import requests
from aegiscore.core.logger import logger, console

crypto_app = typer.Typer(help="Cryptography & Password Tools")

@crypto_app.command("hash")
def generate_hash(
    text: str = typer.Argument(..., help="The text to hash"),
    algo: str = typer.Option("sha256", help="Algorithm to use (md5, sha1, sha256, sha512)")
):
    """
    Generates a cryptographic hash for a given string.
    """
    try:
        h = hashlib.new(algo)
        h.update(text.encode('utf-8'))
        result = h.hexdigest()
        console.print(f"[bold cyan]{algo.upper()}:[/bold cyan] {result}")
    except ValueError:
        logger.error(f"[!] Unsupported algorithm: {algo}")

@crypto_app.command("encode")
def encode_text(
    text: str = typer.Argument(..., help="Text to encode"),
    format: str = typer.Option("base64", help="Format to encode to (base64, hex, url)")
):
    """
    Encodes text into various formats.
    """
    if format == "base64":
        result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif format == "hex":
        result = text.encode('utf-8').hex()
    elif format == "url":
        result = urllib.parse.quote(text)
    else:
        logger.error(f"[!] Unsupported format: {format}")
        return
        
    console.print(f"[bold cyan]Encoded ({format}):[/bold cyan] {result}")

@crypto_app.command("decode")
def decode_text(
    text: str = typer.Argument(..., help="Text to decode"),
    format: str = typer.Option("base64", help="Format to decode from (base64, hex, url)")
):
    """
    Decodes text from various formats.
    """
    try:
        if format == "base64":
            result = base64.b64decode(text).decode('utf-8')
        elif format == "hex":
            result = bytes.fromhex(text).decode('utf-8')
        elif format == "url":
            result = urllib.parse.unquote(text)
        else:
            logger.error(f"[!] Unsupported format: {format}")
            return
            
        console.print(f"[bold cyan]Decoded ({format}):[/bold cyan] {result}")
    except Exception as e:
        logger.error(f"[!] Decoding failed: {e}")

@crypto_app.command("audit-pwd")
def audit_password(
    password: str = typer.Argument(..., help="Password to check against HaveIBeenPwned")
):
    """
    Checks if a password has been compromised using the HaveIBeenPwned API (uses k-Anonymity).
    """
    console.print("[*] Auditing password securely via HaveIBeenPwned (k-Anonymity)")
    
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    logger.warning(f"[red][!] CAUTION! This password has been seen {count} times in data breaches.[/red]")
                    return
            logger.info("[green][+] Good news! This password was not found in known breaches.[/green]")
        else:
            logger.error(f"[!] API request failed with status code {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"[!] Could not connect to API: {e}")

@crypto_app.command("crack")
def crack_hash(
    hash_value: str = typer.Argument(..., help="The hash to crack"),
    wordlist: str = typer.Argument(..., help="Path to the dictionary wordlist"),
    algo: str = typer.Option("md5", help="Hashing algorithm used")
):
    """
    Performs an offline dictionary attack to crack a hash.
    """
    console.print(f"[*] Attempting to crack {algo} hash: {hash_value}")
    
    try:
        with open(wordlist, 'r', errors='ignore') as f:
            for line in f:
                word = line.strip()
                try:
                    h = hashlib.new(algo)
                    h.update(word.encode('utf-8'))
                    if h.hexdigest() == hash_value:
                        logger.info(f"[green][+] Hash cracked![/green] Password is: [bold]{word}[/bold]")
                        return
                except ValueError:
                    logger.error(f"[!] Unsupported algorithm: {algo}")
                    return
                    
        logger.warning("[-] Hash not found in the wordlist.")
    except FileNotFoundError:
        logger.error(f"[!] Wordlist file {wordlist} not found.")

@crypto_app.command("stego-hide")
def stego_hide(
    image: str = typer.Argument(..., help="Path to the cover image (e.g., cover.png)"),
    secret: str = typer.Argument(..., help="The secret message to hide"),
    output: str = typer.Option("secret_image.png", help="Output file name")
):
    """
    Hides a secret message inside an image file (Steganography).
    """
    console.print(f"[*] Hiding secret inside {image}")
    try:
        from stegano import lsb
        secret_image = lsb.hide(image, secret)
        secret_image.save(output)
        logger.info(f"[green][+] Success! Secret hidden inside {output}[/green]")
    except ImportError:
        logger.error("[!] Stegano library not found. Run 'pip install stegano'.")
    except Exception as e:
        logger.error(f"[!] Steganography failed: {e}")

@crypto_app.command("stego-reveal")
def stego_reveal(
    image: str = typer.Argument(..., help="Path to the image containing a secret")
):
    """
    Reveals a hidden secret message from an image file.
    """
    console.print(f"[*] Analyzing {image} for hidden secrets...")
    try:
        from stegano import lsb
        secret = lsb.reveal(image)
        if secret:
            logger.info(f"[green][+] Secret Revealed![/green]\n[bold]{secret}[/bold]")
        else:
            logger.warning("[-] No secret message found in this image.")
    except IndexError:
        logger.warning("[-] No secret message found or image is not encoded properly.")
    except Exception as e:
        logger.error(f"[!] Failed to analyze image: {e}")
