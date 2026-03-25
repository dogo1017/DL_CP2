#DL inputs.py


# Keeps asking the user for a positive number until they enter one
# If the user types 'r', returns None so the caller knows to cancel
def get_positive_float(prompt):
    while True:
        user_inp = input(prompt)
        if user_inp.strip().lower() == 'r':
            return None
        try:
            val = float(user_inp)
            if val <= 0:
                print("Please enter a positive number.")
                continue
            return val
        except ValueError:
            print(f"'{user_inp}' is not a valid number.")


# Keeps asking the user for input until they enter one of the valid choices
# Returns the choice as a string once a valid one is entered
def get_menu_choice(prompt, valid_choices):
    while True:
        user_inp = input(prompt).strip()
        if user_inp in valid_choices:
            return user_inp
        print(f"Please enter one of: {', '.join(valid_choices)}")