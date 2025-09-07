import json
import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

# Load the list of main state sites
with open("state_main_sites.json", "r", encoding="utf-8") as f:
    state_sites = json.load(f)

# Import the LLM summarization module
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))
spec = spec_from_file_location("LLM_summarize", os.path.join(backend_dir, "LLM_summarize.py"))
LLM_summarize = module_from_spec(spec)
spec.loader.exec_module(LLM_summarize)

summaries = []
for entry in state_sites:
    state = entry["state"]
    url = entry["url"]
    print(f"Summarizing for {state}: {url}")
    try:
        summary = LLM_summarize.summarize_with_llm(url)
        summary_json = json.loads(summary)
        summary_json["state"] = state  # Add state info to summary
        summaries.append(summary_json)
    except Exception as e:
        print(f"Failed to summarize {url}: {e}")
        with open("state_error_output.txt", "a", encoding="utf-8") as ef:
            ef.write(f"State: {state}\nURL: {url}\nError: {e}\n\n")

with open("state_summaries.json", "w", encoding="utf-8") as f:
    json.dump(summaries, f, indent=2, ensure_ascii=False)

print("All state summaries complete. Output saved to state_summaries.json.")
