# Simple CLI Menu System

A lightweight, decorator-based command-line menu framework for Python.

This project provides a clean, extensible way to build interactive CLI menus with minimal boilerplate. It leverages decorators, function introspection, and type hints to simplify command registration and argument handling.

---

## Features

- Selection by number or name
- Prefix-based command matching
- Multiple aliases per option
- Built-in quit/exit command
- Optional automatic argument prompting
- Type-hint-based input casting (e.g., `int`, `bool`, `list`)
- Optional screen clearing between runs
- Supports both `@menu.option` and `@menu.option()`

---

## Example

```python
from menu import Menu

menu = Menu(title="My Application")

@menu.option
def greet():
    """Display a greeting."""
    print("Hello.")

@menu.option("add", "plus", help="Add two numbers")
def add_numbers():
    a = int(input("First number: "))
    b = int(input("Second number: "))
    print(f"Result: {a + b}")

if __name__ == "__main__":
    menu.run()
```

---

## Advanced Usage

### Automatic Argument Prompting

```python
menu = Menu(ask_args=True)

@menu.option
def calculate(x: int, y: int = 10):
    """Calculate sum."""
    print(f"Sum: {x + y}")
```

Arguments are prompted automatically and cast based on type annotations.

### Run Once (Disable Loop)

```python
menu.run(loop=False)
```

---

## Design Principles

- Minimal and dependency-free
- Explicit, readable API
- Extensible architecture
- Suitable for small tools and internal utilities

---

## License

MIT License
