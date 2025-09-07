import requests
import json

def test_backend():
    url = "https://business-compliances.onrender.com/get-rules"
    payload = {
        "state": "California",
        "industry": "Retail",
        "size": "1-10 employees",
        "structure": "LLC",
        "hasEmployees": True,
        "hiresContractors": False,
        "employsMinors": False,
        "sellsGoods": True,
        "providesServices": True,
        "operatesOnline": False,
        "operatesPhysical": True,
        "complianceFocus": ["Tax", "Labor"]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_backend()
