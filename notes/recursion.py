import sys

import colorama
from colorama import Fore, Style

# Initialize Colorama (optional, but helpful for compatibility)
colorama.init(autoreset=True) 

for num in range(1,11):
    if num % 2 == 0:
        print(num)

even = []
sys.set_int_max_str_digits(1000000000)
num = 30000000
sum = 1

for x in range(1, num + 1):
    sum *= x
    for char in str(sum):
        if char == 0:
            print(Fore.BLUE + 0)
        elif char == 1:
            print(Fore.RED + 1)
        elif char == 2:
            print(Fore.YELLOW + 2)
        elif char == 3:
            print(Fore.GREEN + 3)
        elif char == 4:
            print(Fore.BLUE + 4)
        elif char == 5:
            print(Fore.BLUE + 5,end='')
        elif char == 6:
            print(Fore.BLUE + 6,end='')
        elif char == 7:
            print(Fore.BLUE + 7,end='')
        elif char == 8:
            print(Fore.BLUE + 8,end='')
        elif char == 9:
            print(Fore.BLUE + 9, end='')
    print("\n"*4)


def factorial(n):
    if n == 1: return 1
    return n * factorial(n-1)


print(f"Recursion: {factorial(num)}")


fib = [1,1]

for i in range(1,11):
    fib.append(fib[i-1] + fib[i])

print(f"loop: {fib}")


numbers = []
def fibonacci(n):
    numbers.append(n)
    if n == 2: 
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

fibonacci(10)

print(f"Recursion: {numbers}")