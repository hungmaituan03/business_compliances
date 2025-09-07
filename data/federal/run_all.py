import subprocess
import os
import sys

FEDERAL_SCRIPTS = [
    "cfr_fetch.py",
    "irs_fetch.py",
    "flsa_fetch.py"
]
FEDERAL_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(FEDERAL_DIR, '../../backend'))

# Run all federal link collection scripts
for script in FEDERAL_SCRIPTS:
    script_path = os.path.join(FEDERAL_DIR, script)
    print(f"Running {script_path}...")
    subprocess.run([sys.executable, script_path], check=True)

# Validate links
verify_script = os.path.join(BACKEND_DIR, "verify_links.py")
print(f"Validating links with {verify_script}...")
subprocess.run([sys.executable, verify_script], check=True)

# Summarize links with LLM
print("Summarizing links with LLM_summarize...")
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("LLM_summarize", os.path.join(BACKEND_DIR, "LLM_summarize.py"))
LLM_summarize = module_from_spec(spec)
spec.loader.exec_module(LLM_summarize)
LLM_summarize.summarize_links_from_file(os.path.join(FEDERAL_DIR, "federal_links.txt"), os.path.join(FEDERAL_DIR, "all_summaries.json"))

print("All steps complete. Summaries are ready for database import.")
