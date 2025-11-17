import streamlit as st
import numpy as np
import pandas as pd
import time

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Fugacity Calculator (Pitzer Correlation)", layout="centered")

# ------------------------------------------------------------
# Custom CSS Styling
# ------------------------------------------------------------
st.markdown("""
    <style>
        html, body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f4f8;
        }
        h1, h2, h3 {
            color: #1E88E5;
        }
        .stNumberInput input {
            background-color: #ffffff;
            border: 1px solid #1E88E5;
            border-radius: 5px;
            padding: 5px;
        }
        div.stButton > button {
            background-color: #1E88E5;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #1565C0;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.image("https://static.vecteezy.com/system/resources/thumbnails/050/393/628/small/cute-curious-gray-and-white-kitten-in-a-long-shot-photo.jpg", width=200)
    st.markdown("### 📘 About This App")
    st.info("This calculator uses the Pitzer correlation to estimate fugacity and fugacity coefficients for gases under non-ideal conditions.")
    st.markdown("---")
    st.markdown("Made with ❤️ by Chemical Engineering Students")

# ------------------------------------------------------------
# Session State: Homepage Toggle
# ------------------------------------------------------------
if "show_homepage" not in st.session_state:
    st.session_state.show_homepage = True
import time

# ------------------------------------------------------------
# Loading Screen with Logo (Auto-Disappear)
# ------------------------------------------------------------
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder:
        st.markdown("""
            <div style="text-align:center; padding:60px;">
                <img src="https://github.com/dalecabato4-maker/SOLTHERMO-FINAL-PR0JECT/blob/main/Untitled_design__3_-removebg-preview.png?raw=true" width="400" style="margin-bottom:40px;" />
                <h2 style="color:#1E88E5;">🔄 Loading Fugacity Calculator...</h2>
                <p style="font-size:16px;">Initializing thermodynamic models and styling interface...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3.5)  # Simulate loading delay
    loading_placeholder.empty()  # Clear the loading screen
    st.session_state.loaded = True
