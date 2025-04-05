import streamlit as st
from collections import deque

# Conversion History (Session State)
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = deque(maxlen=5)

# Define conversion factors manually
conversion_factors = {
    "📏 Length": {
        "meter": 1,
        "kilometer": 1000,
        "mile": 1609.34,
        "foot": 0.3048,
        "inch": 0.0254
    },
    "⚖ Mass": {
        "gram": 1,
        "kilogram": 1000,
        "pound": 453.592,
        "tonne": 1_000_000
    },
    "⏳ Time": {
        "second": 1,
        "minute": 60,
        "hour": 3600,
        "day": 86400
    },
    "🌡 Temperature": {
        "celsius": "temp",
        "fahrenheit": "temp",
        "kelvin": "temp"
    },
    "🏋 Pressure": {
        "pascal": 1,
        "bar": 100000,
        "psi": 6894.76
    },
    "📐 Area": {
        "square meter": 1,
        "hectare": 10000,
        "acre": 4046.86,
        "square mile": 2.59e+6
    },
    "⚡ Energy": {
        "joule": 1,
        "calorie": 4.184,
        "kilowatt-hour": 3.6e+6
    },
    "🚀 Speed": {
        "meter/second": 1,
        "kilometer/hour": 0.277778,
        "mile/hour": 0.44704
    }
}

# Temperature conversion function
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "celsius":
        if to_unit == "fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "kelvin":
            return value + 273.15
    elif from_unit == "fahrenheit":
        if to_unit == "celsius":
            return (value - 32) * 5/9
        elif to_unit == "kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "kelvin":
        if to_unit == "celsius":
            return value - 273.15
        elif to_unit == "fahrenheit":
            return (value - 273.15) * 9/5 + 32
    return None

# Streamlit UI Setup
st.set_page_config(page_title="Smart Converter 🌎", layout="wide")
st.sidebar.title("⭐ Navigator")
page = st.sidebar.radio("Select a section", ["Unit Converter", "Conversion History"])

# Unit Converter Page
if page == "Unit Converter":
    st.title("🔄 Unit Converter")
    category = st.selectbox("📌 Select a Category", list(conversion_factors.keys()))
    units = list(conversion_factors[category].keys())

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("Convert From:", units)
    with col2:
        to_unit = st.selectbox("Convert To:", units)

    value = st.number_input("🔢 Enter Value:", min_value=0.0, format="%.10g")

    if st.button("Convert"):
        result = None
        if category == "🌡 Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            base = conversion_factors[category][from_unit]
            target = conversion_factors[category][to_unit]
            result = value * base / target

        if result is not None:
            formatted_result = "{:.0f}".format(result) if result.is_integer() else "{:.4f}".format(result).rstrip('0').rstrip('.')
            result_text = f"{value} {from_unit} = {formatted_result} {to_unit}"
            st.success(result_text)
            st.session_state.conversion_history.appendleft(result_text)
        else:
            st.error("Invalid conversion! Check units.")

# Conversion History Page
elif page == "Conversion History":
    st.title("📜 History")
    if st.session_state.conversion_history:
        for entry in list(st.session_state.conversion_history):
            st.write(entry)
    else:
        st.info("No conversions yet. Start converting!")
