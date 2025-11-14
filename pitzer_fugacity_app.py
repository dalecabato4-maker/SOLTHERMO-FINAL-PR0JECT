import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np

st.set_page_config(layout="wide")

# Initialize intro state
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

# INTRO SCREEN
if st.session_state.show_intro:

    st.markdown(
"""
<style>
/* Reset padding and margins for full-screen effect */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

body {
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #0d0d0d, #1a1a2e, #16213e);
    background-size: 300% 300%;
    animation: gradientShift 12s ease infinite;
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}

/* Background gradient animation */
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Floating animation */
@keyframes float {
    0% {transform: translateY(0);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0);}
}

.fullscreen-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

.intro-box {
    width: 80%;
    max-width: 900px;
    background: rgba(0,0,0,0.55);
    padding: 50px;
    border-radius: 22px;
    text-align: center;
    backdrop-filter: blur(12px);
    animation: fadeIn 1.4s ease, float 6s ease-in-out infinite;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 0 30px rgba(0,0,0,0.5);
}

/* TITLES */
.intro-title {
    font-size: 55px;
    font-weight: 900;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
    text-shadow: 0px 0px 15px rgba(255,255,255,0.25);
}

.intro-subtitle {
    font-size: 26px;
    opacity: 0.85;
    margin-bottom: 25px;
}

/* TEXT */
.intro-text {
    font-size: 20px;
    line-height: 1.7;
    opacity: 0.95;
    margin-bottom: 15px;
}

/* TEAM SECTION */
.team-title {
    font-size: 28px;
    font-weight: bold;
    margin-top: 30px;
    color: #00d4ff;
    text-shadow: 0px 0px 10px rgba(0,212,255,0.4);
}

.team-names {
    font-size: 20px;
    line-height: 1.7;
    margin-top: 10px;
}

/* BUTTON STYLE */
.enter-button {
    margin-top: 30px;
    background: linear-gradient(135deg, #00d4ff, #0077ff);
    padding: 14px 40px;
    border-radius: 30px;
    font-size: 22px;
    font-weight: bold;
    color: white !important;
    border: none;
    cursor: pointer;
    transition: 0.3s ease;
    box-shadow: 0 0 15px rgba(0,162,255,0.5);
}

.enter-button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 25px rgba(0,162,255,0.9);
}
</style>

<div class="fullscreen-wrapper">
    <div class="intro-box">

        <div class="intro-title">Calculator Suite</div>
        <div class="intro-subtitle">Fugacity & Fugacity Coefficient<br>(Pitzer Correlation)</div>

        <p class="intro-text">
            A fully interactive tool for predicting real-gas behavior using the 
            <b>Pitzer Virial Method</b>.
        </p>

        <p class="intro-text">
            This calculator provides <b>Fugacity (f)</b>, <b>Fugacity Coefficient (φ)</b>,
            reduced properties, and Pitzer's <b>Second Virial Coefficients</b>.
        </p>

        <div class="team-title">Developed By</div>
        <div class="team-names">
            Dale Clarenz Cabato<br>
            Francisco Andrei Joseph Laudez<br>
            Aliona Tejada<br>
            Rafaela Villas<br>
            Archie Plata<br>
            Andrea Hernandez<br>
            Armela Martin<br>
            Dimple Padilla
        </div>

    </div>
</div>
""",
unsafe_allow_html=True)

    # Streamlit replacement button under the HTML overlay
    enter = st.button("🚀 Enter Calculator", key="enter_calc")

    if enter:
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



