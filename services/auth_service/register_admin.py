import requests

BASE_URL = "http://localhost:8000"

data = {
    "email": "admin@hobbyhosting.org",
    "password": "supersecret123",
    "is_admin": True,
}

response = requests.post(f"{BASE_URL}/register", json=data)

print("✅ Response:", response.status_code)
print(response.json())
