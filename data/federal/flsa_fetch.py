import requests
from bs4 import BeautifulSoup

FLSA_URL = "https://www.dol.gov/agencies/whd/flsa"

KEYWORDS = ["minimum wage", "overtime", "child labor", "recordkeeping", "exempt", "nonexempt", "hours worked", "salary basis", "compliance"]

def scrape_flsa():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(FLSA_URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    found_links = set()
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True).lower()
        href = a["href"]
        if any(kw in text for kw in KEYWORDS):
            full_url = href if href.startswith("http") else f"https://www.dol.gov{href}"
            found_links.add(full_url)
    with open("federal_links.txt", "a", encoding="utf-8") as f:
        for link in sorted(found_links):
            f.write(link + "\n")
            print(f"Saved FLSA link: {link}")

if __name__ == "__main__":
    scrape_flsa()
