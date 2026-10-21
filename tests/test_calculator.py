from decimal import Decimal

import pytest

from calculator import evaluate_expression, factorial, reciprocal


@pytest.mark.parametrize(
    ("value", "expected"),
    [(Decimal("4"), Decimal("0.25")), (Decimal("-2"), Decimal("-0.5"))],
)
def test_reciprocal(value, expected):
    assert reciprocal(value) == expected


def test_reciprocal_of_zero_raises_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        reciprocal(Decimal("0"))


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Decimal("5"), Decimal("120")),
        (Decimal("0"), Decimal("1")),
        (Decimal("5.0"), Decimal("120")),
    ],
)
def test_factorial(value, expected):
    assert factorial(value) == expected


@pytest.mark.parametrize("value", [Decimal("-1"), Decimal("2.5")])
def test_factorial_rejects_negative_and_non_integer_values(value):
    with pytest.raises(
        ValueError, match="Factorial is only defined for non-negative integers"
    ):
        factorial(value)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("5!", Decimal("120")),
        ("0!", Decimal("1")),
        ("5.0!", Decimal("120")),
        ("(2 + 3)!", Decimal("120")),
    ],
)
def test_evaluate_expression_with_factorial(expression, expected):
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize("expression", ["(-5)!", "2.5!"])
def test_evaluate_expression_rejects_invalid_factorials(expression):
    with pytest.raises(ValueError, match="Factorial is only defined"):
        evaluate_expression(expression)
