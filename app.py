import streamlit as st
import requests
import json
from pint import UnitRegistry
from collections import deque

# Initialize Unit Registry
ureg = UnitRegistry()

# Conversion History (Session State)
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = deque(maxlen=5)

# Unit Categories with Icons
unit_categories = {
    "📏 Length": ["meter", "kilometer", "mile", "foot", "inch"],
    "⚖ Mass": ["gram", "kilogram", "pound", "tonne"],
    "⏳ Time": ["second", "minute", "hour", "day"],
    "🌡 Temperature": ["celsius", "fahrenheit", "kelvin"],
    "🏋 Pressure": ["pascal", "bar", "psi"],
    "📐 Area": ["square meter", "hectare", "acre", "square mile"],
    "⚡ Energy": ["joule", "calorie", "kilowatt-hour"],
    "🚀 Speed": ["meter/second", "kilometer/hour", "mile/hour"],
}

# Streamlit UI Setup
st.set_page_config(page_title="Smart Converter 🌎", layout="wide")
st.sidebar.title("⭐ Navigator")
page = st.sidebar.radio("Select a section", ["Unit Converter", "Conversion History"])

# Conversion Function
def convert_units(value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        formatted_result = "{:.0f}".format(result.magnitude) if result.magnitude.is_integer() else "{:.4f}".format(result.magnitude).rstrip('0').rstrip('.')
        return result.magnitude, f"{value} {from_unit} = {formatted_result} {to_unit}"
    except Exception:
        return None, "Invalid conversion! Check units."

# Unit Converter Page
if page == "Unit Converter":
    st.title("🔄 Unit Converter")
    category = st.selectbox("📌 Select a Category", list(unit_categories.keys()))
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("Convert From:", unit_categories[category])
    with col2:
        to_unit = st.selectbox("Convert To:", unit_categories[category])
    value = st.number_input("🔢 Enter Value:", min_value=0.0, format="%.10g")
    if st.button("Convert"):
        converted_value, result_text = convert_units(value, from_unit, to_unit)
        if converted_value is not None:
            st.success(result_text)
            st.session_state.conversion_history.appendleft(result_text)
        else:
            st.error(result_text)

# Conversion History Page
elif page == "Conversion History":
    st.title("📜 History")
    if st.session_state.conversion_history:
        for entry in list(st.session_state.conversion_history):
            st.write(entry)
    else:
        st.info("No conversions yet. Start converting!")