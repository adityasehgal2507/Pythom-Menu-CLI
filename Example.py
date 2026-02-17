from menu import Menu, Option
import math
import os

menu = Menu(title="My App", ask_args=True)

@menu.option("hello", "hi", help="Say hello")
def greet():
    print("Hello!")

@menu.option("add", help="Add two numbers")
def add_numbers():
    a = int(input("First number: "))
    b = int(input("Second number: "))
    print(f"Result: {a + b}")

@menu.option
def Triangle(size: int = 5):
    for i in range(1, size+1):
        for j in range(i):
            print("*", end=' ')
        print()

@menu.option
def Square(size: int = 5):
    for i in range(size):
        if i in (0, size-1):
            print(" * " * size)
        else:
            print(f" * {"   " * (size-2)} * ")

@menu.option
def Circle(radius: int = 5):
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            dist = math.sqrt(i**2 + j**2)
            if radius - 0.5 <= dist <= radius + 0.5:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()
    pass

@menu.option("cls")
def clear():
    """Clear the screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

if __name__ == "__main__":
    menu.run()