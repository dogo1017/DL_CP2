import requests

SENDER_ID = "user1"
BASE_URL = "https://dogo1017.pythonanywhere.com"

choice = input("S/R (Send/Receive): ").lower().strip()

if choice == "s":
    url = f"{BASE_URL}/message"
    message_content = input("message send: ")
    payload = {"id": SENDER_ID, "msg": message_content}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Sent successfully: {message_content}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Caught Error: {e}")

else:
    url = f"{BASE_URL}/receive"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                print(f"{entry['id']}: {entry['message']}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Caught Error: {e}")
