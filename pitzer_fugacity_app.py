import streamlit as st
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Fugacity Calculator (Pitzer Correlation)", layout="centered")

# ------------------------------------------------------------
# Custom CSS Styling
# ------------------------------------------------------------
st.markdown("""
<style>
/* Global background for calculator */
.stApp {
    background: linear-gradient(135deg, #f0f4f8, #dbe9f4);
    font-family: 'Segoe UI', sans-serif;
}

/* Homepage fullscreen */
.fullscreen {
    position: fixed;
    inset: 0;
    background: linear-gradient(135deg, #0b0f17, #0f1720, #0d1b2a);
    background-size: 300% 300%;
    animation: gradientShift 12s ease infinite;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.intro-box {
    background: rgba(255, 255, 255, 0.08);
    padding: 40px;
    border-radius: 16px;
    text-align: center;
    color: #eaf2ff;
    backdrop-filter: blur(10px);
    max-width: 700px;
}

.intro-box h1 {
    font-size: 42px;
    margin-bottom: 12px;
}

.intro-box p {
    font-size: 17px;
    line-height: 1.6;
}

.intro-box .team {
    margin-top: 20px;
    font-size: 15px;
    color: #aeeaff;
}

.enter-button {
    margin-top: 30px;
    padding: 12px 28px;
    font-size: 16px;
    font-weight: bold;
    color: white;
    background: linear-gradient(90deg, #00c2ff, #0066ff);
    border: none;
    border-radius: 30px;
    cursor: pointer;
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
    <div class="fullscreen">
        <div class="intro-box">
            <h1>⚗️ Fugacity Calculator Suite</h1>
            <p>
                Welcome to the Fugacity & Fugacity Coefficient Calculator using the <b>Pitzer correlation</b>.<br/>
                Fugacity is a corrected pressure that accounts for non-ideal gas behavior — essential for accurate thermodynamic modeling.
            </p>
            <p>
                This tool supports both pure gases and mixtures, and is based on the work of Pitzer & Curl (1957).
            </p>
            <div class="team">
                <b>Developed By:</b><br/>
                Dale Clarenz Cabato · Francisco Andrei Joseph Laudez · Aliona Tejada · Rafaela Villas ·<br/>
                Archie Plata · Andrea Hernandez · Armela Martin · Dimple Padilla
            </div>
            <form action="" method="post">
                <button class="enter-button" type="submit">🚀 Enter Calculator</button>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.form("enter_form").form_submit_button("Enter Calculator"):
        st.session_state.show_homepage = False

    st.stop()

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
# Calculator Interface
# ------------------------------------------------------------
st.title("🌡️ Fugacity & Fugacity Coefficient Calculator")
st.markdown("Use the Pitzer correlation to compute fugacity and φ for up to 3 gas species.")

st.header("🌡️ Required Operating Conditions")
col1, col2 = st.columns(2)
with col1:
    T = st.number_input("Temperature (T) [K]", min_value=1.0, value=300.0, step=0.1)
with col2:
    P = st.number_input("Pressure (P) [bar]", min_value=0.01, value=10.0, step=0.1)

st.header("🧪 Multi-Species Input")

num_species = st.selectbox("Number of species to calculate:", [1, 2, 3])

species_inputs = []
for i in range(num_species):
    st.subheader(f"Species {i+1}")
    gas = st.selectbox(f"Select gas {i+1}", list(gases.keys()), key=f"gas_{i}")
    mole_frac = st.number_input(f"Mole fraction y{i+1}", min_value=0.0, max_value=1.0, value=1.0 if i == 0 else 0.0, step=0.01, key=f"y_{i}")
    species_inputs.append({
        "name": gas,
        "Tc": gases[gas]["Tc"],
        "Pc": gases[gas]["Pc"],
        "omega": gases[gas]["omega"],
        "y": mole_frac
    })

if st.button("🧮 Calculate Fugacity and φ"):
    total_y = sum([s["y"] for s in species_inputs])
    if total_y > 1.0:
        st.error("❌ Total mole fraction exceeds 1. Please adjust inputs.")
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

        st.success("✅ Multi-species calculation completed!")
      st.dataframe(
    df_multi.style.set_table_styles([
        {"selector": "thead th", "props": [("background-color", "#1E88E5"), ("color", "white"), ("text-align", "center"), ("font-weight", "bold")]},
        {"selector": "tbody td", "props": [("background-color", "#F5F7FA"), ("text-align", "center"), ("padding", "6px 10px")]},
        {"selector": "tbody tr:hover td", "props": [("background-color", "#E3F2FD")]}
    ]),
    use_container_width=True
)
