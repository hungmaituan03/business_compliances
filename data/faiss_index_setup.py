import json
import numpy as np
import faiss
import pickle

# Load embeddings
with open("business_rule_embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract vectors and metadata
vectors = []
metadata = []
for entry in data:
    vectors.append(np.array(entry["embedding"], dtype=np.float32))
    metadata.append({
        "url": entry["url"],
        "title": entry["title"],
        "jurisdiction": entry["jurisdiction"],
        "summary": entry["summary"],
        "key_requirements": entry["key_requirements"],
        "important_deadlines": entry["important_deadlines"],
        "recommended_actions": entry["recommended_actions"],
        "flag": entry["flag"]
    })

vectors_np = np.stack(vectors)

# Build FAISS index
dim = vectors_np.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(vectors_np)

# Save index and metadata
faiss.write_index(index, "business_rule_faiss.index")
with open("business_rule_faiss_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("FAISS index and metadata saved.")
