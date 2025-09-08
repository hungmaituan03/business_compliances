import json
from app import app

def test_get_rules():
    payload = {
        "state": "CA",
        "industry": "Retail",
        "size": "1-10 employees",
        "structure": "LLC",
        "complianceFocus": ["Tax"]
    }
    with app.test_client() as client:
        response = client.post("/get-rules", data=json.dumps(payload), content_type="application/json")
        print("Status Code:", response.status_code)
        print("Response:", response.get_data(as_text=True))

if __name__ == "__main__":
    test_get_rules()