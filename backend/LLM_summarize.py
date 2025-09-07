import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Set your OpenAI API key here or use environment variable
load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def fetch_page_text(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract meta description if available
    meta_desc = soup.find("meta", attrs={"name": "description"})
    meta_content = meta_desc["content"] if meta_desc and meta_desc.has_attr("content") else ""

    # Extract title
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    # Extract headings
    headings = []
    for tag in ["h1", "h2", "h3"]:
        headings.extend([h.get_text(strip=True) for h in soup.find_all(tag)])

    # Extract first 3 paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")[:3]]

    # Extract bullet points (li elements)
    bullets = [li.get_text(strip=True) for li in soup.find_all("li")[:10]]

    # Combine all extracted text
    sections = [title, meta_content] + headings + paragraphs + bullets
    text = "\n".join([s for s in sections if s])

    # Truncate to 2000 characters
    return text[:2000]

def summarize_with_llm(url):
    page_text = fetch_page_text(url)
    prompt = f"""
Summarize the following links. Only include information that is directly relevant to small business owners. Ignore content that does not apply to small businesses. Return the summary as a JSON object with these fields, in this exact order:
1. title
2. url (use this exact URL: {url})
3. jurisdiction (e.g., 'Federal', 'California', etc.)
4. flag (importance of the regulation: 'red' for immediate attention, 'yellow' for should be considered, 'green' for see if applicable)
5. summary (brief overview of the page)
6. key_requirements (list the most important rules or obligations)
7. important_deadlines (list any critical dates or timeframes)
8. recommended_actions (clear, practical steps the business owner should take)

Assign the 'flag' field based on urgency and relevance:
- Use 'red' for regulations that need immediate attention (critical compliance, deadlines, penalties).
- Use 'yellow' for regulations that should be considered (important but not urgent).
- Use 'green' for regulations that may not apply to all, informational only.

The summary should be actionable and focused on helping small business owners comply with all relevant laws and regulations (including but not limited to tax, labor, licensing, environmental, and other compliance areas). Do not include any extra fields or information outside the JSON object.

Page URL: {url}
Page content:
{page_text}
Provide the summary in valid JSON format only."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.2
    )
    summary = response.choices[0].message.content
    return summary

def summarize_links_from_file(links_file, output_file="all_summaries.json"):
    summaries = []
    with open(links_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]
    for link in links:
        print(f"Summarizing: {link}")
        summary = summarize_with_llm(link)
        try:
            summary_json = json.loads(summary)
            summaries.append(summary_json)
        except Exception as e:
            print(f"Failed to parse summary for {link}: {e}")
            with open("error_output.txt", "a", encoding="utf-8") as ef:
                ef.write(f"URL: {link}\n{summary}\n\n")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)
