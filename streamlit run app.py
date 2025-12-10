import streamlit as st
import datetime
import math
import time

st.set_page_config(page_title="Animated Nature Clock (Fixed)", layout="wide")

# ----------------------------
# Time helpers
# ----------------------------
def get_time():
    now = datetime.datetime.now()
    return now.hour, now.minute, now.second

# ----------------------------
# Analog SVG generator
# ----------------------------
def analog_svg(hour, minute, second, size=330):
    # angles
    second_angle = second * 6
    minute_angle = minute * 6 + second * 0.1
    hour_angle = (hour % 12) * 30 + minute * 0.5

    # convert to radians and offset -90 so 0deg is top
    hr = math.radians(hour_angle - 90)
    mr = math.radians(minute_angle - 90)
    sr = math.radians(second_angle - 90)

    cx = size // 2
    cy = size // 2
    r = int(size * 0.36)

    hour_len = r * 0.58
    min_len = r * 0.8
    sec_len = r * 0.92

    hx = cx + hour_len * math.cos(hr)
    hy = cy + hour_len * math.sin(hr)

    mx = cx + min_len * math.cos(mr)
    my = cy + min_len * math.sin(mr)

    sx = cx + sec_len * math.cos(sr)
    sy = cy + sec_len * math.sin(sr)

    svg = f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
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
    </svg>"""
    return svg

# ----------------------------
# Gradient background (no image)
# ----------------------------
def get_gradient(second):
    # 60-second cycle; map to three zones: day -> afternoon -> night -> day
    p = second / 60.0

    day = (135, 206, 250)        # light sky
    afternoon = (250, 214, 165)  # warm
    night = (25, 25, 112)        # deep blue

    if p < 1/3:
        a = p / (1/3)
        r = int(day[0] + a * (afternoon[0] - day[0]))
        g = int(day[1] + a * (afternoon[1] - day[1]))
        b = int(day[2] + a * (afternoon[2] - day[2]))
    elif p < 2/3:
        a = (p - 1/3) / (1/3)
        r = int(afternoon[0] + a * (night[0] - afternoon[0]))
        g = int(afternoon[1] + a * (night[1] - afternoon[1]))
        b = int(afternoon[2] + a * (night[2] - afternoon[2]))
    else:
        a = (p - 2/3) / (1/3)
        r = int(night[0] + a * (day[0] - night[0]))
        g = int(night[1] + a * (day[1] - night[1]))
        b = int(night[2] + a * (day[2] - night[2]))

    return f"rgb({r},{g},{b})"

# ----------------------------
# UI loop
# ----------------------------
placeholder = st.empty()

while True:
    hour, minute, second = get_time()
    bg_color = get_gradient(second)

    with placeholder.container():
        # background style
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(180deg, {bg_color}, #000000 90%);
                transition: background 0.9s linear;
                background-attachment: fixed;
            }}
            .clock-box {{
                display:flex;
                align-items:center;
                justify-content:center;
                gap:40px;
                padding-top:40px;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"<h1 style='text-align:center;color:white;text-shadow:2px 2px 6px rgba(0,0,0,0.7);'>🌿 Animated Nature Clock</h1>", unsafe_allow_html=True)

        # two columns
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("## 🕰️ Analog Clock")
            st.markdown(analog_svg(hour, minute, second, size=360), unsafe_allow_html=True)

        with col2:
            st.markdown("## ⏰ Digital Clock")
            st.markdown(
                f"""
                <div style="
                    width:360px;
                    margin:0 auto;
                    padding:18px;
                    border-radius:14px;
                    text-align:center;
                    font-size:56px;
                    font-weight:700;
                    color:white;
                    background: rgba(255,255,255,0.12);
                    backdrop-filter: blur(6px);
                ">
                    {hour:02d}:{minute:02d}:{second:02d}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    time.sleep(1)
