import streamlit as st
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# PAGE CONFIGURATION WITH CHEMICAL ENGINEERING THEME
# ------------------------------------------------------------
st.set_page_config(
    page_title="Fugacity Calculator (Pitzer Correlation)",
    layout="centered",
    page_icon="⚗️"
)

# ------------------------------------------------------------
# CUSTOM CHEMICAL ENGINEERING CSS DESIGN
# ------------------------------------------------------------
chemical_css = """
<style>
/* Background with chemical engineering blueprint pattern */
.stApp {
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url('https://i.imgur.com/0ZfS9ZQ.png');
    background-size: cover;
}

/* Title styling */
h1 {
    color: #0D47A1 !important;
    text-shadow: 1px 1px 2px #90CAF9;
    font-weight: 800 !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] > div:first-child {
    background-color: #E3F2FD;
    background-image: url('https://i.imgur.com/YpZPpXE.png');
    background-size: 200px;
    background-repeat: no-repeat;
    background-position: bottom;
    border-right: 3px solid #64B5F6;
}

/* Input fields */
input, select {
    border-radius: 10px !important;
    border: 1px solid #64B5F6 !important;
}

/* Buttons */
.stButton>button {
    background-color: #1565C0;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}
.stButton>button:hover {
    background-color: #0D47A1;
}

/* Data table */
.dataframe tbody tr:hover {
    background-color: #BBDEFB !important;
}
</style>
"""

st.markdown(chemical_css, unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER WITH CHE THEME
# ------------------------------------------------------------
st.title("⚗️ Fugacity & Fugacity Coefficient Calculator (Pitzer Correlation)")
st.markdown("""
This app estimates **fugacity** and **fugacity coefficient (φ)** using the **Pitzer correlation**.

Designed with a **Chemical Engineering theme** — featuring blueprint textures, process diagrams,
and modern UI styling inspired by plant control panels and P&ID aesthetics.
""")

# ------------------------------------------------------------
# GAS DATABASE
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
# SIDEBAR WITH CHEMICAL ENGINEERING LOOK
# ------------------------------------------------------------
st.sidebar.header("🛢️ Gas Selection & Critical Properties")
selected_gas = st.sidebar.selectbox("Select a Gas:", list(gases.keys()))

Tc = st.sidebar.number_input("Critical Temperature Tc (K)", value=gases[selected_gas]["Tc"], step=0.1)
Pc = st.sidebar.number_input("Critical Pressure Pc (bar)", value=gases[selected_gas]["Pc"], step=0.1)
omega = st.sidebar.number_input("Acentric Factor (ω)", value=gases[selected_gas]["omega"], step=0.001)

R = 0.08314

# ------------------------------------------------------------
# USER INPUTS
# ------------------------------------------------------------
st.header("🔧 Operating Conditions")
T = st.number_input("Temperature (T) [K]", value=300.0, step=0.1)
P = st.number_input("Pressure (P) [bar]", value=10.0, step=0.1)
y = st.number_input("Mole Fraction (y)", value=1.0, min_value=0.0, max_value=1.0, step=0.01)

calculate = st.button("🧮 Calculate Fugacity & φ")

# ------------------------------------------------------------
# PITZER EQUATION FUNCTION
# ------------------------------------------------------------
def pitzer_fugacity(T, P, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P / Pc
    B0 = 0.083 - (0.422 / Tr**1.6)
    B1 = 0.139 - (0.172 / Tr**4.2)
    ln_phi = (Pr / Tr) * (B0 + omega * B1)
    phi = np.exp(ln_phi)
    f = phi * P
    return {"Tr": Tr, "Pr": Pr, "B0": B0, "B1": B1, "phi": phi, "fugacity": f}

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------
if calculate:
    results = pitzer_fugacity(T, P, Tc, Pc, omega)
    fugacity_adjusted = results["fugacity"] * y

    df_results = pd.DataFrame({
        "Parameter": [
            "Selected Gas", "Reduced Temperature (Tr)", "Reduced Pressure (Pr)",
            "B⁰", "B¹", "Fugacity Coefficient (φ)", "Fugacity (bar)"
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

    st.success("✔ Fugacity Computed Successfully!")

    st.dataframe(df_results.style.hide(axis="index"))

    st.caption("Computed using the Pitzer Correlation (Pitzer & Curl, 1957)")

# ------------------------------------------------------------
# FOOTER WITH CHEMICAL ENGINEERING ICONS
# ------------------------------------------------------------
st.markdown("""
---
📘 **References**  
- Pitzer, K.S. & Curl, R.F. (1957). *J. Am. Chem. Soc.*, 79, 2369.  
- Smith & Van Ness — *Chemical Engineering Thermodynamics*.

🧪 Designed for **Chemical Engineering students & researchers**.
""")
