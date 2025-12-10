import streamlit as st
import datetime
import math
import time

st.set_page_config(page_title="Analog Clock Only", layout="wide")

# ----------------------------
# Time helper
# ----------------------------
def get_time():
    now = datetime.datetime.now()
    return now.hour, now.minute, now.second

# ----------------------------
# Analog SVG generator
# ----------------------------
def analog_svg(hour, minute, second, size=360):
    # Convert angles
    second_angle = second * 6
    minute_angle = minute * 6 + second * 0.1
    hour_angle = (hour % 12) * 30 + minute * 0.5

    # Convert to radians
    hr = math.radians(hour_angle - 90)
    mr = math.radians(minute_angle - 90)
    sr = math.radians(second_angle - 90)

    cx = size // 2
    cy = size // 2
    r = int(size * 0.36)

    # Hand lengths
    hour_len = r * 0.58
    min_len = r * 0.76
    sec_len = r * 0.92

    # Calculate end points
    hx = cx + hour_len * math.cos(hr)
    hy = cy + hour_len * math.sin(hr)

    mx = cx + min_len * math.cos(mr)
    my = cy + min_len * math.sin(mr)

    sx = cx + sec_len * math.cos(sr)
    sy = cy + sec_len * math.sin(sr)

    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="g" cx="50%" cy="40%">
                <stop offset="0%" stop-color="rgba(255,255,255,0.55)"/>
                <stop offset="100%" stop-color="rgba(255,255,255,0.15)"/>
            </radialGradient>
        </defs>

        <!-- face -->
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g)" stroke="rgba(0,0,0,0.25)" stroke-width="3"/>

        <!-- hour -->
        <line x1="{cx}" y1="{cy}" x2="{hx:.3f}" y2="{hy:.3f}" stroke="black" stroke-width="6" stroke-linecap="round"/>

        <!-- minute -->
        <line x1="{cx}" y1="{cy}" x2="{mx:.3f}" y2="{my:.3f}" stroke="black" stroke-width="4" stroke-linecap="round"/>

        <!-- second -->
        <line x1="{cx}" y1="{cy}" x2="{sx:.3f}" y2="{sy:.3f}" stroke="red" stroke-width="2" stroke-linecap="round"/>

        <!-- center -->
        <circle cx="{cx}" cy="{cy}" r="6" fill="black"/>
    </svg>
    """
    return svg

# ----------------------------
# Animated gradient background
# ----------------------------
def get_gradient(second):
    p = second / 60.0
    day = (135, 206, 250)
    afternoon = (250, 214, 165)
    night = (25, 25, 112)

    if p < 1/3:
        a = p / (1/3)
        r = int(day[0] + a * (afternoon[0]-day[0]))
        g = int(day[1] + a * (afternoon[1]-day[1]))
        b = int(day[2] + a * (afternoon[2]-day[2]))
    elif p < 2/3:
        a = (p - 1/3) / (1/3)
        r = int(afternoon[0] + a * (night[0]-afternoon[0]))
        g = int(afternoon[1] + a * (night[1]-afternoon[1]))
        b = int(afternoon[2] + a * (night[2]-afternoon[2]))
    else:
        a = (p - 2/3) / (1/3)
        r = int(night[0] + a * (day[0]-night[0]))
        g = int(night[1] + a * (day[1]-night[1]))
        b = int(night[2] + a * (day[2]-night[2]))

    return f"rgb({r},{g},{b})"

# ----------------------------
# Main UI loop
# ----------------------------
placeholder = st.empty()

while True:
    hour, minute, second = get_time()
    bg_color = get_gradient(second)

    with placeholder.container():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(180deg, {bg_color}, #000000 95%);
                transition: background 0.9s linear;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<h1 style='text-align:center;color:white;'>🕰️ Animated Analog Clock</h1>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div style='display:flex;justify-content:center;padding-top:20px;'>{analog_svg(hour,minute,second,360)}</div>",
            unsafe_allow_html=True
        )

    time.sleep(1)
