import streamlit as st
import time
import math
from datetime import datetime

st.set_page_config(page_title="Nature Clock Pro", layout="wide")

# -----------------------------------------------------
# 🌄 REALISTIC ILLUSTRATED BACKGROUNDS (You can replace them)
# -----------------------------------------------------
BG_SUNNY = "https://i.imgur.com/R0BgbaN.jpeg"
BG_CLOUDY = "https://i.imgur.com/k8hrmH0.jpeg"
BG_RAINY  = "https://i.imgur.com/VXQ4Rh4.jpeg"
BG_NIGHT  = "https://i.imgur.com/8A2RtwU.jpeg"

# 🎵 Nature Sound (Replace if needed)
MUSIC_URL = "https://www2.cs.uic.edu/~i101/SoundFiles/Bird.wav"
st.audio(MUSIC_URL, autoplay=True)


# -----------------------------------------------------
# 🌤 WEATHER LOGIC (Auto-change every 15 seconds)
# -----------------------------------------------------
def get_weather():
    s = datetime.now().second
    if 0 <= s < 15:
        return "Sunny", BG_SUNNY
    elif 15 <= s < 30:
        return "Cloudy", BG_CLOUDY
    elif 30 <= s < 45:
        return "Rainy", BG_RAINY
    else:
        return "Night", BG_NIGHT


# -----------------------------------------------------
# BACKGROUND APPLY
# -----------------------------------------------------
def apply_background(img):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{img}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------
# 🕒 ANALOG CLOCK SVG (Your SVG exact output integrated)
# -----------------------------------------------------
def generate_clock():
    now = datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour % 12

    sec_angle = sec * 6
    min_angle = minute * 6
    hour_angle = hour * 30 + minute * 0.5

    # Dynamic hand coordinates
    hour_x = 165 + 70 * math.sin(math.radians(hour_angle))
    hour_y = 165 - 70 * math.cos(math.radians(hour_angle))

    min_x = 165 + 105 * math.sin(math.radians(min_angle))
    min_y = 165 - 105 * math.cos(math.radians(min_angle))

    sec_x = 165 + 130 * math.sin(math.radians(sec_angle))
    sec_y = 165 - 130 * math.cos(math.radians(sec_angle))

    svg = f"""
    <svg width="330" height="330">
        <!-- Hour Hand -->
        <line x1="165" y1="165"
              x2="{hour_x}"
              y2="{hour_y}"
              stroke="black" stroke-width="6" />

        <!-- Minute Hand -->
        <line x1="165" y1="165"
              x2="{min_x}"
              y2="{min_y}"
              stroke="black" stroke-width="4" />

        <!-- Second Hand -->
        <line x1="165" y1="165"
              x2="{sec_x}"
              y2="{sec_y}"
              stroke="red" stroke-width="2" />

        <circle cx="165" cy="165" r="6" fill="black" />
    </svg>
    """
    return svg


# -----------------------------------------------------
# 🧭 DIGITAL CLOCK
# -----------------------------------------------------
def digital_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    return (
        f"<div style='font-size:50px; font-weight:bold; text-align:center; color:white;'>"
        f"{now}</div>"
    )


# -----------------------------------------------------
# 🚀 MAIN LOOP
# -----------------------------------------------------
ui = st.empty()

while True:
    weather_name, bg = get_weather()
    apply_background(bg)

    with ui.container():
        st.markdown(
            f"""
            <h1 style="text-align:center; color:white; text-shadow:2px 2px 5px black;">
            🌿 Nature Clock Pro — {weather_name} Mode
            </h1>
            """,
            unsafe_allow_html=True,
        )

        # Digital Clock
        st.markdown(digital_clock(), unsafe_allow_html=True)

        # Analog Clock
        st.markdown(
            f"""
            <div style='text-align:center; margin-top:-10px;'>
                {generate_clock()}
            </div>
            """,
            unsafe_allow_html=True,
        )

    time.sleep(1)# -----------------------------------------------------
container = st.empty()

while True:
    weather, bg = get_weather_by_seconds()
    apply_background(bg)

    with container.container():
        st.markdown(
            f"""
            <h1 style='text-align:center; color:white; text-shadow:2px 2px 4px black;'>
                🌿 Nature Clock Pro — {weather.title()} Mode
            </h1>
            """,
            unsafe_allow_html=True,
        )

        # Digital Clock
        st.markdown(digital_clock(), unsafe_allow_html=True)

        # Analog Clock
        st.markdown(
            f"<div style='text-align:center;'>{analog_clock_svg()}</div>",
            unsafe_allow_html=True,
        )

    time.sleep(1)
