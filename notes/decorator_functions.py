def decorator(func):
    def wrapper():
        print("Before calling the function.")
        func()
        print("After calling a function.")
    return wrapper

@decorator
def greet():
    print("Hello, World")
    
greet()