import json

# Load federal summaries

# Load federal summaries
with open("federal/all_summaries.json", "r", encoding="utf-8") as f:
    federal_summaries = json.load(f)

# Load state summaries
with open("states/state_summaries.json", "r", encoding="utf-8") as f:
    state_summaries = json.load(f)

# Combine both lists
all_summaries = federal_summaries + state_summaries

# Save to a single file in the data directory
with open("all_business_rule_summaries.json", "w", encoding="utf-8") as f:
    json.dump(all_summaries, f, indent=2, ensure_ascii=False)

print("Combined summaries saved to all_business_rule_summaries.json")
