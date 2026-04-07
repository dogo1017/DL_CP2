# login.py

import hashlib
import user_registration
import os

# Function for logging in
def log_in(username,password):
    information = user_registration.load_csv()
    mixer = hashlib.shake_128()
    mixer.update(password.encode('utf-8'))
    f_password = str(mixer.hexdigest(4))
    correct = False
    for i in information:
        if f_password == i["password"]:
            return True
        else:
            return False