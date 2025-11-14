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
    .intro-container {
        width: 90%;
        max-width: 1100px;
        margin-left: auto;
        margin-right: auto;
        margin-top: 40px;
        padding: 50px 60px;
        background: rgba(0, 0, 0, 0.55);
        backdrop-filter: blur(6px);
        border-radius: 20px;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
    }
    .intro-title {
        font-size: 60px;
        font-weight: 900;
        margin-bottom: 5px;
    }
    .intro-subtitle {
        font-size: 26px;
        color: #d8d8d8;
        margin-top: -10px;
        margin-bottom: 25px;
    }
    .intro-text {
        font-size: 20px;
        line-height: 1.65;
        margin-left: auto;
        margin-right: auto;
        max-width: 900px;
    }
    .intro-list {
        text-align: left;
        margin: 0 auto;
        margin-top: 20px;
        max-width: 700px;
        font-size: 19px;
        line-height: 1.6;
    }
    .team-title {
        font-size: 30px;
        margin-top: 45px;
        font-weight: 700;
    }
    .team-names {
        font-size: 22px;
        line-height: 1.7;
    }
    </style>

    <div class="intro-container">

        <img src='https://cdn-icons-png.flaticon.com/512/3004/3004613.png'
            width='170' style='margin-bottom:20px;'>

        <div class="intro-title">⚗️ Chemical Engineering Calculator Suite</div>
        <div class="intro-subtitle">Fugacity & Fugacity Coefficient (Pitzer Correlation)</div>

        <p class="intro-text">
            Welcome to the Fugacity & Fugacity Coefficient Calculator — a powerful tool made for
            <b>Chemical Engineering students, researchers, and process design engineers</b>.
            This application helps you compute essential real-gas properties needed for
            thermodynamic modeling and high-pressure system design.
        </p>

        <div class="intro-list">
            <b>This tool calculates:</b><br><br>
            • Fugacity Coefficient (φ) <br>
            • Fugacity (corrected real-gas pressure) <br>
            • Reduced Properties (Tr, Pr) <br>
            • Pitzer Virial Coefficients (B⁰ & B¹) <br><br>
            Useful for VLE analysis, reactor design, gas processing, and high-pressure equipment simulations.
        </div>

        <div class="team-title">Developed By:</div>

        <div class="team-names">
            <b>Dale CLarenz Cabato</b><br>
            <b>Francisco Andrei Joseph Laudez</b><br>
            <b>Aliona Tejada</b><br>
            <b>Rafaela Villas</b><br>
            <b>Archie Plata</b><br>
            <b>Andrea Hernandez</b><br>
            <b>Armela Martin</b><br>
            <b>Dimple Padilla</b><br>
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



