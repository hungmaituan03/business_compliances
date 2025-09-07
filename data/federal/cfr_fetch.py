import requests
from bs4 import BeautifulSoup
import re
import os

# List of CFR titles and keywords relevant to small businesses
CFR_LINKS = [
    "https://www.ecfr.gov/current/title-13",  # SBA, small business credit/assistance
    "https://www.ecfr.gov/current/title-29",  # Labor, OSHA
    "https://www.ecfr.gov/current/title-26",  # Internal Revenue
]
KEYWORDS = ["small business", "small entity", "self-employed", "sole proprietor", "small employer", "small organization"]

CFR_TITLE_LINKS = [
    "https://www.ecfr.gov/current/title-13",  # SBA, small business credit/assistance
    "https://www.ecfr.gov/current/title-29",  # Labor, OSHA
    "https://www.ecfr.gov/current/title-26",  # Internal Revenue
]

def fetch_cfr_sections():
    found_links = set()
    for base_url in CFR_LINKS:
        print(f"Searching: {base_url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Find all links and filter by keywords
            for a in soup.find_all("a", href=True):
                text = a.get_text(strip=True).lower()
                href = a["href"]
                if any(kw in text for kw in KEYWORDS):
                    full_url = href if href.startswith("http") else f"https://www.ecfr.gov{href}"
                    found_links.add(full_url)
        except Exception as e:
            print(f"Failed to fetch {base_url}: {e}")
    # Write results to federal_links.txt
    with open("federal_links.txt", "a", encoding="utf-8") as f:
        # If no links found, append the three main CFR title links
        if not found_links:
            print("No specific CFR links found. Appending main CFR title links.")
            for link in CFR_TITLE_LINKS:
                f.write(link + "\n")
                print(f"Saved CFR title link: {link}")
        else:
            for link in sorted(found_links):
                f.write(link + "\n")
                print(f"Saved CFR link: {link}")

if __name__ == "__main__":
    fetch_cfr_sections()
