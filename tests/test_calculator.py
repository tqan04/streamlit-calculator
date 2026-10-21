from decimal import Decimal

import pytest

from calculator import reciprocal


@pytest.mark.parametrize(
    ("value", "expected"),
    [(Decimal("4"), Decimal("0.25")), (Decimal("-2"), Decimal("-0.5"))],
)
def test_reciprocal(value, expected):
    assert reciprocal(value) == expected


def test_reciprocal_of_zero_raises_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        reciprocal(Decimal("0"))
