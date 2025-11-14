import streamlit as st
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Fugacity Calculator (Pitzer Correlation)",
    layout="centered"
)

# ------------------------------------------------------------
# GLOBAL CUSTOM CSS
# ------------------------------------------------------------
st.markdown("""
<style>
/* GLOBAL FONT & BACKGROUND */
html, body {
    font-family: 'Segoe UI', sans-serif;
    background: #f4f6f9;
}

/* HEADER BAR */
.main-header {
    background: linear-gradient(90deg, #004aad, #007bff);
    padding: 25px;
    margin: -90px 0 30px 0;
    border-radius: 0 0 18px 18px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.main-header h1 {
    margin: 0;
    font-size: 38px;
    font-weight: 800;
}

/* INPUT CARDS */
.card {
    background: white;
    padding: 25px 30px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* BUTTON UPGRADE */
div.stButton > button {
    background: linear-gradient(90deg, #007bff, #00aaff);
    color: white;
    padding: 10px 26px;
    border-radius: 8px;
    font-size: 18px;
    border: none;
    font-weight: 600;
}
div.stButton > button:hover {
    transform: scale(1.04);
    transition: 0.2s;
}

/* HOMEPAGE TITLE */
.home-title {
    font-size: 48px;
    font-weight: 900;
    color: #007bff;
    text-shadow: 2px 2px 10px rgba(0,123,255,0.25);
}

/* RESULTS TABLE */
thead th {
    background-color: #004aad !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Session State: Homepage Toggle
# ------------------------------------------------------------
if "show_homepage" not in st.session_state:
    st.session_state.show_homepage = True

# ------------------------------------------------------------
# HOMEPAGE INTRO SCREEN
# ------------------------------------------------------------
if st.session_state.show_homepage:

    st.markdown("""
    <div style="text-align:center; padding:60px;">
        <h1 class="home-title">⚗️ Fugacity Calculator Suite</h1>

        <p style="font-size:20px; max-width:720px; margin:auto;">
            Welcome to the interactive calculator for estimating fugacity and fugacity coefficients
            using the <b>Pitzer virial correlation</b>. This tool is designed for chemical engineers,
            researchers, and students working with real-gas behavior and VLE systems.
        </p>

        <br/>

        <h3 style="color:#007bff;">Developed By</h3>
        <p style="font-size:17px; line-height:1.6;">
            Dale Clarenz Cabato · Francisco Andrei Joseph Laudez · Aliona Tejada ·  
            Rafaela Villas · Archie Plata · Andrea Hernandez ·  
            Armela Martin · Dimple Padilla
        </p>

        <br/><br/>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Enter Calculator"):
        st.session_state.show_homepage = False

    st.stop()

# ------------------------------------------------------------
# Header Section with Gradient Bar
# ------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🌡️ Fugacity & Fugacity Coefficient Calculator</h1>
    <p style="margin-top:6px; font-size:18px;">
        Pitzer Virial Correlation • Multi-Species Support • Real Gas Thermodynamics
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Gas Database (Critical Constants)
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

# ------------------------------------------------------------
# Pitzer Correlation Function
# ------------------------------------------------------------
def pitzer_fugacity(T, P, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P / Pc
    B0 = 0.083 - (0.422 / Tr**1.6)
    B1 = 0.139 - (0.172 / Tr**4.2)
    ln_phi = (Pr / Tr) * (B0 + omega * B1)
    phi = np.exp(ln_phi)
    f = phi * P
    return {
        "Tr": Tr,
        "Pr": Pr,
        "B0": B0,
        "B1": B1,
        "phi": phi,
        "fugacity": f
    }

# ------------------------------------------------------------
# Multi-Species Input Section
# ------------------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("🧪 Multi-Species Fugacity Calculator")

num_species = st.selectbox("Number of species:", [1, 2, 3])

species_inputs = []
for i in range(num_species):
    st.subheader(f"Species {i+1}")
    gas = st.selectbox(f"Gas {i+1}", list(gases.keys()), key=f"gas_{i}")
    mole_frac = st.number_input(
        f"Mole fraction y{i+1}",
        min_value=0.0, max_value=1.0,
        value=1.0 if i == 0 else 0.0,
        step=0.01, key=f"y_{i}"
    )
    species_inputs.append({
        "name": gas,
        "Tc": gases[gas]["Tc"],
        "Pc": gases[gas]["Pc"],
        "omega": gases[gas]["omega"],
        "y": mole_frac
    })

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Operating Conditions
# ------------------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("🌡️ Operating Conditions")

col1, col2 = st.columns(2)
with col1:
    T = st.number_input("Temperature (T) [K]", value=300.0)
with col2:
    P = st.number_input("Pressure (P) [bar]", value=10.0)

multi_calc = st.button("🧮 Calculate Fugacity & φ")
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Multi-Species Results
# ------------------------------------------------------------
if multi_calc:
    total_y = sum([s["y"] for s in species_inputs])
    if total_y > 1.0:
        st.error("❌ Total mole fraction exceeds 1. Fix your inputs.")
    else:
        results = []
        for s in species_inputs:
            res = pitzer_fugacity(T, P, s["Tc"], s["Pc"], s["omega"])
            f_corrected = res["fugacity"] * s["y"]
            results.append({
                "Gas": s["name"],
                "y": f"{s['y']:.2f}",
                "Tr": f"{res['Tr']:.3f}",
                "Pr": f"{res['Pr']:.3f}",
                "B⁰": f"{res['B0']:.5f}",
                "B¹": f"{res['B1']:.5f}",
                "φ": f"{res['phi']:.5f}",
                "Fugacity (bar)": f"{f_corrected:.5f}"
            })

        df_multi = pd.DataFrame(results)

        st.success("✅ Fugacity and φ calculation complete!")
        st.dataframe(df_multi, use_container_width=True)

# ------------------------------------------------------------
# Footer Notes
# ------------------------------------------------------------
st.markdown("""
<br><br>
---
**References**  
- Pitzer, K.S. & Curl, R.F. Jr. (1957). *Journal of the American Chemical Society*, **79**, 2369.  
- Smith, Van Ness & Abbott. *Introduction to Chemical Engineering Thermodynamics*.
""")

