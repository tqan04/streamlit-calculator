from decimal import Decimal, InvalidOperation

import streamlit as st

from calculator import (
    add,
    divide,
    evaluate_expression,
    multiply,
    power,
    square_root,
    subtract,
)


OPERATIONS = {
    "+": add,
    "−": subtract,
    "×": multiply,
    "÷": divide,
    "^": power,
}
KEYPAD = (
    ("AC", "⌫", "(", ")"),
    ("√", "^", "%", "÷"),
    ("7", "8", "9", "×"),
    ("4", "5", "6", "−"),
    ("1", "2", "3", "+"),
    ("±", "0", "."),
)


def format_number(value: Decimal) -> str:
    if value == value.to_integral_value():
        return format(value, "f")
    return format(value.normalize(), "f")


def apply_operation(left: Decimal, operator: str, right: Decimal) -> Decimal:
    return OPERATIONS[operator](left, right)


def is_number_token(token: str) -> bool:
    try:
        Decimal(token)
        return True
    except InvalidOperation:
        return False


def update_expression(state) -> None:
    state.expression = " ".join(state.tokens)


def press_key(key: str) -> None:
    state = st.session_state
    state.error = ""

    if key == "AC":
        state.display = "0"
        state.expression = ""
        state.start_new = True
        state.repeat_operator = None
        state.repeat_operand = None
        state.tokens = []
        return

    if key == "⌫":
        if state.tokens:
            if not state.start_new and is_number_token(state.tokens[-1]):
                shortened = state.tokens[-1][:-1]
                state.tokens[-1] = (
                    shortened if shortened not in ("", "-") else "0"
                )
                state.display = state.tokens[-1]
                state.start_new = False
            else:
                state.tokens.pop()
                state.start_new = not (
                    state.tokens and is_number_token(state.tokens[-1])
                )
                if not state.start_new:
                    state.display = state.tokens[-1]
            update_expression(state)
        elif state.display != "0":
            shortened = state.display[:-1]
            state.display = shortened if shortened not in ("", "-") else "0"
            state.start_new = False
            state.repeat_operator = None
            state.repeat_operand = None
        return

    if key in "0123456789.":
        if state.start_new:
            if state.tokens and state.tokens[-1] == ")":
                state.tokens.append("×")
            value = "0." if key == "." else key
            state.tokens.append(value)
            state.start_new = False
        elif state.tokens and is_number_token(state.tokens[-1]):
            value = state.tokens[-1]
            if key == ".":
                if "." not in value:
                    state.tokens[-1] += "."
            elif value in ("0", "-0"):
                state.tokens[-1] = key if value == "0" else f"-{key}"
            elif len(value) < 16:
                state.tokens[-1] += key
        else:
            value = "0." if key == "." else key
            state.tokens.append(value)
        state.display = state.tokens[-1]
        update_expression(state)
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "±":
        if state.tokens and not state.start_new and is_number_token(state.tokens[-1]):
            value = state.tokens[-1]
            if value.startswith("-"):
                state.tokens[-1] = value[1:]
            else:
                state.tokens[-1] = f"-{value}"
            state.display = state.tokens[-1]
        elif state.tokens and state.tokens[-1] in ("(", "+", "−", "×", "÷", "^"):
            state.tokens.append("−")
            state.start_new = True
        else:
            state.display = (
                state.display[1:]
                if state.display.startswith("-")
                else f"-{state.display}"
            )
            state.tokens = [state.display]
            state.start_new = False
        update_expression(state)
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "%":
        has_current_operand = (
            state.tokens and is_number_token(state.tokens[-1])
        )
        value = (
            Decimal(state.tokens[-1])
            if has_current_operand
            else Decimal(state.display)
        )
        if (
            len(state.tokens) >= 3
            and state.tokens[-2] in ("+", "−")
            and is_number_token(state.tokens[-3])
        ):
            value = Decimal(state.tokens[-3]) * value / Decimal(100)
        else:
            value /= Decimal(100)
        state.display = format_number(value)
        if has_current_operand:
            state.tokens[-1] = state.display
        elif state.tokens and state.tokens[-1] in ("+", "−", "×", "÷", "^"):
            state.tokens.append(state.display)
        else:
            state.tokens = [state.display]
        update_expression(state)
        state.start_new = False
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "√":
        try:
            if state.tokens and is_number_token(state.tokens[-1]):
                value = Decimal(state.tokens[-1])
            elif not state.tokens:
                value = Decimal(state.display)
            else:
                state.error = "Enter a number before taking the square root."
                return
            result = square_root(value)
            if state.tokens and is_number_token(state.tokens[-1]):
                state.tokens.pop()
            state.tokens.extend(("√", "(", format_number(value), ")"))
            state.display = format_number(result)
            update_expression(state)
            state.start_new = True
            state.repeat_operator = None
            state.repeat_operand = None
        except ValueError as error:
            state.error = str(error)
        return

    if key in OPERATIONS:
        if not state.tokens:
            state.tokens.append(state.display)
        if state.tokens[-1] == "(":
            if key == "−":
                state.tokens.append(key)
            else:
                state.error = "Enter a number before choosing an operation."
                return
        elif state.tokens[-1] in ("+", "−", "×", "÷", "^"):
            if (
                state.tokens[-1] == "−"
                and len(state.tokens) > 1
                and state.tokens[-2] == "("
            ):
                if key != "−":
                    state.error = "Enter a number after the opening parenthesis."
                    return
            else:
                state.tokens[-1] = key
        elif is_number_token(state.tokens[-1]) or state.tokens[-1] == ")":
            state.tokens.append(key)
        update_expression(state)
        state.start_new = True
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "(":
        if state.tokens and (
            is_number_token(state.tokens[-1]) or state.tokens[-1] == ")"
        ):
            state.tokens.append("×")
        state.tokens.append("(")
        update_expression(state)
        state.start_new = True
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == ")":
        if (
            state.tokens
            and state.tokens[-1] not in ("(", "+", "−", "×", "÷", "^")
            and state.tokens.count("(") > state.tokens.count(")")
        ):
            state.tokens.append(")")
            update_expression(state)
            state.start_new = True
        elif state.tokens.count("(") <= state.tokens.count(")"):
            state.error = "There is no unmatched opening parenthesis."
        else:
            state.error = "Enter a number before closing the parenthesis."
        return

    if key == "=":
        try:
            if state.tokens:
                expression = " ".join(state.tokens)
                result = evaluate_expression(expression)
                state.expression = f"{expression} ="
                state.history.insert(
                    0,
                    f"{state.expression} {format_number(result)}",
                )
                state.history = state.history[:10]
                if (
                    len(state.tokens) == 3
                    and state.tokens[1] in OPERATIONS
                    and is_number_token(state.tokens[0])
                    and is_number_token(state.tokens[2])
                ):
                    state.repeat_operator = state.tokens[1]
                    state.repeat_operand = Decimal(state.tokens[2])
                else:
                    state.repeat_operator = None
                    state.repeat_operand = None
                state.display = format_number(result)
                state.tokens = []
                state.start_new = True
            elif state.repeat_operator is not None:
                left = Decimal(state.display)
                result = apply_operation(
                    left, state.repeat_operator, state.repeat_operand
                )
                state.expression = (
                    f"{format_number(left)} {state.repeat_operator} "
                    f"{format_number(state.repeat_operand)} ="
                )
                state.history.insert(
                    0,
                    f"{state.expression} {format_number(result)}",
                )
                state.history = state.history[:10]
                state.display = format_number(result)
                state.start_new = True
        except ZeroDivisionError:
            state.error = "Cannot divide by zero."
        except ValueError as error:
            state.error = str(error)


