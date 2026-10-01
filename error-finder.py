import ast
import sys


def find_errors(code):
    errors = []

    # Check syntax errors
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append({
            "type": "SyntaxError",
            "line": e.lineno,
            "message": e.msg,
            "suggestion": "Check brackets, quotes, indentation, and Python syntax."
        })
        return errors

    lines = code.splitlines()

    # Check some common problems
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Old Python print syntax
        if stripped.startswith("print ") and not stripped.startswith("print("):
            errors.append({
                "type": "Possible Syntax Issue",
                "line": number,
                "message": "Old-style print syntax detected.",
                "suggestion": "Use print(...) in Python 3."
            })

        # input() returns string
        if "input(" in stripped and "int(input(" not in stripped:
            errors.append({
                "type": "Possible Type Issue",
                "line": number,
                "message": "input() returns a string.",
                "suggestion": "Use int(input(...)) or float(input(...)) if you need a number."
            })

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python error_finder.py your_file.py")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    errors = find_errors(code)

    if not errors:
        print("No common errors found.")
        return

    print(f"Found {len(errors)} possible issue(s):\n")

    for error in errors:
        print(f"[{error['type']}] Line {error['line']}")
        print(f"Problem: {error['message']}")
        print(f"Suggestion: {error['suggestion']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
