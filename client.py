import requests

# Ensure /test is at the end
URL = "https://pythonanywhere.com"

try:
    response = requests.post(URL, json={"msg": "Hello!"})
    print(f"Status Code: {response.status_code}")
    
    if not response.text.strip():
        print("ERROR: The server sent a totally blank response (Empty Body).")
        print("This means the Reload failed or the WSGI file is wrong.")
    else:
        print(f"Server Response: {response.text}")
        # Only try to parse if it's not empty
        print("JSON Data:", response.json())

except Exception as e:
    print(f"Caught Error: {e}")
