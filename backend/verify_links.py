import requests
import os
import re

def is_valid_gov_domain(url):
    # Accept .gov or .mil domains only
    return re.match(r"^https?://([\w.-]+\.)?(gov|mil)(/|$)", url)

def verify_links(input_file, output_file=None):
    if output_file is None:
        output_file = input_file
    seen = set()
    valid_links = []
    with open(input_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]
    for link in links:
        if link in seen:
            print(f"Duplicate: {link}")
            continue
        if not is_valid_gov_domain(link):
            print(f"Invalid domain: {link}")
            continue
        try:
            resp = requests.head(link, allow_redirects=True, timeout=10)
            if resp.status_code == 404:
                print(f"404 Not Found: {link}")
                continue
            elif resp.status_code >= 400:
                print(f"Error {resp.status_code}: {link}")
                continue
        except Exception as e:
            print(f"Request failed: {link} ({e})")
            continue
        valid_links.append(link)
        seen.add(link)
    with open(output_file, "w", encoding="utf-8") as f:
        for link in valid_links:
            f.write(link + "\n")
    print(f"Verification complete. {len(valid_links)} valid links written to {output_file}.")