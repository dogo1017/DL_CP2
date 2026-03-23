def menu_input(message, valid_inps):
    while True:
        user_inp = input(message)
        if user_inp not in valid_inps:
            continue
        else:
            return user_inp