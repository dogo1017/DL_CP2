#DL 1st, password generator

import os
import msvcrt

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


def main():
    menu(["Generate Password", "Exit"])
    output = menu(["Password Length", "Lowercase", "Uppercase", "Numbers", "Special Characters", "Return"], number = [0], toggle = [1, 2, 3, 4])
main()