# ------------------------------------------------------------
# HOMEPAGE INTRO SCREEN
# ------------------------------------------------------------
if st.session_state.show_homepage:
    st.markdown("""
    <div style="text-align:center; padding:40px;">
        <h1 style="font-size:42px;">⚗️ Fugacity Calculator Suite</h1>
        <p style="font-size:18px; max-width:700px; margin:auto;">
            Welcome to the Fugacity & Fugacity Coefficient Calculator using the <b>Pitzer correlation</b>.  
            Fugacity is a corrected pressure that accounts for non-ideal gas behavior — essential for accurate thermodynamic modeling.  
            This tool supports both pure gases and mixtures, and is based on the work of Pitzer & Curl (1957).
        </p>
        <br/>
        <h3 style="color:#00aaff;">Developed By:</h3>
        <p style="font-size:16px;">
            Dale Clarenz Cabato · Francisco Andrei Joseph Laudez · Aliona Tejada · Rafaela Villas ·  
            Archie Plata · Andrea Hernandez · Armela Martin · Dimple Padilla
        </p>
        <br/><br/>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Enter Calculator"):
        st.session_state.show_homepage = False

    st.stop()

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
# Header Section
# ------------------------------------------------------------
st.title("🌡️ Fugacity & Fugacity Coefficient Calculator (Pitzer Correlation)")
st.markdown("""
This interactive app estimates *fugacity* and *fugacity coefficient (φ)* for selected gases  
using the *Pitzer correlation*. It supports both pure gases and mixtures (via mole fraction input).
""")

# ------------------------------------------------------------
# Multi-Species Input Section
# ------------------------------------------------------------
st.markdown("""<h2>🧪 Multi-Species Fugacity Calculation <span style="color:#1E88E5;">(Ideal Gas model)</span></h2>""",
            unsafe_allow_html=True)


num_species = st.selectbox("Number of species to calculate:", [1, 2, 3])

species_inputs = []
for i in range(num_species):
    st.subheader(f"Species {i+1}")

    gas = st.selectbox(
        f"Select gas {i+1}",
        list(gases.keys()),
        key=f"gas_{i}"
    )

    # Default critical properties
    Tc = gases[gas]["Tc"]
    Pc = gases[gas]["Pc"]
    omega = gases[gas]["omega"]

    # --- CUSTOM OPTION ---
    if gas == "Custom":
        st.warning("Enter custom critical properties for this gas:")

        Tc = st.number_input(
            f"Custom Tc (K) for species {i+1}",
            min_value=1.0,
            value=300.0,
            step=1.0,
            key=f"custom_Tc_{i}"
        )

        Pc = st.number_input(
            f"Custom Pc (bar) for species {i+1}",
            min_value=0.1,
            value=50.0,
            step=0.1,
            key=f"custom_Pc_{i}"
        )

        omega = st.number_input(
            f"Custom acentric factor (ω) for species {i+1}",
            min_value=-0.5,
            max_value=1.0,
            value=0.10,
            step=0.01,
            key=f"custom_omega_{i}"
        )

    mole_frac = st.number_input(
        f"Mole fraction y{i+1}",
        min_value=0.0, max_value=1.0,
        value=1.0 if i == 0 else 0.0,
        step=0.01,
        key=f"y_{i}"
    )

    species_inputs.append({
        "name": gas,
        "Tc": Tc,
        "Pc": Pc,
        "omega": omega,
        "y": mole_frac
    })

# ------------------------------------------------------------
# Required Operating Conditions
# ------------------------------------------------------------
st.header("🌡️ Required Operating Conditions")

col1, col2 = st.columns(2)
with col1:
    T = st.number_input("Temperature (T) [K]", min_value=1.0, value=300.0, step=0.1, help="Enter temperature in Kelvin")
with col2:
    P = st.number_input("Pressure (P) [bar]", min_value=0.01, value=10.0, step=0.1, help="Enter pressure in bar")

multi_calc = st.button("🧮 Calculate Fugacity and φ")

# ------------------------------------------------------------
# Multi-Species Calculation & Results
# ------------------------------------------------------------
def highlight_gradient(val, min_val, max_val, base="#ECEFF1", accent="#90CAF9"):
    """Apply a gradient background based on value."""
    try:
        val = float(val)
        ratio = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
        def blend(c1, c2, r):
            return tuple(int(c1[i] + (c2[i] - c1[i]) * r) for i in range(3))
        base_rgb = tuple(int(base[i:i+2], 16) for i in (1, 3, 5))
        accent_rgb = tuple(int(accent[i:i+2], 16) for i in (1, 3, 5))
        blended = blend(base_rgb, accent_rgb, ratio)
        return f"background-color: rgb{blended}"
    except:
        return ""

if multi_calc:
    progress = st.progress(0)
    status = st.empty()

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)
        status.write(f"Computing thermodynamic properties... {i+1}%")

    progress.empty()
    status.empty()
    
    if total_y > 1.0:
        st.error("❌ Total mole fraction exceeds 1. Please adjust inputs.")
    else:
        results = []
        for s in species_inputs:
            res = pitzer_fugacity(T, P, s["Tc"], s["Pc"], s["omega"])
            f_corrected = res["phi"] * s["y"] * P
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

        st.success("✅ Multi-species calculation completed!")
        # Convert Fugacity column to float for styling
        df_multi["Fugacity (bar)"] = df_multi["Fugacity (bar)"].astype(float)

        # Get min and max for gradient scaling
        min_f = df_multi["Fugacity (bar)"].min()
        max_f = df_multi["Fugacity (bar)"].max()

        # Apply gradient styling to Fugacity column
        styled_df = df_multi.style.applymap(
            lambda v: highlight_gradient(v, min_f, max_f),
            subset=["Fugacity (bar)"]
        ).set_table_styles([
            {"selector": "thead th", "props": [
                ("background-color", "#172630"),
                ("color", "gray"),
                ("text-align", "center"),
                ("font-weight", "bold")
            ]},
            {"selector": "tbody td", "props": [
                ("text-align", "center"),
                ("padding", "6px 10px")
            ]},
            {"selector": "tbody tr:hover td", "props": [
                ("background-color", "#172630")
            ]}
        ])

        st.write(styled_df)



        st.caption("Each fugacity value is corrected by mole fraction (f × y).")
