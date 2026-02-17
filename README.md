# Simple CLI Menu System

A lightweight, decorator-based CLI menu framework for Python.

Build interactive command-line menus quickly using clean, Pythonic syntax — without boilerplate.

---

## ✨ Features

- Select options by **number or name**
- **Prefix matching** (`hel` matches `hello`)
- Multiple aliases per option
- Built-in `quit / exit` command
- Optional automatic argument prompting
- Type-hint-based input casting (`int`, `bool`, `list`, etc.)
- Optional screen clearing
- Works with or without decorator parentheses

---

## 🚀 Quick Example

```python
from menu import Menu

menu = Menu(title="My App")

@menu.option
def greet():
    """Say hello"""
    print("Hello!")

@menu.option("add", "plus", help="Add two numbers")
def add_numbers():
    a = int(input("First number: "))
    b = int(input("Second number: "))
    print(f"Result: {a + b}")

if __name__ == "__main__":
    menu.run()
```

---

## 🔧 Advanced Usage

### Auto-Prompt Function Arguments

```python
menu = Menu(ask_args=True)

@menu.option
def calculate(x: int, y: int = 10):
    """Calculate sum"""
    print(f"Sum: {x + y}")
```

Arguments are automatically prompted and cast using type hints.

---

### Clear Screen Between Runs

```python
menu = Menu(clear_screen=True)
```

---

### Run Once (No Loop)

```python
menu.run(loop=False)
```

---

## 🧠 Design Goals

- Minimal and dependency-free
- Clean decorator-based API
- Beginner-friendly
- Easily extensible

---
