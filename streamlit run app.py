import streamlit as st
import time
import math
from datetime import datetime

st.set_page_config(page_title="Nature Clock Ultra Pro", layout="wide")

# -----------------------------------------------------
# 🌄 BACKGROUNDS
# -----------------------------------------------------
BG_SUNNY = "https://i.imgur.com/R0BgbaN.jpeg"
BG_CLOUDY = "https://i.imgur.com/k8hrmH0.jpeg"
BG_RAINY = "https://i.imgur.com/VXQ4Rh4.jpeg"
BG_NIGHT = "https://i.imgur.com/8A2RtwU.jpeg"

GRADIENT_SUNRISE = "linear-gradient(#FFB75E,#ED8F03)"
GRADIENT_SUNSET = "linear-gradient(#654ea3,#eaafc8)"

CLOUDS_GIF = "https://i.imgur.com/cinbVvG.gif"
RAIN_GIF = "https://i.imgur.com/6hE6x4p.gif"
LIGHTNING_GIF = "https://i.imgur.com/ZV7Yu1T.gif"

MUSIC_URL = "https://www2.cs.uic.edu/~i101/SoundFiles/Bird.wav"
st.audio(MUSIC_URL, autoplay=True)


# -----------------------------------------------------
# AUTO WEATHER
# -----------------------------------------------------
def get_auto_weather():
    s = datetime.now().second
    if 0 <= s < 15:
        return "Sunny"
    elif 15 <= s < 30:
        return "Cloudy"
    elif 30 <= s < 45:
        return "Rainy"
    else:
        return "Night"


