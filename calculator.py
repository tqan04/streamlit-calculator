from decimal import Decimal
import math


def add(a, b):
    return a + b


def power(a, b):
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
    print("Operations: +, -, *, /, ^, √")
    print("Type 'q' at any prompt to quit.\n")

    while True:
        operation = input("Choose an operation (+, -, *, /, ^, √): ").strip()
        if operation.lower() == 'q':
            print("Goodbye!")
            break

        if operation not in {"+", "-", "*", "/", "^", "√"}:
            print("Invalid operation. Please choose one of: +, -, *, /, ^, √")
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
