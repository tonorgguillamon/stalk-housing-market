from dotenv import load_dotenv
import os
import base64
import requests
load_dotenv()

APIKEY = os.getenv("APIKEY", None)
SECRET = os.getenv("SECRET", None)

if not APIKEY or not SECRET:
    raise Exception("Missing credentials")

credentials = f"{APIKEY}:{SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

tokenUrl = "https://api.idealista.com/oauth/token"

data = {
    "grant_type": "client_credentials",
    "scope": "read"
}

headers = {"Authorization": f"Basic {encoded_credentials}", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

response = requests.post(
    url=tokenUrl, 
    data=data,
    headers=headers
)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data["access_token"]
else:
    print("Error:", response.status_code, response.text)