from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


def test_reciprocal_updates_expression_and_is_recorded_in_history():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = "4"
    app.session_state["tokens"] = ["4"]
    app.session_state["start_new"] = False
    app.run()

    app.button(key="key_2_3").click().run()

    assert app.session_state["display"] == "0.25"
    assert app.session_state["expression"] == "( 1 ÷ ( 4 ) )"
    assert app.session_state["tokens"] == ["(", "1", "÷", "(", "4", ")", ")"]

    app.button(key="key_equals").click().run()

    assert app.session_state["display"] == "0.25"
    assert app.session_state["history"] == ["( 1 ÷ ( 4 ) ) = 0.25"]


def test_reciprocal_of_zero_shows_error_without_changing_calculator_state():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = "0"
    app.session_state["expression"] = "0"
    app.session_state["tokens"] = ["0"]
    app.session_state["start_new"] = False
    app.session_state["history"] = ["previous calculation"]
    app.run()

    app.button(key="key_2_3").click().run()

    assert app.session_state["display"] == "0"
    assert app.session_state["expression"] == "0"
    assert app.session_state["tokens"] == ["0"]
    assert app.session_state["history"] == ["previous calculation"]
    assert app.session_state["error"] == "Cannot divide by zero."


def test_reciprocal_uses_a_parenthesized_current_operand():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = "4"
    app.session_state["tokens"] = ["(", "2", "+", "2", ")"]
    app.session_state["start_new"] = True
    app.run()

    app.button(key="key_2_3").click().run()

    assert app.session_state["display"] == "0.25"
    assert app.session_state["expression"] == "( 1 ÷ ( ( 2 + 2 ) ) )"

    app.button(key="key_equals").click().run()

    assert app.session_state["history"] == [
        "( 1 ÷ ( ( 2 + 2 ) ) ) = 0.25"
    ]


def test_reciprocal_after_power_keeps_the_reciprocal_grouped():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = "3"
    app.session_state["tokens"] = ["2", "^", "3"]
    app.session_state["start_new"] = False
    app.run()

    app.button(key="key_2_3").click().run()

    assert app.session_state["display"] == "0.3333333333333333333333333333"
    assert app.session_state["expression"] == "2 ^ ( 1 ÷ ( 3 ) )"

    app.button(key="key_equals").click().run()

    assert float(app.session_state["display"]) == pytest.approx(2 ** (1 / 3))
    assert app.session_state["history"] == [
        "2 ^ ( 1 ÷ ( 3 ) ) = " + app.session_state["display"]
    ]


def test_reciprocal_twice_returns_original_value():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = "4"
    app.session_state["tokens"] = ["4"]
    app.session_state["start_new"] = False
    app.run()

    app.button(key="key_2_3").click().run()
    app.button(key="key_2_3").click().run()

    assert app.session_state["display"] == "4"
    assert app.session_state["expression"] == "( 1 ÷ ( ( 1 ÷ ( 4 ) ) ) )"

    app.button(key="key_equals").click().run()

    assert app.session_state["display"] == "4"
    assert app.session_state["history"] == [
        "( 1 ÷ ( ( 1 ÷ ( 4 ) ) ) ) = 4"
    ]


@pytest.mark.parametrize(
    ("display", "tokens", "expected"),
    [("5", ["5"], "120"), ("0", ["0"], "1")],
)
def test_factorial_updates_expression_and_is_recorded_in_history(
    display, tokens, expected
):
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = display
    app.session_state["tokens"] = tokens
    app.session_state["start_new"] = False
    app.run()

    app.button(key="key_1_2").click().run()

    assert app.session_state["display"] == expected
    assert app.session_state["expression"] == f"( {display} ) !"
    assert app.session_state["tokens"] == ["(", display, ")", "!"]

    app.button(key="key_equals").click().run()

    assert app.session_state["display"] == expected
    assert app.session_state["history"] == [
        f"( {display} ) ! = {expected}"
    ]


def test_factorial_applies_to_the_current_parenthesized_operand():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = "3"
    app.session_state["tokens"] = ["2", "+", "(", "2", "+", "3", ")"]
    app.session_state["start_new"] = True
    app.run()

    app.button(key="key_1_2").click().run()

    assert app.session_state["display"] == "120"
    assert app.session_state["expression"] == "2 + ( ( 2 + 3 ) ) !"

    app.button(key="key_equals").click().run()

    assert app.session_state["history"] == [
        "2 + ( ( 2 + 3 ) ) ! = 122"
    ]


@pytest.mark.parametrize(
    ("display", "tokens"),
    [("-5", ["-5"]), ("2.5", ["2.5"])],
)
def test_invalid_factorial_shows_error_without_changing_calculator_state(
    display, tokens
):
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.session_state["display"] = display
    app.session_state["expression"] = display
    app.session_state["tokens"] = tokens
    app.session_state["start_new"] = False
    app.session_state["history"] = ["previous calculation"]
    app.run()

    app.button(key="key_1_2").click().run()

    assert app.session_state["display"] == display
    assert app.session_state["expression"] == display
    assert app.session_state["tokens"] == tokens
    assert app.session_state["history"] == ["previous calculation"]
    assert app.session_state["error"] == (
        "Factorial is only defined for non-negative integers."
    )


def test_operator_buttons_share_the_same_size_and_right_edge_column():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py").run()

    # All keypad rows use five equal-width columns, with each operator at the
    # far-right column.
    for key, label in (
        ("key_1_4", "÷"),
        ("key_2_4", "×"),
        ("key_3_4", "−"),
        ("key_4_4", "+"),
    ):
        assert app.button(key=key).label == label

    assert app.button(key="key_1_3").label == "%"
    assert app.button(key="key_2_3").label == "1/x"
    assert app.button(key="key_5_1").label == "."
