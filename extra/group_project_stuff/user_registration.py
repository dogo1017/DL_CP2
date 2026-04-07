import hashlib
import csv

def register(users,password,username):
    usernames = []
    for user in users:
        usernames.append(user["username"])
    password_encoded = password.encode("utf-8")
    hashed_password = hashlib.shake_128(password_encoded)
    hex_password = hashed_password.hexdigest(4)
    users.append({"username" : username, "password" : hex_password})
    return users

def load_csv():
    with open("extra/group_project_stuff/users.csv", "r") as user_list:
        content = csv.reader(user_list)
        row_count = sum(1 for row in content)
        user_list.seek(0)
        if row_count == 0:
            headers = ["username", "password"]
        else:
            headers = next(content)
        rows = []
        for line in content:
            rows.append({headers[0] : line[0], headers[1] : line[1]})
        return rows
    
def save_changes(users):
    feildnames = ["username", "password"]
    with open("extra/group_project_stuff/users.csv", "w", newline = "") as user_list:
        writer = csv.DictWriter(user_list, fieldnames = feildnames)
        writer.writeheader()
        writer.writerows(users)