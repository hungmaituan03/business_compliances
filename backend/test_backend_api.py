import requests
import json

url = "https://business-compliances.onrender.com/get-rules"
payload = {
    "state": "CA",
    "industry": "Retail",
    "size": "1-10 employees",
    "structure": "LLC",
    "complianceFocus": ["Tax"]
}
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)