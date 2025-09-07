from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import os
import pickle
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)
CORS(app)

# Load FAISS index and metadata
INDEX_PATH = os.path.join(os.path.dirname(__file__), '../data/business_rule_faiss.index')
META_PATH = os.path.join(os.path.dirname(__file__), '../data/business_rule_faiss_metadata.pkl')
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

@app.route('/get-rules', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_rules():
    data = request.json
    # Build query string from form data
    query_parts = [
        data.get('state', ''),
        data.get('industry', ''),
        data.get('size', ''),
        data.get('structure', ''),
    ]
    for key in ['hasEmployees', 'hiresContractors', 'employsMinors', 'sellsGoods', 'providesServices', 'operatesOnline', 'operatesPhysical']:
        if data.get(key):
            query_parts.append(key)
    query_parts += data.get('complianceFocus', [])
    query = ' '.join([str(p) for p in query_parts if p])
    target_jurisdiction = data.get('state', '').strip()

    def embed(text):
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def cosine_similarity(vec1, vec2):
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    # Step 1: Filter by jurisdiction
    filtered = [r for r in metadata if r.get('jurisdiction', '').lower() == target_jurisdiction.lower()]
    federal = [r for r in metadata if r.get('jurisdiction', '').lower() == "federal"]
    if filtered:
        filtered += federal  # Add federal rules to state-specific results
    else:
        filtered = federal   # Only federal if no state match

    # Step 2: Rank results
    query_emb = embed(query)
    scored = []
    for r in filtered:
        jurisdiction_score = 1 if r.get('jurisdiction', '').lower() == target_jurisdiction.lower() else 0
        title_emb = embed(r.get('title', ''))
        content_emb = embed(r.get('summary', '') + " " + " ".join(r.get('key_requirements', [])))
        title_score = cosine_similarity(query_emb, title_emb)
        content_score = cosine_similarity(query_emb, content_emb)
        score = 0.6 * jurisdiction_score + 0.3 * title_score + 0.1 * content_score
        scored.append((score, r))
    flag_order = {"red": 3, "yellow": 2, "green": 1}
    sorted_results = [r for _, r in sorted(scored, key=lambda x: (x[0], flag_order.get(x[1].get('flag', 'green'), 0)), reverse=True)]

    # Ensure at least 3 state and 3 federal rules
    state_rules = [r for r in sorted_results if r.get('jurisdiction', '').lower() == target_jurisdiction.lower()]
    federal_rules = [r for r in sorted_results if r.get('jurisdiction', '').lower() == "federal"]

    # Collect missing jurisdictions and counts
    missing = {}
    if len(state_rules) < 3:
        missing[target_jurisdiction] = 3 - len(state_rules)
    if len(federal_rules) < 3:
        missing["Federal"] = 3 - len(federal_rules)

    def llm_fallback_combined(missing_dict, query):
        if not missing_dict:
            return {}
        jurisdictions = "\n".join([f"- {j}: {c}" for j, c in missing_dict.items()])
        prompt = f"""
You are a compliance assistant for small businesses. For each jurisdiction below, provide the specified number of important regulations relevant to this business query: {query}.
Format your response as a JSON object where each key is the jurisdiction and the value is a list of regulations (each as a JSON object with fields: title, jurisdiction, summary, key_requirements, recommended_actions).

Jurisdictions and counts needed:
{jurisdictions}
Business query: {query}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.2
        )
        try:
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {}

    # Call LLM fallback once for all missing jurisdictions
    fallback_results = llm_fallback_combined(missing, query)
    if len(state_rules) < 3 and target_jurisdiction in fallback_results:
        state_rules += fallback_results[target_jurisdiction]
    if len(federal_rules) < 3 and "Federal" in fallback_results:
        federal_rules += fallback_results["Federal"]

    final_results = state_rules[:3] + federal_rules[:3]

    def synthesize_answer(form_data, rules):
        user_info = []
        for k, v in form_data.items():
            if isinstance(v, list):
                v = ', '.join(v)
            user_info.append(f"{k}: {v}")
        user_info_str = '\n'.join(user_info)
        rules_str = json.dumps(rules, indent=2, ensure_ascii=False)
        prompt = f"""
You are a compliance assistant for small businesses. The user's business info is:
{user_info_str}

Here are the most relevant rules:
{rules_str}

Based on these, summarize what rules apply and what actions the user should take. Be concise and actionable. Only use information from the rules provided. Format your answer for easy reading.
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.2
        )
        return response.choices[0].message.content

    summary = synthesize_answer(data, final_results)
    return jsonify({"results": final_results, "summary": summary})

if __name__ == "__main__":
    app.run()
