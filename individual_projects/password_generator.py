#DL 1st, password generator

import os
import msvcrt
import random

def menu(options, **mod):
    number = mod.get('accesed', [])
    toggle = mod.get('toggle', [])
    index = 0
    num = []
    for i in number:
        num.append([])
    while True:
        os.system('cls')
        for i, option in enumerate(options):
            prefix = "> " if i == index else "  "
            if toggle == True:
                if i in toggle:
                    print
            if number == True:
                if i in number:
                    print(prefix + option + ' <' + str(num) + '> (left/right arrow keys)')
                else:
                    print(prefix + option)
            else:
                    print(prefix + option)
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()
        if key == b"H":
            index = (index - 1) % len(options)
        elif key == b"P":
            index = (index + 1) % len(options)
        elif key == b"K":
            if index in number:
                if num[index] > 1:
                    num[index] -= 1
        elif key == b"M":
            if index in number:
                num[index] += 1
        elif key == b"\r":
            if number == True:
                if index in number:
                    return num[index]
            return index
        print(num)


def generate_password(requirments):
    password_len = requirments[0]
    lower_case = requirments[1] 
    upper_case = requirments[2] 
    numbers = requirments[3]
    special_chars = requirments[4]

    remaining_chars = password_len
    password_requirements = []

    password_outline = {}
    password = []

    if lower_case == True:
        password_outline.append[[1]]
        remaining_chars -= 1
        password_requirements.append[1]
    if upper_case == True:
        password_outline.append[[2]]
        remaining_chars -= 1
        password_requirements.append[2]
    if numbers == True:
        password_outline.append[[3]]
        remaining_chars -= 1
        password_requirements.append[3]
    if special_chars == True:
        password_outline.append[[4]]
        remaining_chars -= 1
        password_requirements.append[4]

    for i in range(remaining_chars):
        password_outline.append([random.choice([1,2,3,4])])

    for x in range password_outline:
        
        

    



def main():
    menu(["Generate Password", "Exit"])
    output = menu(["Password Length", "Lowercase", "Uppercase", "Numbers", "Special Characters", "Return"], number = [0], toggle = [1, 2, 3, 4])
main()