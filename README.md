# Streamlit Calculator

A simple keypad-style calculator built with Python and Streamlit.

## Features

- Addition, subtraction, multiplication, and division
- Percentage, sign change, clear, and backspace
- Repeated equals and recent calculation history
- Light and dark appearance modes
- Ocean, forest, sunset, and rose theme presets

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser.

## Themes

Use Streamlit's settings menu to switch between the default light and dark
appearances. To use a named preset, copy its config before starting the app:

```bash
cp .streamlit/themes/ocean.toml .streamlit/config.toml
streamlit run app.py
```

Replace `ocean.toml` with `forest.toml`, `sunset.toml`, or `rose.toml` to try
another palette. Restore the default dual-mode theme by restarting with the
dual-mode config from this repository.