st.set_page_config(page_title="Calculator", page_icon="🧮")

st.session_state.setdefault("display", "0")
st.session_state.setdefault("expression", "")
st.session_state.setdefault("start_new", True)
st.session_state.setdefault("repeat_operator", None)
st.session_state.setdefault("repeat_operand", None)
st.session_state.setdefault("history", [])
st.session_state.setdefault("error", "")
st.session_state.setdefault("tokens", [])

st.html(
    """
    <style>
    .st-key-calculator_keypad button {
        box-shadow: 0 4px 0 rgba(0, 0, 0, 0.32);
        transition: transform 100ms ease, box-shadow 100ms ease;
    }

    .st-key-calculator_keypad button:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 5px 0 rgba(0, 0, 0, 0.32),
            0 7px 12px rgba(0, 0, 0, 0.14);
    }

    .st-key-calculator_keypad button:active:not(:disabled) {
        transform: translateY(3px);
        box-shadow: 0 1px 0 rgba(0, 0, 0, 0.32);
    }
    </style>
    """
)

with st.container(horizontal=True, horizontal_alignment="center"):
    with st.container(width=420):
        st.title("Calculator")
        st.caption("A simple everyday calculator")

        with st.container(border=True, height=160):
            st.caption(st.session_state.expression or " ")
            st.metric("Display", st.session_state.display)

        if st.session_state.error:
            st.error(st.session_state.error)

        with st.container(key="calculator_keypad"):
            with st.container(horizontal=True, horizontal_alignment="distribute"):
                for column_index, key in enumerate(KEYPAD[0]):
                    st.button(
                        key,
                        key=f"key_0_{column_index}",
                        type="secondary",
                        width="stretch",
                        on_click=press_key,
                        args=(key,),
                    )

            for row_index, row in enumerate(KEYPAD[1:], start=1):
                columns = st.columns(len(row))
                for column_index, key in enumerate(row):
                    columns[column_index].button(
                        key,
                        key=f"key_{row_index}_{column_index}",
                        type="secondary",
                        width="stretch",
                        on_click=press_key,
                        args=(key,),
                    )

            equals_columns = st.columns(4)
            equals_columns[3].button(
                "=",
                key="key_equals",
                type="primary",
                width="stretch",
                on_click=press_key,
                args=("=",),
            )

        if st.session_state.history:
            with st.expander("History"):
                for calculation in st.session_state.history:
                    st.text(calculation)
