import requests
from bs4 import BeautifulSoup
import os

def is_small_business_link(href, anchor_text):
    href_lower = href.lower()
    anchor_lower = anchor_text.lower()
    # Only include links that are highly relevant to small business
    if "small-business" in href_lower or "self-employed" in href_lower:
        return True
    keywords = ["small business", "self-employed", "sole proprietor", "business tax", "business owner", "employer identification number", "schedule c", "schedule se"]
    if any(kw in anchor_lower for kw in keywords):
        return True
    return False

def scrape_irs_hub_and_details():
    hub_url = "https://www.irs.gov/businesses/small-businesses-self-employed"
    response = requests.get(hub_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all relevant links in the main content
    main_content = soup.find("main") or soup
    links = set()
    for a in main_content.find_all("a", href=True):
        href = a["href"]
        anchor_text = a.get_text(strip=True)
        if is_small_business_link(href, anchor_text):
            full_url = f"https://www.irs.gov{href}" if href.startswith("/") else href
            links.add(full_url)

    print(f"Found {len(links)} highly relevant small business IRS links.")
    # Write all links to a single file
    with open("federal_links.txt", "w", encoding="utf-8") as f:
        for link in sorted(links):
            f.write(link + "\n")
            print(f"Saved link: {link}")

if __name__ == "__main__":
    scrape_irs_hub_and_details()