# -----------------------------------------------------
# BACKGROUND CSS
# -----------------------------------------------------
def set_background(bg_image=None, gradient=None):
    if gradient:
        css = f"background:{gradient};"
    else:
        css = (
            f"background-image:url('{bg_image}');"
            "background-size:cover;background-position:center;"
        )

    st.markdown(
        f"""
        <style>
        .stApp {{
            {css}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------
# CLOUDS / RAIN / LIGHTNING
# -----------------------------------------------------
def show_clouds():
    st.markdown(
        f"""
        <img src="{CLOUDS_GIF}" style="
        width:100%;position:fixed;top:0;left:0;
        opacity:0.5;z-index:1;">
        """,
        unsafe_allow_html=True,
    )


def show_rain():
    st.markdown(
        f"""
        <img src="{RAIN_GIF}" style="
        width:100%;position:fixed;top:0;left:0;
        opacity:0.6;z-index:2;">
        """,
        unsafe_allow_html=True,
    )


def show_lightning():
    st.markdown(
        f"""
        <img src="{LIGHTNING_GIF}" style="
        width:100%;position:fixed;top:0;left:0;
        opacity:0.9;z-index:3;">
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------
# DIGITAL CLOCK
# -----------------------------------------------------
def digital_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    return f"""
    <div style='font-size:55px;font-weight:bold;
    color:white;text-align:center;text-shadow:2px 2px 5px black;'>
        {now}
    </div>
    """


# -----------------------------------------------------
# ANALOG CLOCK SVG
# -----------------------------------------------------
def analog_clock():
    now = datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour % 12

    sec_a = sec * 6
    min_a = minute * 6
    hour_a = hour * 30 + minute * 0.5

    hx = 165 + 70 * math.sin(math.radians(hour_a))
    hy = 165 - 70 * math.cos(math.radians(hour_a))

    mx = 165 + 105 * math.sin(math.radians(min_a))
    my = 165 - 105 * math.cos(math.radians(min_a))

    sx = 165 + 130 * math.sin(math.radians(sec_a))
    sy = 165 - 130 * math.cos(math.radians(sec_a))

    return f"""
    <svg width="330" height="330">
        <circle cx="165" cy="165" r="150"
        fill="rgba(255,255,255,0.25)" stroke="black" stroke-width="3"/>

        <line x1="165" y1="165" x2="{hx}" y2="{hy}"
        stroke="black" stroke-width="6"/>

        <line x1="165" y1="165" x2="{mx}" y2="{my}"
        stroke="black" stroke-width="4"/>

        <line x1="165" y1="165" x2="{sx}" y2="{sy}"
        stroke="red" stroke-width="2"/>

        <circle cx="165" cy="165" r="6" fill="black"/>
    </svg>
    """


# -----------------------------------------------------
# SIDEBAR WEATHER CONTROL
# -----------------------------------------------------
st.sidebar.title("Weather Mode")
mode = st.sidebar.radio(
    "Select Mode",
    ["Auto", "Sunny", "Cloudy", "Rainy", "Night", "Sunrise", "Sunset"],
)


# -----------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------
ui = st.empty()

while True:
    weather = mode if mode != "Auto" else get_auto_weather()

    # Set backgrounds
    if weather == "Sunny":
        set_background(bg_image=BG_SUNNY)

    elif weather == "Cloudy":
        set_background(bg_image=BG_CLOUDY)
        show_clouds()

    elif weather == "Rainy":
        set_background(bg_image=BG_RAINY)
        show_rain()
        if datetime.now().second % 7 == 0:
            show_lightning()

    elif weather == "Night":
        set_background(bg_image=BG_NIGHT)

    elif weather == "Sunrise":
        set_background(gradient=GRADIENT_SUNRISE)

    elif weather == "Sunset":
        set_background(gradient=GRADIENT_SUNSET)

    # ---------------------------
    # UI Update
    # ---------------------------
    with ui.container():
        st.markdown(
            f"""
            <h1 style='text-align:center;color:white;
            text-shadow:3px 3px 5px black;'>
                🌿 Nature Clock Ultra Pro — {weather} Mode
            </h1>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(digital_clock(), unsafe_allow_html=True)

        st.markdown(
            f"<div style='text-align:center;margin-top:-10px;'>{analog_clock()}</div>",
            unsafe_allow_html=True,
        )

    time.sleep(1)        unsafe_allow_html=True,
    )

def show_lightning():
    st.markdown(
        f"""
        <img src="{LIGHTNING_GIF}" style="
            width:100%;
            position:fixed;
            top:0;
            left:0;
            opacity:0.9;
            z-index:2;
        ">
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------
# DIGITAL CLOCK
# -----------------------------------------------------
def digital_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    return f"""
        <div style='font-size:55px;font-weight:bold;color:white;text-align:center;text-shadow:2px 2px 5px black;'>
            {now}
        </div>
    """


# -----------------------------------------------------
# ANALOG CLOCK
# -----------------------------------------------------
def analog_clock():
    now = datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour % 12

    sec_a = sec * 6
    min_a = minute * 6
    hour_a = hour * 30 + minute * 0.5

    hx = 165 + 70 * math.sin(math.radians(hour_a))
    hy = 165 - 70 * math.cos(math.radians(hour_a))

    mx = 165 + 105 * math.sin(math.radians(min_a))
    my = 165 - 105 * math.cos(math.radians(min_a))

    sx = 165 + 130 * math.sin(math.radians(sec_a))
    sy = 165 - 130 * math.cos(math.radians(sec_a))

    return f"""
    <svg width="330" height="330">
        <circle cx="165" cy="165" r="150" fill="rgba(255,255,255,0.25)" stroke="black" stroke-width="3"/>

        <line x1="165" y1="165" x2="{hx}" y2="{hy}" stroke="black" stroke-width="6"/>
        <line x1="165" y1="165" x2="{mx}" y2="{my}" stroke="black" stroke-width="4"/>
        <line x1="165" y1="165" x2="{sx}" y2="{sy}" stroke="red" stroke-width="2"/>

        <circle cx="165" cy="165" r="6" fill="black"/>
    </svg>
    """


# -----------------------------------------------------
# WEATHER BUTTONS
# -----------------------------------------------------
st.sidebar.title("Weather Control")
mode = st.sidebar.radio("Mode", ["Auto", "Sunny", "Cloudy", "Rainy", "Night", "Sunrise", "Sunset"])

# -----------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------
ui = st.empty()

while True:

    # Get current weather (auto or manual)
    weather = mode if mode != "Auto" else get_auto_weather()

    # Set backgrounds according to weather
    if weather == "Sunny":
        set_background(bg_image=BG_SUNNY)
    elif weather == "Cloudy":
        set_background(bg_image=BG_CLOUDY)
        show_clouds()
    elif weather == "Rainy":
        set_background(bg_image=BG_RAINY)
        show_rain()
        if datetime.now().second % 7 == 0:
            show_lightning()
    elif weather == "Night":
        set_background(bg_image=BG_NIGHT)
    elif weather == "Sunrise":
        set_background(gradient=GRADIENT_SUNRISE)
    elif weather == "Sunset":
        set_background(gradient=GRADIENT_SUNSET)

    with ui.container():

        st.markdown(
            f"""
            <h1 style='text-align:center;color:white;text-shadow:3px 3px 5px black;'>
                🌿 Nature Clock Ultra Pro — {weather} Mode
            </h1>
            """,
            unsafe_allow_html=True,
        )

        # Digital Clock
        st.markdown(digital_clock(), unsafe_allow_html=True)

        # Analog Clock
        st.markdown(
            f"<div style='text-align:center;margin-top:-10px;'>{analog_clock()}</div>",
            unsafe_allow_html=True,
        )

    time.sleep(1)def digital_clock():
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
