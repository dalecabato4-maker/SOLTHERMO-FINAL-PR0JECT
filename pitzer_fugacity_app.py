import streamlit as st
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Fugacity Calculator (Pitzer Correlation)", layout="centered")

# ------------------------------------------------------------
# Header Section
# ------------------------------------------------------------
st.title("🌡️ Fugacity & Fugacity Coefficient Calculator (Pitzer Correlation)")
st.markdown("""
This interactive app estimates *fugacity* and *fugacity coefficient (φ)* for selected gases  
using the *Pitzer correlation*. It supports both pure gases and mixtures (via mole fraction input).
""")

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

# ------------------------------------------
# GAS SELECTION
# ------------------------------------------
st.sidebar.header("⚙️ Gas Selection & Constants")
selected_gas = st.sidebar.selectbox("Select a gas:", list(gases.keys()))

Tc = st.sidebar.number_input("Critical Temperature Tc (K)", value=gases[selected_gas]["Tc"], step=0.1)
Pc = st.sidebar.number_input("Critical Pressure Pc (bar)", value=gases[selected_gas]["Pc"], step=0.1)
omega = st.sidebar.number_input("Acentric Factor ω", value=gases[selected_gas]["omega"], step=0.001)

R = 0.08314  # L·bar/(mol·K)

# ------------------------------------------
# USER INPUTS
# ------------------------------------------
st.header("🧮 Input Conditions")

T = st.number_input("Temperature (T) [K]", value=300.0, step=0.1)
P = st.number_input("Pressure (P) [bar]", value=10.0, step=0.1)
y = st.number_input("Concentration / Mole Fraction (y)", value=1.0, min_value=0.0, max_value=1.0, step=0.01)

calculate = st.button("🧮 Calculate Fugacity and φ")

# ------------------------------------------------------------
# Pitzer Correlation Function
# ------------------------------------------------------------
def pitzer_fugacity(T, P, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P / Pc

    # Correlations for second virial coefficients
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

    # Create a DataFrame for clean table display
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

    # Table styling
    st.success("✅ Calculation completed successfully!")
    st.header("📊 Results Table")

    st.dataframe(
        df_results.style.set_table_styles([
            {"selector": "thead th", "props": [("background-color", "#1E88E5"), ("color", "white"), ("text-align", "center"), ("font-weight", "bold")]},
            {"selector": "tbody td", "props": [("background-color", "#F5F7FA"), ("text-align", "center"), ("padding", "6px 10px")]},
            {"selector": "tbody tr:hover td", "props": [("background-color", "#E3F2FD")]}
        ]).hide(axis="index"),
        use_container_width=True
    )

    st.divider()
    st.caption("Computed using Pitzer Correlation (Pitzer & Curl, 1957)")

# ------------------------------------------------------------
# Footer Notes
# ------------------------------------------------------------
st.markdown("""
---
**References:**
- Pitzer, K.S. & Curl, R.F. Jr. (1957). *J. Am. Chem. Soc.*, **79**, 2369.  
- Smith, J.M., Van Ness, H.C., & Abbott, M.M. *Introduction to Chemical Engineering Thermodynamics* (8th Ed.).
""")
