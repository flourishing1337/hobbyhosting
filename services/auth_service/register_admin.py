import requests

BASE_URL = "http://localhost:8000"

data = {
    "username": "admin@hobbyhosting.org",
    "password": "supersecret123",
}

response = requests.post(f"{BASE_URL}/auth/register", json=data)

print("✅ Response:", response.status_code)
print(response.json())
