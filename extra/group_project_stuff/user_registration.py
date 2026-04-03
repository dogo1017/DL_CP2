import hashlib
import csv

def register(users,password,username):
    usernames = []
    for user in users:
        usernames.append(user["username"])
    password_encoded = password.encode("utf-8")
    hashed_password = hashlib.shake_128(password_encoded)
    hex_password = hashed_password.hexdigest(4)
    users.append({"username" : username, "password" : hex_password, "high score" : 0, "status" : "active"})
    return users

def load_csv():
    with open("user_info.csv", "r") as user_list:
        content = csv.reader(user_list)
        row_count = sum(1 for row in content)
        user_list.seek(0)
        if row_count == 0:
            headers = ["username", "password", "high score", "status"]
        else:
            headers = next(content)
        rows = []
        for line in content:
            rows.append({headers[0] : line[0], headers[1] : line[1], headers[2] : line[2], headers[3] : line[3]})
        return rows
    
def save_changes(users):
    feildnames = ["username", "password", "high score", "status"]
    with open("user_info.csv", "w", newline = "") as user_list:
        writer = csv.DictWriter(user_list, fieldnames = feildnames)
        writer.writeheader()
        writer.writerows(users)