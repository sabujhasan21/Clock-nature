import streamlit as st
import datetime
import math
import time

st.set_page_config(page_title="Animated Nature Clock", layout="wide")

# -------------------------------------------
# FUNCTIONS
# -------------------------------------------

def get_time():
    now = datetime.datetime.now()
    return now.hour, now.minute, now.second

def analog_svg(hour, minute, second):
    # Convert to angles
    second_angle = second * 6
    minute_angle = minute * 6 + second * 0.1
    hour_angle = (hour % 12) * 30 + minute * 0.5

    # Convert to radians
    hr = math.radians(hour_angle - 90)
    mr = math.radians(minute_angle - 90)
    sr = math.radians(second_angle - 90)

    cx, cy, r = 165, 165, 120

    # Hand lengths
    hour_len = 70
    min_len = 95
    sec_len = 110

    hx = cx + hour_len * math.cos(hr)
    hy = cy + hour_len * math.sin(hr)

    mx = cx + min_len * math.cos(mr)
    my = cy + min_len * math.sin(mr)

    sx = cx + sec_len * math.cos(sr)
    sy = cy + sec_len * math.sin(sr)

    svg = f"""
    <svg width="330" height="330">

        <!-- Clock outer ring -->
        <circle cx="{cx}" cy="{cy}" r="{r}" stroke="white" stroke-width="5" fill="#ffffff33" />

        <!-- Hour Hand -->
        <line x1="{cx}" y1="{cy}" x2="{hx}" y2="{hy}" stroke="black" stroke-width="6" />

        <!-- Minute Hand -->
        <line x1="{cx}" y1="{cy}" x2="{mx}" y2="{my}" stroke="black" stroke-width="4" />

        <!-- Second Hand -->
        <line x1="{cx}" y1="{cy}" x2="{sx}" y2="{sy}" stroke="red" stroke-width="2" />

        <circle cx="{cx}" cy="{cy}" r="6" fill="black" />
    </svg>
    """
    return svg

# -------------------------------------------
# ANIMATED GRADIENT BACKGROUND
# -------------------------------------------

def get_gradient(second):
    # 60 sec cycle → background color pulse
    p = second / 60

    # day → afternoon → night
    # smoothly blending colors
    # (R, G, B)
    day = (135, 206, 250)
    afternoon = (250, 214, 165)
    night = (25, 25, 112)

    if p < 0.33:
        a = p / 0.33
        r = int(day[0] + a * (afternoon[0] - day[0]))
        g = int(day[1] + a * (afternoon[1] - day[1]))
        b = int(day[2] + a * (afternoon[2] - day[2]))
    elif p < 0.66:
        a = (p - 0.33) / 0.33
        r = int(afternoon[0] + a * (night[0] - afternoon[0]))
        g = int(afternoon[1] + a * (night[1] - afternoon[1]))
        b = int(afternoon[2] + a * (night[2] - afternoon[2]))
    else:
        a = (p - 0.66) / 0.34
        r = int(night[0] + a * (day[0] - night[0]))
        g = int(night[1] + a * (day[1] - night[1]))
        b = int(night[2] + a * (day[2] - night[2]))

    return f"rgb({r},{g},{b})"

# -------------------------------------------
# UI LOOP (AUTO REFRESH EVERY SECOND)
# -------------------------------------------

placeholder = st.empty()

while True:
    hour, minute, second = get_time()
    bg = get_gradient(second)

    with placeholder.container():
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background: linear-gradient(180deg, {bg}, #000000);
                    transition: background 1s linear;
                    background-size: cover;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("## 🕰️ Analog Clock")
            st.markdown(analog_svg(hour, minute, second), unsafe_allow_html=True)

        with col2:
            st.markdown("## ⏰ Digital Clock")
            st.markdown(
                f"""
                <div style="
                    font-size: 60px;
                    padding: 20px;
                    background:#ffffff44;
                    width:330px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    backdrop-filter: blur(8px);
                ">
                    {hour:02d}:{minute:02d}:{second:02d}
                </div>
                """,
                unsafe_allow_html=True
            )

    time.sleep(1)    return f"""
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
