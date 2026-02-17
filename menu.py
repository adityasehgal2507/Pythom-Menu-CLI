"""
Simple CLI Menu System
======================

Usage Example:
--------------
    from menu import Menu

    menu = Menu(title="My App")

    @menu.option  # Simple syntax
    def greet():
        '''Say hello'''
        print("Hello!")

    @menu.option("add", "plus", help="Add two numbers")  # With aliases
    def add_numbers():
        a = int(input("First number: "))
        b = int(input("Second number: "))
        print(f"Result: {a + b}")

    if __name__ == "__main__":
        menu.run()

Advanced Usage:
---------------
    # Auto-prompt for function arguments
    menu = Menu(ask_args=True)

    @menu.option
    def calculate(x: int, y: int = 10):
        '''Calculate sum'''
        print(f"Sum: {x + y}")
    
    # Clear screen between options
    menu = Menu(clear_screen=True)

    # Run once without looping
    menu.run(loop=False)

Features:
---------
- Select by number or name
- Prefix matching (typing "hel" matches "hello")
- Multiple aliases per option
- Type hints for auto-casting (int, bool, list, etc.)
- Built-in quit/exit command
- Optional argument prompting
- Works with or without parentheses: @menu.option or @menu.option()
"""

import inspect
import os
import sys


class Option:
    def __init__(self, func, names, help_text=None):
        self.func = func
        self.names = tuple(names)
        self.help = help_text or (func.__doc__ or "").strip()

    @property
    def primary(self):
        return self.names[0]


class Menu:
    def __init__(self, *, ask_args=False, title="Main Menu", clear_screen=False):
        self.ask_args = ask_args
        self.title = title
        self.clear_screen = clear_screen
        self._options = {}
        self._order = []
        self._register_builtin_quit()

    # ---------- public API ----------

    def option(self, *names, help=None):
        """Decorator to register a function as a menu option."""
        # Handle @menu.option (no parens)
        if len(names) == 1 and callable(names[0]) and help is None:
            func = names[0]
            return self.option()(func)
        
        # Handle @menu.option() or @menu.option("name")
        def decorator(func):
            option_names = names or (func.__name__,)
            opt = Option(func, option_names, help)

            for name in option_names:
                self._options[name.lower()] = opt

            if opt not in self._order:
                self._order.append(opt)

            return func
        return decorator

    def run(self, *, loop=True):
        """Run the menu loop."""
        while True:
            if self.clear_screen:
                os.system('clear' if os.name == 'posix' else 'cls')
            
            self._print_menu()
            choice = input("Choose option (number or name):\n> ").strip()

            if not choice:
                continue

            try:
                opt = self._resolve_choice(choice)
                if opt is None:
                    print("\n❌ Invalid choice. Try again.\n")
                    if not loop:
                        return
                    continue

                self._execute(opt)
                print()  # spacing after execution

            except (SystemExit, KeyboardInterrupt):
                print("\nExiting...")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                if not loop:
                    raise

    # ---------- internals ----------

    def _register_builtin_quit(self):
        """Register default quit option."""
        @self.option("quit", "exit", "q", help="Exit the program")
        def _quit():
            raise SystemExit

    def _resolve_choice(self, choice):
        """Match user input to an option by number, exact name, or prefix."""
        choice = choice.lower()

        # by number
        if choice.isdigit():
            idx = int(choice) - 1
            return self._order[idx] if 0 <= idx < len(self._order) else None

        # exact match
        if choice in self._options:
            return self._options[choice]

        # prefix match
        matches = {opt for name, opt in self._options.items() if name.startswith(choice)}
        
        if len(matches) == 1:
            return matches.pop()
        
        if len(matches) > 1:
            names = ', '.join(sorted(opt.primary for opt in matches))
            print(f"\n⚠️  Ambiguous: {names}")
        
        return None

    def _execute(self, opt):
        """Execute an option, prompting for args if needed."""
        if not self.ask_args:
            opt.func()
            return

        sig = inspect.signature(opt.func)
        kwargs = {}

        for name, param in sig.parameters.items():
            has_default = param.default is not inspect.Parameter.empty
            prompt = f"{name} [{param.default}]: " if has_default else f"{name}: "
            value = input(prompt).strip()

            if not value:
                if has_default:
                    continue
                raise ValueError(f"Missing required argument: {name}")

            kwargs[name] = self._cast(value, param.annotation)

        opt.func(**kwargs)

    def _cast(self, value, annotation):
        """Smart type casting with fallback."""
        if annotation is inspect.Parameter.empty:
            return value

        # handle booleans
        if annotation == bool:
            return value.lower() in ('true', 'yes', '1', 'y')
        
        # handle lists
        if annotation == list:
            return [item.strip() for item in value.split(',')]

        try:
            return annotation(value)
        except (ValueError, TypeError):
            return value

    def _print_menu(self):
        """Display the menu options."""
        print("\n" + "=" * 40)
        print(f"  {self.title}")
        print("=" * 40)
        
        for i, opt in enumerate(self._order, start=1):
            aliases = [n for n in opt.names if n != opt.primary]
            alias_text = f" ({', '.join(aliases)})" if aliases else ""
            desc = f" — {opt.help}" if opt.help else ""
            print(f"  {i}. {opt.primary}{alias_text}{desc}")
        
        print("=" * 40 + "\n")