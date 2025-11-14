import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np

# ------------------------------------------------------------
# Page Configuration MUST be first Streamlit command
# ------------------------------------------------------------
st.set_page_config(
    page_title="Fugacity Calculator (Pitzer Correlation)",
    page_icon="⚗️",
    layout="centered"
)

# ------------------------------------------------------------
# INTRO PAGE LOGIC
# ------------------------------------------------------------
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:

    st.markdown("""
    <style>
    /* Remove Streamlit default padding */
    .main > div {
        padding-top: 0rem;
    }

    /* Full-screen container */
    .fullscreen-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;

        background: url('https://images.unsplash.com/photo-1581091012184-5c8f8b9c3f65?auto=format&fit=crop&w=1400&q=60')
                    center/cover no-repeat fixed;

        display: flex;
        justify-content: center;
        align-items: center;

        backdrop-filter: brightness(0.45);
        z-index: -1;
    }

    /* Centered content box */
    .intro-box {
        width: 75%;
        max-width: 900px;

        background: rgba(0, 0, 0, 0.60);
        padding: 50px 70px;
        border-radius: 25px;
        text-align: center;
        color: white;

        animation: fadein 1.2s ease-in-out;
    }

    /* Title */
    .intro-title {
        font-size: 60px;
        font-weight: 900;
        margin-bottom: 10px;
    }

    /* Subtitle */
    .intro-subtitle {
        font-size: 28px;
        margin-bottom: 25px;
        color: #e0e0e0;
    }

    .intro-text {
        font-size: 20px;
        line-height: 1.7;
        margin-bottom: 20px;
    }

    .team-title {
        margin-top: 30px;
        font-size: 30px;
        font-weight: 700;
    }

    .team-names {
        font-size: 20px;
        line-height: 1.7;
        margin-bottom: 10px;
    }

    /* Fade-in animation */
    @keyframes fadein {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    </style>

    <div class="fullscreen-bg"></div>

    <div class="intro-box">
        <h1 class="intro-title">⚗️ Chemical Engineering Calculator Suite</h1>
        <div class="intro-subtitle">Fugacity & Fugacity Coefficient (Pitzer Correlation)</div>

        <p class="intro-text">
            A full-screen interactive calculator for real-gas behavior using the
            <b>Pitzer Virial Equation</b>. Designed for chemical engineering
            students, process engineers, and researchers dealing with VLE,
            thermodynamics, and high-pressure systems.
        </p>

        <p class="intro-text">
            Compute **Fugacity**, **Fugacity Coefficient**, **Reduced Properties**,
            and **Pitzer Second Virial Coefficients** with ease.
        </p>

        <h2 class="team-title">Developed By</h2>
        <div class="team-names">
            Dale CLarenz Cabato<br>
            Francisco Andrei Joseph Laudez<br>
            Aliona Tejada<br>
            Rafaela Villas<br>
            Archie Plata<br>
            Andrea Hernandez<br>
            Armela Martin<br>
            Dimple Padilla
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    if st.button("🚀 Enter Fugacity Calculator"):
        st.session_state.show_intro = False

    st.stop()

# ------------------------------------------------------------
# PAGE BACKGROUND (Chemical Lab Style)
# ------------------------------------------------------------
background_image_url = "https://png.pngtree.com/thumb_back/fh260/background/20210728/pngtree-hexagon-light-effect-molecular-structure-chemical-engineering-geometric-texture-colorful-background-image_752109.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# HEADER / INTRO STYLING
# ------------------------------------------------------------
st.title("🌡️ Fugacity & Fugacity Coefficient Calculator (Pitzer Correlation)")

st.markdown("""
<div style="background-color: rgba(0, 0, 0, 0.7); padding: 20px 25px; border-radius: 12px;">
<h2 style="color:#f0f6ff; font-weight:800;"> Overview </h2>

<p style="font-size:16px; color:#f0f6ff;">
This tool computes fugacity and non-ideal gas behavior using the <b>Pitzer Correlation</b>.
Ideal for chemical engineers working with:
<br><b>thermodynamics, VLE, high-pressure gases, reactors,</b> and <b>separation processes.</b>
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# GAS PROPERTIES
# ------------------------------------------------------------
gases = {
    "Carbon Dioxide (CO₂)": {"Tc": 304.2, "Pc": 73.8, "omega": 0.225},
    "Methane (CH₄)": {"Tc": 190.6, "Pc": 45.99, "omega": 0.011},
    "Nitrogen (N₂)": {"Tc": 126.2, "Pc": 33.5, "omega": 0.037},
    "Oxygen (O₂)": {"Tc": 154.6, "Pc": 50.4, "omega": 0.022},
    "Hydrogen (H₂)": {"Tc": 33.2, "Pc": 12.8, "omega": -0.22},
    "Ammonia (NH₃)": {"Tc": 405.5, "Pc": 113.5, "omega": 0.256},
    "Custom": {"Tc": 300.0, "Pc": 50.0, "omega": 0.1}
}

# SIDEBAR
st.sidebar.header("⚙️ Gas Selection")
selected_gas = st.sidebar.selectbox("Choose a gas:", list(gases.keys()))

Tc = st.sidebar.number_input("Critical Temperature Tc (K)", value=gases[selected_gas]["Tc"])
Pc = st.sidebar.number_input("Critical Pressure Pc (bar)", value=gases[selected_gas]["Pc"])
omega = st.sidebar.number_input("Acentric Factor ω", value=gases[selected_gas]["omega"])

R = 0.08314  # L·bar/mol-K

# ------------------------------------------------------------
# USER INPUTS
# ------------------------------------------------------------
st.header("🧮 Input Conditions")

T = st.number_input("Temperature (K)", value=300.0)
P = st.number_input("Pressure (bar)", value=10.0)
y = st.number_input("Mole Fraction (y)", value=1.0, min_value=0.0, max_value=1.0)

clicked = st.button("Calculate Fugacity")

# ------------------------------------------------------------
# PITZER FUNCTION
# ------------------------------------------------------------
def pitzer_fugacity(T, P, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P / Pc

    B0 = 0.083 - (0.422 / Tr**1.6)
    B1 = 0.139 - (0.172 / Tr**4.2)

    ln_phi = (Pr / Tr) * (B0 + omega * B1)
    phi = np.exp(ln_phi)
    f = phi * P

    return Tr, Pr, B0, B1, phi, f

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------
if clicked:
    Tr, Pr, B0, B1, phi, f = pitzer_fugacity(T, P, Tc, Pc, omega)

    f_corrected = f * y

    df = pd.DataFrame({
        "Parameter": [
            "Reduced Temperature (Tr)",
            "Reduced Pressure (Pr)",
            "B⁰",
            "B¹",
            "Fugacity Coefficient (φ)",
            "Fugacity (bar, corrected)"
        ],
        "Value": [
            f"{Tr:.4f}",
            f"{Pr:.4f}",
            f"{B0:.5f}",
            f"{B1:.5f}",
            f"{phi:.5f}",
            f"{f_corrected:.5f}"
        ]
    })

    st.success("Calculation completed successfully!")
    st.dataframe(df, use_container_width=True)

    st.caption("Computed using Pitzer Correlation (1957)")

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("""
---
**References:**  
- Pitzer, K.S. & Curl, R.F. Jr. (1957). *J. Am. Chem. Soc.*, 79, 2369.  
- Smith, Van Ness & Abbott — *Intro to Chemical Engineering Thermodynamics (8th Ed.)*
""")



