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
# Custom CSS for Material Design
# ------------------------------------------------------------
st.markdown("""
<style>
/* Main background */
.main {
    background-color: #F3F6F9;
}

/* Card container */
.material-card {
    background-color: white;
    padding: 20px 25px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-top: 18px;
}

/* Section headers */
.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #0D47A1;
    padding-bottom: 8px;
    border-bottom: 2px solid #1E88E5;
    margin-bottom: 10px;
}

/* Sidebar style */
.sidebar .sidebar-content {
    background-color: #E3F2FD !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Header Section
# ------------------------------------------------------------
st.markdown("<h1 style='color:#0D47A1;'>🌡️ Fugacity & Fugacity Coefficient Calculator</h1>", 
            unsafe_allow_html=True)

st.markdown("""
This interactive tool calculates **fugacity** and the **fugacity coefficient (φ)**  
using the **Pitzer correlation**. Supports pure gases and mixtures.
""")

# ------------------------------------------------------------
# Gas Database
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
# Sidebar: Gas Selection
# ------------------------------------------------------------
st.sidebar.header("⚙️ Gas Selection & Constants")
selected_gas = st.sidebar.selectbox("Select a gas:", list(gases.keys()))

Tc = st.sidebar.number_input("Critical Temperature Tc (K)", value=gases[selected_gas]["Tc"], step=0.1)
Pc = st.sidebar.number_input("Critical Pressure Pc (bar)", value=gases[selected_gas]["Pc"], step=0.1)
omega = st.sidebar.number_input("Acentric Factor ω", value=gases[selected_gas]["omega"], step=0.001)

R = 0.08314  # L·bar/(mol·K)

# ------------------------------------------------------------
# Input Section
# ------------------------------------------------------------
with st.container():
    st.markdown("<div class='material-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🧮 Input Conditions</div>", unsafe_allow_html=True)

    T = st.number_input("Temperature (T) [K]", value=300.0, step=0.1)
    P = st.number_input("Pressure (P) [bar]", value=10.0, step=0.1)
    y = st.number_input("Concentration / Mole Fraction (y)", value=1.0, min_value=0.0, max_value=1.0, step=0.01)

    calculate = st.button("🧮 Calculate Fugacity and φ", type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

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
# Results Section
# ------------------------------------------------------------
if calculate:

    results = pitzer_fugacity(T, P, Tc, Pc, omega)
    fugacity_adjusted = results["fugacity"] * y

    st.markdown("<div class='material-card'>", unsafe_allow_html=True)
    st.success("Calculation completed successfully!")

    st.markdown("<div class='section-title'>📊 Results</div>", unsafe_allow_html=True)

    df_results = pd.DataFrame({
        "Parameter": [
            "Selected Gas", "Reduced Temperature (Tr)", "Reduced Pressure (Pr)",
            "B⁰", "B¹", "Fugacity Coefficient (φ)", "Fugacity (f, bar)"
        ],
        "Value": [
            selected_gas,
            f"{results['Tr']:.3f}",
            f"{results['Pr']:.3f}",
            f"{results['B0']:.5f}",
            f"{results['B1']:.5f}",
            f"{results['phi']:.5f}",
            f"{fugacity_adjusted:.5f}"
        ]
    })

    st.dataframe(
        df_results.style.set_table_styles([
            {"selector": "thead th", "props": [("background-color", "#1E88E5"), ("color", "white"), ("text-align", "center")]},
            {"selector": "tbody td", "props": [("background-color", "#F9FBFD"), ("text-align", "center"), ("padding", "6px 10px")]},
        ]).hide(axis="index"),
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("""
---
**References:**
- Pitzer, K.S. & Curl, R.F. Jr. (1957). *J. Am. Chem. Soc.*, 79, 2369.  
- Smith, Van Ness, & Abbott. *Intro to Chemical Engineering Thermodynamics*.
""")

