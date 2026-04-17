import requests

# Ensure /api/test is at the end
URL = "https://dogo1017.pythonanywhere.com/test"

try:
    response = requests.post(URL, json={"msg": "Hello!"})
    print(f"Status Code: {response.status_code}")
    
    if not response.text.strip():
        print("ERROR: The server sent a totally blank response (Empty Body).")
        print("This means the Reload failed or the WSGI file is wrong.")
    else:
        print(f"Server Response: {response.text}")
        # Only try to parse if it's not empty and likely JSON
        if response.headers.get('Content-Type') == 'application/json':
            print("JSON Data:", response.json())
        else:
            print("Response is not JSON.")

except Exception as e:
    print(f"Caught Error: {e}")