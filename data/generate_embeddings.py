import json
import openai
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load combined summaries
with open("all_business_rule_summaries.json", "r", encoding="utf-8") as f:
    all_summaries = json.load(f)

embeddings = []

for rule in all_summaries:
    # Use summary + key_requirements + recommended_actions for embedding
    text = rule.get("summary", "")
    text += " " + " ".join(rule.get("key_requirements", []))
    text += " " + " ".join(rule.get("recommended_actions", []))
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        embeddings.append({
            "url": rule.get("url"),
            "title": rule.get("title"),
            "jurisdiction": rule.get("jurisdiction"),
            "embedding": embedding,
            "summary": rule.get("summary"),
            "key_requirements": rule.get("key_requirements", []),
            "important_deadlines": rule.get("important_deadlines", []),
            "recommended_actions": rule.get("recommended_actions", []),
            "flag": rule.get("flag", "")
        })
    except Exception as e:
        print(f"Failed to generate embedding for {rule.get('url')}: {e}")

with open("business_rule_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embeddings, f, indent=2, ensure_ascii=False)

print("Embeddings saved to business_rule_embeddings.json")
