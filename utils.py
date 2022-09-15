#!/usr/bin/env python3
"""Command-line interface for performing several security tests."""

import requests
import whois
import typer
import nmap3
from lxml import html

app = typer.Typer()

@app.command()
def domain(name: str):
    """Print the domain registrant's name and organization."""
    results = whois.whois(name)
    print(f"{name} is registered by {results.name} - {results.org}")

@app.command()
def portscan(target: str, top: int = 10):
    """Perform a portscan against a target on the top ports,
    and print the open ports and services."""
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(target, default = top)
    ip, *_unused = results.keys()
    for port in results[ip]["ports"]:
        if "open" in port["state"]:
            print(f"{port['portid']} {port['service']['name']}")

def get_page(url: str, proxy: str = None):
    """Perform a GET request and return response object."""
    proxies = None
    if proxy:
        proxies = {"http": f"http://{proxy}"}
    response = requests.get(url, proxies=proxies)
    return response

@app.command()
def forms(url: str, proxy: str = None):
    """Find a form in a page and print form details."""
    response = get_page(url, proxy)
    tree = html.fromstring(response.content)
    for form in tree.xpath("//form"):
        print(f"Found a {form.method} form for {form.action}")
        for field in form.fields:
            print(f"Contains input field {field}")

if __name__ == "__main__":
    app()
