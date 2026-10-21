from decimal import Decimal
import math
import re


def add(a, b):
    return a + b


def power(a, b):
    if a == 0 and b < 0:
        raise ZeroDivisionError("Cannot raise zero to a negative power.")
    if a < 0 and b != int(b):
        raise ValueError("Cannot raise a negative number to a fractional power.")
    return a ** b


def square_root(value):
    if value < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    if isinstance(value, Decimal):
        return value.sqrt()
    return math.sqrt(value)


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def reciprocal(value):
    return divide(1, value)


def evaluate_expression(expression):
    tokens = []
    position = 0
    token_pattern = re.compile(
        r"\s*([0-9]+(?:\.[0-9]*)?|\.[0-9]+|[()+\-*/^√])"
    )
    operator_aliases = {"−": "-", "×": "*", "÷": "/"}
    normalized_expression = expression.translate(
        str.maketrans(operator_aliases)
    )

    while position < len(normalized_expression):
        if not normalized_expression[position:].strip():
            break
        match = token_pattern.match(normalized_expression, position)
        if match is None:
            raise ValueError("Invalid expression.")
        tokens.append(match.group(1))
        position = match.end()

    if not tokens:
        raise ValueError("Enter an expression.")

    position = 0

    def parse_primary():
        nonlocal position
        if position >= len(tokens):
            raise ValueError("Incomplete expression.")
        token = tokens[position]
        if token == "√":
            position += 1
            return square_root(parse_primary())
        if token == "(":
            position += 1
            value = parse_expression()
            if position >= len(tokens) or tokens[position] != ")":
                raise ValueError("Unmatched opening parenthesis.")
            position += 1
            return value
        if token == ")" or token in {"+", "-", "*", "/", "^"}:
            raise ValueError("Expected a number or opening parenthesis.")
        position += 1
        return Decimal(token)

    def parse_power():
        nonlocal position
        value = parse_primary()
        if position < len(tokens) and tokens[position] == "^":
            position += 1
            value = power(value, parse_unary())
        return value

    def parse_unary():
        nonlocal position
        if position < len(tokens) and tokens[position] in {"+", "-"}:
            operator = tokens[position]
            position += 1
            value = parse_unary()
            return value if operator == "+" else -value
        return parse_power()

    def parse_term():
        nonlocal position
        value = parse_unary()
        while position < len(tokens) and tokens[position] in {"*", "/"}:
            operator = tokens[position]
            position += 1
            right = parse_unary()
            value = (
                multiply(value, right)
                if operator == "*"
                else divide(value, right)
            )
        return value

    def parse_expression():
        nonlocal position
        value = parse_term()
        while position < len(tokens) and tokens[position] in {"+", "-"}:
            operator = tokens[position]
            position += 1
            right = parse_term()
            value = add(value, right) if operator == "+" else subtract(value, right)
        return value

    result = parse_expression()
    if position != len(tokens):
        if tokens[position] == ")":
            raise ValueError("Unmatched closing parenthesis.")
        raise ValueError("Invalid expression.")
    return result


def get_number(prompt):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'q':
            return None
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def main():
    print("Simple Calculator")
    print("Operations: +, -, *, /, ^, √, expression (e)")
    print("Type 'q' at any prompt to quit.\n")

    while True:
        operation = input(
            "Choose an operation (+, -, *, /, ^, √, e): "
        ).strip()
        if operation.lower() == 'q':
            print("Goodbye!")
            break

        if operation.lower() == "e":
            expression = input("Enter an expression (q to quit): ").strip()
            if expression.lower() == "q":
                print("Goodbye!")
                break
            try:
                print(f"Result: {evaluate_expression(expression)}\n")
            except (ValueError, ZeroDivisionError) as error:
                print(f"{error}\n")
            continue

        if operation not in {"+", "-", "*", "/", "^", "√"}:
            print(
                "Invalid operation. Please choose one of: "
                "+, -, *, /, ^, √, e"
            )
            continue

        num1 = get_number("Enter first number: ")
        if num1 is None:
            print("Goodbye!")
            break

        num2 = None
        if operation != "√":
            num2 = get_number("Enter second number: ")
            if num2 is None:
                print("Goodbye!")
                break

        try:
            if operation == "+":
                result = add(num1, num2)
            elif operation == "-":
                result = subtract(num1, num2)
            elif operation == "*":
                result = multiply(num1, num2)
            elif operation == "^":
                result = power(num1, num2)
            elif operation == "√":
                result = square_root(num1)
            else:
                result = divide(num1, num2)

            print(f"Result: {result}\n")
        except ZeroDivisionError as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
