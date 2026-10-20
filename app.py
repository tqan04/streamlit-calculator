from decimal import Decimal

import streamlit as st

from calculator import add, divide, multiply, subtract


OPERATIONS = {
    "+": add,
    "−": subtract,
    "×": multiply,
    "÷": divide,
}
KEYPAD = (
    ("AC", "⌫", "%", "÷"),
    ("7", "8", "9", "×"),
    ("4", "5", "6", "−"),
    ("1", "2", "3", "+"),
    ("±", "0", ".", "="),
)


def format_number(value: Decimal) -> str:
    if value == value.to_integral_value():
        return format(value, "f")
    return format(value.normalize(), "f")


def apply_operation(left: Decimal, operator: str, right: Decimal) -> Decimal:
    return OPERATIONS[operator](left, right)


def press_key(key: str) -> None:
    state = st.session_state
    state.error = ""

    if key == "AC":
        state.display = "0"
        state.accumulator = None
        state.operator = None
        state.expression = ""
        state.start_new = True
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "⌫":
        if not state.start_new or (
            state.operator is None and state.display != "0"
        ):
            shortened = state.display[:-1]
            state.display = shortened if shortened not in ("", "-") else "0"
            state.start_new = False
            state.repeat_operator = None
            state.repeat_operand = None
        return

    if key in "0123456789.":
        if state.start_new:
            state.display = "0." if key == "." else key
            state.start_new = False
        elif key == ".":
            if "." not in state.display:
                state.display += "."
        elif state.display in ("0", "-0"):
            state.display = key if state.display == "0" else f"-{key}"
        elif len(state.display) < 16:
            state.display += key
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "±":
        if state.display.startswith("-"):
            state.display = state.display[1:]
        else:
            state.display = f"-{state.display}"
        state.start_new = False
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key == "%":
        value = Decimal(state.display)
        if state.operator in ("+", "−") and state.accumulator is not None:
            value = state.accumulator * value / Decimal(100)
        else:
            value /= Decimal(100)
        state.display = format_number(value)
        state.start_new = False
        state.repeat_operator = None
        state.repeat_operand = None
        return

    if key in OPERATIONS:
        try:
            if state.operator is not None and not state.start_new:
                result = apply_operation(
                    state.accumulator, state.operator, Decimal(state.display)
                )
                state.display = format_number(result)
                state.accumulator = result
            else:
                state.accumulator = Decimal(state.display)
            state.operator = key
            state.expression = f"{format_number(state.accumulator)} {key}"
            state.start_new = True
            state.repeat_operator = None
            state.repeat_operand = None
        except ZeroDivisionError:
            state.error = "Cannot divide by zero."
        return

    if key == "=":
        try:
            if state.operator is not None:
                left = state.accumulator
                right = Decimal(state.display)
                operator = state.operator
                result = apply_operation(left, operator, right)
                state.expression = (
                    f"{format_number(left)} {operator} "
                    f"{format_number(right)} ="
                )
                state.history.insert(
                    0,
                    f"{state.expression} {format_number(result)}",
                )
                state.history = state.history[:10]
                state.repeat_operator = operator
                state.repeat_operand = right
                state.display = format_number(result)
                state.accumulator = None
                state.operator = None
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


st.set_page_config(page_title="Calculator", page_icon="🧮")

st.session_state.setdefault("display", "0")
st.session_state.setdefault("accumulator", None)
st.session_state.setdefault("operator", None)
st.session_state.setdefault("expression", "")
st.session_state.setdefault("start_new", True)
st.session_state.setdefault("repeat_operator", None)
st.session_state.setdefault("repeat_operand", None)
st.session_state.setdefault("history", [])
st.session_state.setdefault("error", "")

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
            for row_index, row in enumerate(KEYPAD):
                columns = st.columns(4)
                for column_index, key in enumerate(row):
                    button_type = "primary" if key == "=" else "secondary"
                    columns[column_index].button(
                        key,
                        key=f"key_{row_index}_{column_index}",
                        type=button_type,
                        width="stretch",
                        on_click=press_key,
                        args=(key,),
                    )

        if st.session_state.history:
            with st.expander("History"):
                for calculation in st.session_state.history:
                    st.text(calculation)
