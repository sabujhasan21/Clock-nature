import streamlit as st
import time
import math
import random
from datetime import datetime

st.set_page_config(page_title="Nature Clock Pro", layout="wide")

# -----------------------------------------------------
# 🎨 CUSTOM REALISTIC ILLUSTRATION BACKGROUNDS
# (You can replace these with your own image URLs)
# -----------------------------------------------------
BG_SUNNY = "https://i.imgur.com/R0BgbaN.jpeg"
BG_CLOUDY = "https://i.imgur.com/k8hrmH0.jpeg"
BG_RAINY  = "https://i.imgur.com/VXQ4Rh4.jpeg"
BG_NIGHT  = "https://i.imgur.com/8A2RtwU.jpeg"

# -----------------------------------------------------
# 🎵 MUSIC / SOUND EFFECTS
# -----------------------------------------------------
MUSIC_URL = "https://www2.cs.uic.edu/~i101/SoundFiles/Bird.wav"

st.audio(MUSIC_URL, autoplay=True)

# -----------------------------------------------------
# 🌤 WEATHER SIMULATION (auto changes every 15 seconds)
# -----------------------------------------------------
def get_weather_by_seconds():
    s = datetime.now().second

    if 0 <= s < 15:
        return "sunny", BG_SUNNY
    elif 15 <= s < 30:
        return "cloudy", BG_CLOUDY
    elif 30 <= s < 45:
        return "rainy", BG_RAINY
    else:
        return "night", BG_NIGHT

# -----------------------------------------------------
# 🌄 APPLY BACKGROUND IMAGE
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
# 🕒 ANALOG CLOCK SVG
# -----------------------------------------------------
def analog_clock_svg():
    now = datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour % 12

    sec_angle = sec * 6
    min_angle = minute * 6
    hour_angle = hour * 30 + minute * 0.5

    svg = f"""
    <svg width="330" height="330">
        <circle cx="165" cy="165" r="150" fill="rgba(255,255,255,0.25)" stroke="black" stroke-width="3"/>

        <!-- Hour Hand -->
        <line x1="165" y1="165"
              x2="{165 + 70 * math.sin(math.radians(hour_angle))}"
              y2="{165 - 70 * math.cos(math.radians(hour_angle))}"
              stroke="black" stroke-width="6" />

        <!-- Minute Hand -->
        <line x1="165" y1="165"
              x2="{165 + 105 * math.sin(math.radians(min_angle))}"
              y2="{165 - 105 * math.cos(math.radians(min_angle))}"
              stroke="black" stroke-width="4" />

        <!-- Second Hand -->
        <line x1="165" y1="165"
              x2="{165 + 130 * math.sin(math.radians(sec_angle))}"
              y2="{165 - 130 * math.cos(math.radians(sec_angle))}"
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
    return f"<div style='font-size:48px; font-weight:bold; color:white; text-align:center;'>{now}</div>"

# -----------------------------------------------------
# 🚀 MAIN LOOP
# -----------------------------------------------------
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
